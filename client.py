import pickle
import struct
import socket
import cv2

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 6042
sock.connect(("127.0.0.1", port))

data = b""
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = sock.recv(4096)

        if not packet:
            break
        data += packet
    packed_msg = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg)[0]

    while len(data) < msg_size:
        data += sock.recv(4096)
    frame = data[:msg_size]
    data = data[msg_size:]
    vid = pickle.loads(frame)
    cv2.imshow("the video from client side", vid)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
sock.close()