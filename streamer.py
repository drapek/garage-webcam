import cv2, socket, sys, pickle, struct


class Streamer:
    STREAM_IP = "192.168.1.30"
    STREAM_PORT = 8089
    image_splitter = None  # splitter is initialized in constructor
    socket = None  # socket is initialized in constructor

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_STREAM)  # Stream
        self.socket.connect((self.STREAM_IP, self.STREAM_PORT))  # TODO handle exceptions -> while disconnected

    def run(self):
        cap = cv2.VideoCapture(0)

        cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.cv.CV_CAP_PROP_FOURCC, cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'))

        cap.set(cv2.cv.CV_CAP_PROP_FPS, 1)

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==True:

                frame_serialized = pickle.dumps(frame)
                print("[LOG] Frame size: {}", len(frame_serialized))
                self.socket.sendall(struct.pack("q", len(frame_serialized)) + frame_serialized)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            else:
                break

        # Release everything if job is finished
        cap.release()
        cv2.destroyAllWindows()
