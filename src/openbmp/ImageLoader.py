from openbmp.BitmapImage import BitmapImage
from openbmp.BitmapBuilder import BitmapBuild
import os


class ImageLoader:
    
    RED = 0
    GREEN = 1
    BLUE = 2
    
    def load_image(file_path) -> BitmapImage:
        with open(file_path, "rb") as file:
            if file.read(2) != b'BM':
                raise FileFormatError("File path does not lead to a bitmap file.")
                
            file_size = int.from_bytes(file.read(4), byteorder="little")
            
            file.seek(10, os.SEEK_SET)
            
            offset = int.from_bytes(file.read(4), byteorder="little")
            header_size = int.from_bytes(file.read(4), byteorder="little")    
            width = int.from_bytes(file.read(4), byteorder="little")
            height = int.from_bytes(file.read(4), byteorder="little")
            num_planes = int.from_bytes(file.read(2), byteorder="little")
            bytes_per_pixel = int.from_bytes(file.read(2), byteorder="little") / 8
            compression = int.from_bytes(file.read(4), byteorder="little")
            image_size = int.from_bytes(file.read(4), byteorder="little")
            ppm_horizontal = int.from_bytes(file.read(4), byteorder="little")
            ppm_vertical = int.from_bytes(file.read(4), byteorder="little")
            colors = int.from_bytes(file.read(4), byteorder="little")
            important_colors = int.from_bytes(file.read(4), byteorder="little")
            
            image = BitmapBuild(file_size, width, height).with_image_offset(offset) \
                        .with_header_size(header_size) \
                        .with_num_planes(num_planes) \
                        .with_bytes_per_pixel(bytes_per_pixel) \
                        .with_compression(compression) \
                        .with_image_data_size(image_size) \
                        .with_ppm_horizontal(ppm_horizontal) \
                        .with_ppm_vertical(ppm_vertical) \
                        .with_colors(colors) \
                        .with_important_colors(important_colors) \
                        .build()
            
            file.seek(image.image_offset, os.SEEK_SET)
            
            pixel_index = 0
            row_index = image.height - 1
            padding = image.width % 4
            while True:
                if pixel_index >= image.width:
                    pixel_index = 0
                    row_index -= 1
                    
                    if row_index == -1:
                        break

                    file.read(padding)
                
                b_byte = file.read(1)
                g_byte = file.read(1)
                r_byte = file.read(1)
                
                image.bitmap[row_index, pixel_index, ImageLoader.RED] = int.from_bytes(r_byte)
                image.bitmap[row_index, pixel_index, ImageLoader.GREEN] = int.from_bytes(g_byte)
                image.bitmap[row_index, pixel_index, ImageLoader.BLUE] = int.from_bytes(b_byte)
                            
                pixel_index += 1
        
        return image
    

class FileFormatError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)