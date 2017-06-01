import cv2, socket, sys, pickle, struct
from PIL import Image
from modules.ImageSplitter import ImageSplitter


class Streamer:
    STREAM_IP = "127.0.0.1"
    STREAM_PORT = 8089
    image_splitter = None  # splitter is initialized in constructor
    socket = None  # socket is initialized in constructor

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_STREAM)  # Stream
        self.socket.connect((self.STREAM_IP, self.STREAM_PORT))  # TODO handle exceptions -> while disconnected
        self.image_splitter = ImageSplitter()

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.cv.CV_CAP_PROP_FPS, 20)
        # Define the codec and create VideoWriter object
        fourcc = cv2.cv.CV_FOURCC(*'MJPG')
        out = cv2.VideoWriter('output.avi', fourcc, 10.0, (640, 480))

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==True:
                # save to a file
                out.write(frame)

                cv2.imshow('frame', frame)
                # img_str = cv2.imdecode(frame, cv2.cv.CV_LOAD_IMAGE_COLOR)  # TODO do not work - find solution to convert this to bytecode or string
                # color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # TODO this doesn't work as well
                # frame_as_image = Image.fromarray(frame, 'RGB')  # TODO it gives weird solution -> violet color of the face
                # self.send_image_to_server(frame_as_image)

                frame_serialized = pickle.dumps(frame)
                self.socket.sendall(struct.pack("H", len(frame_serialized))+frame_serialized)

                print("[LOG] Frame size: {}", sys.getsizeof(frame_serialized))
                print("[LOG] Frame content: {}", frame_serialized)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            else:
                break

        # Release everything if job is finished
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def send_image_to_server(self, frame):
        frame_chunks = self.image_splitter.chunk_frame(frame)

        # TODO example working code: sock.sendto(frame, (UDP_IP, UDP_PORT))
        # TODO send each chunk separately - for each loop

