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
from PIL import Image
#Import Sound
from playsound import playsound

#Tooltip
class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

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

        #Tooltip
        Search_btn0 = CreateToolTip(self.builder.get_object("Select_Files"), "Choose your images")
        Search_btn1 = CreateToolTip(self.builder.get_object("Select_Location"), "Select output location")
        add_btn = CreateToolTip(self.builder.get_object("Add_Files"), "Add more images")
        copy_btn = CreateToolTip(self.builder.get_object("Same_Location"), "Output to source image folder")
        moveup_btn = CreateToolTip(self.builder.get_object("order_up"), "Move image order up")
        movedown_btn = CreateToolTip(self.builder.get_object("order_down"), "Move image order down")
        delete_btn = CreateToolTip(self.builder.get_object("order_delete"), "Delete image")

    def resource_path(self, relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath("./source/repos/JPG2PDF/JPG2PDF/")
            #/source/repos/JPG2PDF/JPG2PDF/

        return os.path.join(base_path, relative_path)

    #preset variables
    def set_default(self):

        if self.builder.get_variable("paper_size").get() == "":
            self.builder.get_variable("paper_size").set("Letter")

        if self.builder.get_variable("paper_orien").get() == "":
            self.builder.get_variable("paper_orien").set("Portrait")

        if self.builder.get_variable("paper_marge").get() == "":
            self.builder.get_variable("paper_marge").set("No_Margin")
        
        if self.builder.get_variable("paper_scale").get() == "":
            self.builder.get_variable("paper_scale").set("Stretch")

    def reset_btn(self):
        self.builder.get_object("convert_btn").config(text='Convert', background='#eafeff')   #Reset Button

    def reset_listbox(self):
        #List
        self.builder.get_object("List").delete(0,'end')
        for f in filez:
            filename = str(f)
            file_n = str(os.path.basename(filename))
            self.builder.get_object("List").insert("end", file_n)

    #Functions
    def open_files(self):
        mask = [("JPG Images","*.jpg")]
        global filez
        filez = filedialog.askopenfilenames(parent=root, filetypes=mask, title='Choose your images')

        #Check if none
        if filez != None:
            self.reset_listbox()    #Reset List
            
        
        self.set_default()   #Setting Default Settings
        self.reset_btn()

    def add_files(self):
        mask = [("JPG Images","*.jpg")]
        fadd = filedialog.askopenfilenames(parent=root, filetypes=mask, title='Choose your images')

        global filez
        #Check if filez is defined
        try:
            #add filez and fadd
            filez = filez + fadd
        except NameError:
            filez = fadd

        #check if empty
        if filez != None:
            self.reset_listbox()    #Reset List
        
        self.set_default()   #Setting Default Settings
        self.reset_btn()   #Reset Button

    def move_up(self):
        listbox = self.builder.get_object("List")
        active = int(listbox.curselection()[0])  #Get selected item
        old_active = listbox.curselection()

        #Change filez
        global filez
        listx = list(filez)
        listx.insert(active - 1, listx.pop(active))
        filez = tuple(listx)

        self.reset_listbox()    #Reset List
        listbox.activate(old_active)    #reactivate
        
        self.reset_btn()   #Reset Button


    def move_down(self):
        listbox = self.builder.get_object("List")
        active = int(listbox.curselection()[0]) #Get selected item
        old_active = listbox.curselection()

        #Change filez
        global filez
        listx = list(filez)
        listx.insert(active + 1, listx.pop(active))
        filez = tuple(listx)

        self.reset_listbox()    #Reset List
        listbox.activate(old_active)    #reactivate
        
        self.reset_btn()   #Reset Button

    def file_delete(self):
        listbox = self.builder.get_object("List")
        active = int(listbox.curselection()[0])  #Get selected item

        #Change filez
        global filez
        listx = list(filez)
        del listx[active]
        filez = tuple(listx)

        self.reset_listbox()    #Reset List
        self.reset_btn()   #Reset Button
        
    def open_locations(self):
        mask = [("Portable Document Format","*.pdf")]  
        global fout
        fout = filedialog.askdirectory(title='Choose a location to save the PDF')
        if fout != None:
            self.builder.get_variable("fout_loc").set(str(fout))

    def same_locations(self):
        if filez != None:
            global fout
            fout = os.path.dirname(filez[0])
            self.builder.get_variable("fout_loc").set(str(fout))
    
    def convert(self):

        #Loading
        self.builder.get_object("convert_btn").config(text='Converting...', background='#fffda8')
        
        #Get Setting Size
        papersize = self.builder.get_variable("paper_size").get()
        paperori = self.builder.get_variable("paper_orien").get()
        papermargin = self.builder.get_variable("paper_marge").get()
        paperscale = self.builder.get_variable("paper_scale").get()
        path = os.path.exists(self.builder.get_variable("fout_loc").get())

        #Dictionary
        pdf_size = {'LP': {'w': 8.5, 'h': 11}, 'LL': {'w': 11, 'h': 8.5}, 'AP': {'w': 8.27, 'h': 11.69}, 'AL': {'w': 11.69, 'h': 8.27}}
        
        if papersize != "" and paperori != "" and papermargin != "" and paperscale != "" and path == True:
                
            #Convertion
            if paperori == "Portrait":
                ori_s = "P"
            else:
                ori_s = "L"
            
            if papersize == "Letter":
                sizecode = "L"
            elif papersize == "A4":
                sizecode = "A"

            #margin
            if papermargin == "Small_Margin":
                marge = 0.975
            elif papermargin == "Big_Margin":
                marge = 0.95
            else:
                marge = 1

            pdf = FPDF(ori_s, 'in', papersize)
            for image in filez:
                #Check Image Size
                if paperscale == "Stretch":
                    pxcale = pdf_size[sizecode + ori_s]["w"] * marge
                    pycale = pdf_size[sizecode + ori_s]["h"] * marge
                else:
                    im = Image.open(image)
                    img_width, img_height = im.size

                    #Calculate dpi
                    img_dpi_w = img_width / pdf_size[sizecode + ori_s]["w"]
                    img_dpi_h = img_height / pdf_size[sizecode + ori_s]["h"]

                    if img_width >= img_height:

                        #Set DPI
                        img_width = img_width / img_dpi_w
                        img_height = img_height / img_dpi_w

                        #Check Orientation
                        if ori_s == "P":
                            pxcale = pdf_size[sizecode + ori_s]["w"] * marge
                            pycale = ( img_width / pxcale ) * img_height * marge
                        else:
                            pxcale = pdf_size[sizecode + ori_s]["w"] * marge
                            pycale = ( img_width / pxcale ) * img_height * marge
                    else:

                        #Set DPI
                        img_width = img_width / img_dpi_h
                        img_height = img_height / img_dpi_h
                        
                        #Check Orientation
                        if ori_s == "L":
                            pycale = pdf_size[sizecode + ori_s]["h"] * marge
                            pxcale = ( img_height / pycale ) * img_width * marge
                        else:
                            pycale = pdf_size[sizecode + ori_s]["h"] * marge 
                            pxcale = ( img_height / pycale ) * img_width * marge
                
                pdf.add_page()
                #Image Settings
                pdf.image(image, 
                x = 0 + (pdf_size[sizecode + ori_s]["w"] - pdf_size[sizecode + ori_s]["w"] * marge) / 2, 
                y = 0 + (pdf_size[sizecode + ori_s]["h"] - pdf_size[sizecode + ori_s]["h"] * marge) / 2, 
                w = pxcale, 
                h = pycale, 
                type = 'JPG')
                
            pdf.output(str(fout) + "/" + str(self.builder.get_variable("fout_name").get()) + ".pdf", "F")
            
            self.builder.get_object("convert_btn").config(text='File Converted!', background='#a9feab')     #Message
            playsound(self.resource_path("message_tone.mp3"))   #Sound FX
            

        elif path == False:
            messagebox.showerror("No Output Location", "Please pick a valid output location")
            self.reset_btn()   #Reset Button
        else:
            messagebox.showerror("No Settings", "Please pick the settings first")
            self.reset_btn()   #Reset Button
            


root = tk.Tk()
app = Application(root)
root.title('JPG2PDF v1.5 beta     by Sam F')
root.iconbitmap(Application.resource_path(Application,"pdf_icon.ico"))
root.resizable(False, False)

root.mainloop()