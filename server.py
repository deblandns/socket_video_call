import socket
import cv2
import pickle
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 6042
sock.bind(("127.0.0.1", port))
sock.listen(5)

while True:
    client, addr = sock.accept()
    if client:
        capture = cv2.VideoCapture(0)
        while(capture.isOpened()):
            img, frame = capture.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client.sendall(message)
            cv2.imshow("the video in server", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client.close()