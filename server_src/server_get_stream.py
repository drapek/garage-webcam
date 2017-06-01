import socket
import cv2
import pickle
import struct

HOST='0.0.0.0'
PORT=8089

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print 'Socket created'

s.bind((HOST,PORT))
print 'Socket bind complete'
s.listen(10)
print 'Socket now listening'

conn,addr=s.accept()

print 'Connection established'

data = b''
payload_size = struct.calcsize("q")
while True:
    while len(data) < payload_size:
        data += conn.recv(1024)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("q", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    print ("[LOG] Frame received")
    frame=pickle.loads(frame_data)
    frame = cv2.imdecode(frame, cv2.cv.CV_LOAD_IMAGE_COLOR)  # decode from jpeg bytecode

    # maybe show on website as bytecode
    cv2.imwrite('tmp.jpeg', frame)

    frame2 = cv2.imread('tmp.jpeg')
    cv2.imshow('frame',frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
