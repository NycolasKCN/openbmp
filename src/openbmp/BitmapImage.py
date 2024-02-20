class BitmapImage:
    def __init__(self, file_size, width, height, bytes_per_pixel, compression, image_size):
        self.file_size = file_size
        self.width, self.height = width, height
        self.bytes_per_pixel = bytes_per_pixel
        self.compression_type = compression
        self.image_size = image_size
        
        self.bitmap = [[(0,0,0) for _ in range(self.width)] for _ in range(self.height)]
        
    def __str__(self):
        return f"filesize: {self.file_size} bytes; width: {self.width}; height: {self.height}"