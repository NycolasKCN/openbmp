from tkinter import Tk, Button, Label, Menu, messagebox, Toplevel
from openbmp.ImageLoader import ImageLoader, FileFormatError
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt


class OpenbmpVisualizer:
    
    ALL_CHANNELS = -1
    RED_CHANNEL = 0
    GREEN_CHANNEL = 1
    BLUE_CHANNEL = 2
    
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("OpenBMP")
        self.window.config(padx=20, pady=20)
        self.window.geometry("600x200")
        self.window.resizable(width=False, height=False)
        
        self.file_name = None
        self.image = None
        
        self.__init_ui()
    
    def __open_file(self) -> None:
        self.file_name = askopenfilename(initialdir="./", filetypes=[("Image Files", "*.bmp")])
        
        if self.file_name == '': return
        
        try:
            self.image = ImageLoader.load_image(self.file_name)
        except FileFormatError:
            messagebox.showinfo("File format", "You are trying to open an image that is not in bitmap format. Try opening another file.")
            self.file_name = None
            return
        except FileNotFoundError:
            messagebox.showinfo("File not found", "No such file or directory. Try opening another file.")
            

        self.channels = {
            self.ALL_CHANNELS : (self.image.bitmap, "viridis"),
            self.RED_CHANNEL : (self.image.bitmap[:,:,self.RED_CHANNEL], "Reds"),
            self.GREEN_CHANNEL : (self.image.bitmap[:,:,self.GREEN_CHANNEL], "Greens"),
            self.BLUE_CHANNEL : (self.image.bitmap[:,:,self.BLUE_CHANNEL], "Blues")
            } 

        self.file_name_lab.config(text=f"File opened: {self.file_name}")
    
    def __show_image(self, channel: int) -> None:
        if not self.file_name:
            messagebox.showinfo("Open a file", "Open a file before trying to view it.")
            return
        
        plt.title("Image")
        plt.axis("off")
        plt.imshow(self.channels[channel][0], cmap=self.channels[channel][1])
        plt.show()
        
    def __show_info(self):
        if not self.file_name:
            messagebox.showinfo("Open a file", "Open a file before trying to view it.")
            return
        
        info_window = Toplevel()
        info_window.title("Image info")
        info_window.config(padx=20, pady=20)
        info_window.geometry("400x350")
        info_window.resizable(width=False, height=False)
        
        file_size_kb = self.image.file_size / 1000
        
        size_label = Label(info_window, text=f"File size: {file_size_kb:.2f} Kb"); size_label.pack()
        width_label = Label(info_window, text=f"Image width: {self.image.width} px"); width_label.pack()
        height_label = Label(info_window, text=f"Image height: {self.image.width} px"); height_label.pack()
        offset_label = Label(info_window, text=f"Bitmap offset: {self.image.image_offset}"); offset_label.pack()
        header_size_label = Label(info_window, text=f"Header size: {self.image.header_size} bytes"); header_size_label.pack()
        planes_label = Label(info_window, text=f"Number of planes: {self.image.num_planes}"); planes_label.pack()
        bpp_label = Label(info_window, text=f"Bytes per pixel: {self.image.bytes_per_pixel} bytes"); bpp_label.pack()
        comp_label = Label(info_window, text=f"Compression: {self.image.compression}"); comp_label.pack()
        data_size_label = Label(info_window, text=f"Image data size: {self.image.image_data_size} bytes"); data_size_label.pack()
        ppm_hor_label = Label(info_window, text=f"Pixel p/ meter horizontal: {self.image.ppm_horizontal} px"); ppm_hor_label.pack()
        ppm_ver_label = Label(info_window, text=f"Pixel p/ meter: {self.image.ppm_vertical} px"); ppm_ver_label.pack()
        colors_label = Label(info_window, text=f"Colors: {self.image.colors}"); colors_label.pack()
        important_colors_label = Label(info_window, text=f"Important colors: {self.image.important_colors}"); important_colors_label.pack()
                    
    def __init_ui(self) -> None:
        menubar = Menu(self.window)
        self.window.config(menu=menubar)
        
        file_menu = Menu(menubar, tearoff=False)
        file_menu.add_command(label="Open", command=self.__open_file)
        file_menu.add_command(label="Show image info", command=self.__show_info)
        menubar.add_cascade(label="File", menu=file_menu)
        
        self.file_name_lab = Label(self.window, text="No file opened.") 
        
        self.file_name_lab.pack(anchor="n", side="top")
        
        show_btn = Button(self.window, text="Show image", width=16, command=lambda: self.__show_image(self.ALL_CHANNELS))
        red_btn = Button(self.window, text="Show red channel", width=16, command=lambda: self.__show_image(self.RED_CHANNEL))
        green_btn = Button(self.window, text="Show green channel", width=16, command=lambda: self.__show_image(self.GREEN_CHANNEL))
        blue_btn = Button(self.window, text="Show blue channel", width=16, command=lambda: self.__show_image(self.BLUE_CHANNEL))
        
        open_btn = Button(self.window, text="Open file", width=16, command=self.__open_file)
        
        show_btn.pack(side="left")
        red_btn.pack(side="left")
        green_btn.pack(side="left")
        blue_btn.pack(side="left")
        
        open_btn.pack(anchor="se", side="bottom")

    def main(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = OpenbmpVisualizer()
    app.main()
