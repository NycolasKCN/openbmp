from BitmapImage import BitmapImage
import os

class ImageLoader:
    def load_image(file_path) -> BitmapImage:
        with open(file_path, "rb") as file:
            if file.read(2) != b'BM':
                raise FileFormatError("File path does not lead to a bitmap file.")
                
            file_size = int.from_bytes(file.read(4), byteorder="little")
            
            file.seek(10)
            
            image_data_start = int.from_bytes(file.read(4), byteorder="little")
            
            file.seek(4, os.SEEK_CUR)
            
            width = int.from_bytes(file.read(4), byteorder="little")
            height = int.from_bytes(file.read(4), byteorder="little")
            
            file.seek(2, os.SEEK_CUR)
            
            bytes_per_pixel = int.from_bytes(file.read(2), byteorder="little") / 8
            compression = int.from_bytes(file.read(4), byteorder="little")
            image_size = int.from_bytes(file.read(4), byteorder="little")
            
            file.seek(image_data_start, os.SEEK_SET)
            
            image = BitmapImage(file_size, width, height, bytes_per_pixel, compression, image_size)
            
            pixel_index = 0
            row_index = image.height - 1
            while True:
                if pixel_index == image.width:
                    pixel_index = 0
                    row_index -= 1
                    
                    if row_index == -1:
                        break
                
                b_byte = file.read(1)
                g_byte = file.read(1)
                r_byte = file.read(1)
                
                if len(b_byte) == 0:
                    break
                
                r = int.from_bytes(r_byte)
                g = int.from_bytes(g_byte)
                b = int.from_bytes(b_byte)
                
                pixel = r,g,b
                
                image.bitmap[row_index][pixel_index] = pixel
                
                pixel_index += 1
        
        return image
    

class FileFormatError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)