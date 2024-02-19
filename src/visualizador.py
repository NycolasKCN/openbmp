from tkinter import Tk
from tkinter.filedialog import askopenfilename
from dataclasses import dataclass
import os
from matplotlib.pyplot import imshow, show


class bitmap_image:
    def __init__(self, file_size:int, width:int, height:int):
        self.file_size = file_size
        self.width, self.height = width, height
        self.bitmap = [[(0,0,0) for _ in range(self.width)] for _ in range(self.height)]
        
    def __str__(self):
        return f"filesize: {self.file_size} bytes; width: {self.width}; height: {self.height}"


janela = Tk().withdraw()
path_name = askopenfilename(initialdir="./",
                            filetypes=[("Image Files", "*.bmp")])

# para ler os bytes de um arquivo utilizar o "rb"
# sample size = 70 bytes

with open(path_name, "rb") as file:
    if file.read(2) != b'BM':
        print("Não é uma imagem bitmap")
        exit()
        
    file_size = int.from_bytes(file.read(4), byteorder="little")
    
    file.seek(10)
    
    image_data_start = int.from_bytes(file.read(4), byteorder="little")
    print(image_data_start)
    
    file.seek(4, os.SEEK_CUR)
    
    width = int.from_bytes(file.read(4), byteorder="little")
    height = int.from_bytes(file.read(4), byteorder="little")
    
    file.seek(2, os.SEEK_CUR)
    
    bytes_per_pixel = int.from_bytes(file.read(2), byteorder="little") / 8
    print(bytes_per_pixel)
    
    compression = int.from_bytes(file.read(4), byteorder="little")
    print(compression)
    
    image_size = int.from_bytes(file.read(4), byteorder="little")
    print(image_size)
    
    file.seek(image_data_start, os.SEEK_SET)
    
    image = bitmap_image(file_size, width, height)
    
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
        
print(image)
imshow(image.bitmap, interpolation='nearest')
show()

    