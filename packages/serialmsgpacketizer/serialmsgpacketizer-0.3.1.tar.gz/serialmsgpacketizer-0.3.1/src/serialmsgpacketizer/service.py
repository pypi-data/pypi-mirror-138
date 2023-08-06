"""Main classes for serialmsgpacketizer"""
from __future__ import annotations
from typing import Optional, Any, List, cast
from dataclasses import dataclass, field
import logging
import asyncio
import functools

from datastreamcorelib.abstract import ZMQSocketType, ZMQSocketDescription
from datastreamcorelib.binpackers import uuid_to_b64
from datastreamcorelib.datamessage import PubSubDataMessage
from datastreamservicelib.service import SimpleService
from datastreamservicelib.zmqwrappers import Socket
import msgpacketizer
from msgpacketizer.subscriber import SubscriptionTracker
import serial  # type: ignore

LOGGER = logging.getLogger(__name__)


@dataclass
class SerialMsgPacketizerService(SimpleService):
    """Main class for serialmsgpacketizer"""

    _serialtask: Optional[asyncio.Task[Any]] = field(init=False, default=None)
    _serial: Optional[serial.Serial] = field(repr=False, init=False, default=None, hash=False)
    _packetizer: Optional[SubscriptionTracker] = field(repr=False, init=False, default=None, hash=False)
    _reptask: Optional[asyncio.Task[Any]] = field(init=False, default=None)

    async def teardown(self) -> None:
        """Called once by the run method before exiting"""
        await self._close_port()
        # close the REPly handler
        if self._reptask and not self._reptask.done():
            self._reptask.cancel()
            await self._reptask
        # Remember to let SimpleServices own teardown work too.
        await super().teardown()

    async def _close_port(self) -> None:
        """Close the serial port"""
        if self._serial and not self._serial.closed:
            self._serial.close()
        self._serial = None
        if self._serialtask:
            await self._serialtask
        self._serialtask = None

    async def _open_port(self) -> None:
        """Open the serial port"""
        args_dict = dict(self.config["serial"])
        uri = args_dict.pop("uri")
        LOGGER.info("opening port {}".format(uri))
        self._serial = serial.serial_for_url(uri, **args_dict)
        LOGGER.debug("Port is {}".format(self._serial))

    async def _serial_reader_task(self) -> None:
        """Handles the port reading"""
        if not self._serial:
            self.quit(1)
            return
        # re-init the packetizer
        if self._packetizer:
            self._packetizer = None
        self._packetizer = SubscriptionTracker()
        for idx in range(256):
            self._packetizer.subscribe(self._serial, idx, functools.partial(self._handle_packet_synccb, idx))
        try:
            while self._serial and not self._serial.closed:
                # This is blocking but the library does not yet support asyncio
                self._packetizer.parse()
                await asyncio.sleep(0.1)
        except OSError as exc:
            if exc.errno == 9:
                return
            raise
        finally:
            if self._exitcode is None:
                self.quit(1)

    async def _handle_packet(self, idx: int, data: Any) -> None:
        """Handle the packet"""
        msg = PubSubDataMessage("packet_{:03d}".format(idx))
        msg.data.update(
            {
                "idx": idx,
                "payload": data,
            }
        )
        LOGGER.debug("PUBlishing {}".format(msg))
        await self.psmgr.publish_async(msg)

    def _handle_packet_synccb(self, idx: int, data: Any) -> None:
        """Callback for msgpacketizer packets, just created task for actually handling it"""
        asyncio.create_task(self._handle_packet(idx, data))

    async def rep_task(self) -> None:
        """Handle incoming REQuests and REPly to them"""
        sdesc = ZMQSocketDescription(self.config["zmq"]["rep_sockets"], ZMQSocketType.REP)
        sock = cast(Socket, self.psmgr.sockethandler.get_socket(sdesc))
        try:
            while not sock.closed:
                msgparts = await sock.recv_multipart()
                replymsg = await self.handle_rep(msgparts)
                await sock.send_multipart(replymsg.zmq_encode())
        except asyncio.CancelledError:
            pass
        finally:
            if not sock.closed:
                sock.close()

    async def handle_rep(self, msgparts: List[bytes]) -> PubSubDataMessage:  # pylint: disable=R0912
        """Handle the incoming message and construct a reply"""
        loop = asyncio.get_event_loop()
        reply = PubSubDataMessage(b"reply")
        reply.data.update({"failed": False, "exception": None, "reason": None})
        try:
            msg = PubSubDataMessage.zmq_decode(msgparts)
            reply.data["cmd_msgid"] = uuid_to_b64(msg.messageid)
            LOGGER.debug("sending idx={}, payload={}".format(msg.data["idx"], msg.data["payload"]))
            await asyncio.wait_for(
                loop.run_in_executor(None, msgpacketizer.send, self._serial, msg.data["idx"], msg.data["payload"]),
                timeout=0.5,
            )
        except Exception as exc:  # pylint: disable=W0703
            LOGGER.exception("Could not handle incoming message: {}".format(exc))
            reply.data.update({"failed": True, "exception": True, "reason": repr(exc)})
        return reply

    async def reload_async(self) -> None:
        """Async reload stuff"""
        await self._close_port()
        await self._open_port()
        # If we did not get a serial port quit
        if not self._serial:
            self.quit(1)
            return

        asyncio.create_task(self._serial_reader_task())
        self._reptask = asyncio.create_task(self.rep_task())

    def reload(self) -> None:
        """Load configs, restart sockets"""
        super().reload()
        if "timeout" not in self.config["serial"]:
            self.config["serial"]["timeout"] = 0.25
        asyncio.create_task(self.reload_async())
