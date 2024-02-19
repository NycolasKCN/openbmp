from tkinter import Tk, Button, Label, Canvas, PhotoImage, Menu, messagebox
from bitmap.ImageLoader import ImageLoader, FileFormatError
from tkinter.filedialog import askopenfilename
import numpy as np
import matplotlib.pyplot as plt


class ImageVisualizer:
    
    ALL_CHANNELS = -1
    RED_CHANNEL = 0
    GREEN_CHANNEL = 1
    BLUE_CHANNEL = 2
    
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("Image visualizer")
        self.window.config(padx=20, pady=20)
        self.window.geometry("600x200")
        self.window.resizable(width=False, height=False)
        
        self.file_name = None
        self.image = None
        
        self.__init_ui()
    
    def __open_file(self) -> None:
        self.file_name = askopenfilename(initialdir="./", filetypes=[("Image Files", "*.bmp")])
        try:
            self.image = ImageLoader.load_image(self.file_name)
        except FileFormatError:
            messagebox.showinfo("File format", "You are trying to open an image that is not in bitmap format. Try opening another file.")
            self.file_name = None
            return
        
        self.file_name_lab.config(text=f"File opened: {self.file_name}")
    
    def __show_image(self, channel: int) -> None:
        if not self.file_name:
            messagebox.showinfo("Open a file", "Open a file before trying to view it.")
            return
        
        img_arr = np.array(self.image.bitmap)

        channels = {
            self.ALL_CHANNELS : (img_arr, "viridis"),
            self.RED_CHANNEL : (img_arr[:,:,self.RED_CHANNEL], "Reds"),
            self.GREEN_CHANNEL : (img_arr[:,:,self.GREEN_CHANNEL], "Greens"),
            self.BLUE_CHANNEL : (img_arr[:,:,self.BLUE_CHANNEL], "Blues")
            } 

        plt.title("Image")
        plt.axis("off")
        plt.imshow(channels[channel][0], cmap=channels[channel][1])
        plt.show()
                
    def __init_ui(self) -> None:
        menubar = Menu(self.window)
        self.window.config(menu=menubar)
        
        file_menu = Menu(menubar)
        file_menu.add_command(label="Open", command=self.__open_file)
        file_menu.add_command(label="Show image info", command=None) # TODO
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
        
        open_btn.pack(anchor="s", side="bottom")

    def main(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = ImageVisualizer()
    app.main()
