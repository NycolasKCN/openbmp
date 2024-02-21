from numpy import zeros, uint8

class BitmapImage:
    def __init__(self, file_size:int, width:int, height:int):
        self.file_size = file_size
        self.width = width
        self.height = height
        self.image_offset = None
        self.header_size = None
        self.num_planes = None
        self.bytes_per_pixel = None
        self.compression = None
        self.image_data_size = None
        self.ppm_horizontal = None
        self.ppm_vertical = None
        self.colors = None
        self.important_colors = None
        
        self.bitmap = zeros((self.height, self.width, 3), dtype=uint8)
        
    def __str__(self):
        return f"filesize: {self.file_size} bytes; width: {self.width}; height: {self.height}"