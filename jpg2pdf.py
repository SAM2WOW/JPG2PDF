#JPG2PDF Converter
#Designed by Sam F

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pygubu
import os
#PDF
from fpdf import FPDF
#from PIL import Image

class Application:
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file(self.resource_path("UI.ui"))

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('TopBase', master)

        # Connect method callbacks
        builder.connect_callbacks(self)
    
    def resource_path(self, relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath("./source/repos/JPG2PDF/")

        return os.path.join(base_path, relative_path)

    #Functions
    def open_files(self):
        mask = [("JPG Images","*.jpg")]
        global filez
        filez = filedialog.askopenfilenames(parent=root, filetypes=mask, title='Choose your images')
        print (str(filez))
        if filez != None:
            self.builder.get_variable("jpg_loc").set(str(filez))

            file_n = []
            for f in filez:
                filename = str(f)
                file_n.append(str(os.path.basename(filename)))
            self.builder.get_variable("selected_jpgs").set(str(file_n))

    def open_locations(self):
        mask = [("Portable Document Format","*.pdf")]  
        global fout
        fout = filedialog.askdirectory(title='Choose a location to save the PDF')
        if fout != None:
            self.builder.get_variable("fout_loc").set(str(fout))

    def convert(self):
        #Get Setting Size
        papersize = self.builder.get_variable("paper_size").get()
        paperori = self.builder.get_variable("paper_orien").get()

        if papersize != "" and paperori != "":
                
            #Convertion
            if paperori == "Portrait":
                ori_s = "P"
            else:
                ori_s = "L"
            
            if papersize == "Letter":
                sizecode = "L"
            elif papersize == "A4":
                sizecode = "A"

            #Dictionary
            pdf_size = {'LP': {'w': 8.5, 'h': 11}, 'LL': {'w': 11, 'h': 8.5}, 'AP': {'w': 8.27, 'h': 11.69}, 'AL': {'w': 11.69, 'h': 8.27}}

            pdf = FPDF(ori_s, 'in', papersize)
            for image in filez:
                #Check Image Size
                #img_width, img_height = Image.size(image)
                
                pdf.add_page()
                pdf.image(image, x = 0, y = 0, w = pdf_size[sizecode + ori_s]["w"], h = pdf_size[sizecode + ori_s]["h"], type = 'JPG')
            pdf.output(str(fout) + "/J2PConverted.pdf", "F")

            #Message
            messagebox.showinfo("Finished!", "PDF file converted!")
        else:
            messagebox.showinfo("No Settings", "Please pick the settings first")
            


root = tk.Tk()
app = Application(root)
root.title('JPG2PDF tool v1.0    by Sam Feng')
#root.iconbitmap(Applicationresource_path("export_icon.png"))
root.resizable(False, False)

root.mainloop()