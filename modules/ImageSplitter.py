

class ImageSplitter():
    image_id = 0

    def chunk_frame(frame, chunk_size=512):
        # TODO split data and add headers
        # 1. divide on array
        # 2. transform it to a string
        # 3. add headers w
        # TODO return array of prepared chunks
        pass

    def get_next_image_id(self):
        self.image_id += 1
        return self.image_id