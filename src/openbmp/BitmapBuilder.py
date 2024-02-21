from openbmp.BitmapImage import BitmapImage

class BitmapBuild:
    def __init__(self, file_size:int, image_width:int, image_height:int) -> None:
        self.image = BitmapImage(file_size, image_width,image_height)
        
        
    def with_image_offset(self, image_offset):
        self.image.image_offset = image_offset
        return self
    
    def with_header_size(self, header_size):
        self.image.header_size = header_size
        return self
    
    def with_num_planes(self, num_planes):
        self.image.num_planes = num_planes
        return self
    
    def with_bytes_per_pixel(self, bytes_per_pixel):
        self.image.bytes_per_pixel = bytes_per_pixel
        return self
    
    def with_compression(self, compression):
        self.image.compression = compression
        return self
    
    def with_image_data_size(self, image_data_size):
        self.image.image_data_size = image_data_size
        return self
    
    def with_ppm_horizontal(self, ppm_horizontal):
        self.image.ppm_horizontal = ppm_horizontal
        return self
    
    def with_ppm_vertical(self, ppm_vertical):
        self.image.ppm_vertical = ppm_vertical
        return self
    
    def with_colors(self, colors):
        self.image.colors = colors
        return self
    
    def with_important_colors(self, important_colors):
        self.image.important_colors = important_colors
        return self
        
    def build(self):
        return self.image