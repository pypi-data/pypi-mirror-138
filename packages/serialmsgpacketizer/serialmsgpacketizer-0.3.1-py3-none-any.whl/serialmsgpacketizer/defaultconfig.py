"""Default configuration file contents"""

# Remember to add tests for keys into test_serialmsgpacketizer.py
DEFAULT_CONFIG_STR = """
[zmq]
pub_sockets = ["ipc:///tmp/serialmsgpacketizer_pub.sock", "tcp://*:51459"]
rep_sockets = ["ipc:///tmp/serialmsgpacketizer_rep.sock", "tcp://*:51460"]

[serial]
uri = "/dev/tty.USB0"
baudrate = 115200

""".lstrip()
