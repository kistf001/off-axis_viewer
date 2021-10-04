from tkinter import *
from tkinter.ttk import *
import viewport

class MyFrame(Frame):

    def eye_gap(self,asddasd) :
        self.gaq = float(asddasd)
        viewport.adfadf[0] = self.pos_x + self.gaq
        viewport.adfadf[3] = self.pos_x - self.gaq

    def posx(self,asddasd) :
        self.pos_x = float(asddasd)
        viewport.adfadf[0] = self.pos_x + self.gaq
        viewport.adfadf[3] = self.pos_x - self.gaq


    def light_ambient (self,asddasd) :
        viewport.gui_ambient= (viewport.pyrr.Vector3(
            [float(asddasd),float(asddasd),float(asddasd)]))
    def light_diffuse (self,asddasd) :
        viewport.gui_diffuse= (viewport.pyrr.Vector3(
            [float(asddasd),float(asddasd),float(asddasd)]))
    def light_specular(self,asddasd) :
        viewport.gui_specular= (viewport.pyrr.Vector3(
            [float(asddasd),float(asddasd),float(asddasd)]))
    def light_position(self,asddasd) :
        viewport.gui_position=(viewport.pyrr.Vector3(
            [float(asddasd),float(asddasd),4.0]))

    
    def __init__(self, master):
        Frame.__init__(self, master)

        self.gaq = 0
        self.pos_x = 0
        self.pos_y = 0

        self.master = master
        self.master.title("고객 입력")
        self.pack(fill=BOTH, expand=True)
 
        # 성명
 
        frame5 = Frame(self)
        frame5.pack(fill=X)
        w = Scale(frame5, from_=0, to=1000, command = self.eye_gap)
        w.pack()
        
        eye_width = Scale(frame5, from_=-1000, to=1000, command = self.posx)
        eye_width.pack()
        
        lblName_ambient  = Label(frame5, text="ambient ", width=10)
        lblName_diffuse  = Label(frame5, text="diffuse ", width=10)
        lblName_specular = Label(frame5, text="specular", width=10)
        lblName_position = Label(frame5, text="position", width=10)
        _ambient  = Scale(frame5, from_=0, to=1, command = self.light_ambient )
        _diffuse  = Scale(frame5, from_=0, to=1, command = self.light_diffuse )
        _specular = Scale(frame5, from_=0, to=1, command = self.light_specular)
        _position = Scale(frame5, from_=0, to=1, command = self.light_position)
        lblName_ambient .pack(fill=X)
        _ambient .pack()
        lblName_diffuse .pack(fill=X)
        _diffuse .pack()
        lblName_specular.pack(fill=X)
        _specular.pack()
        lblName_position.pack(fill=X)
        _position.pack()

        
 
 
def main():
    root = Tk()
    root.geometry("400x350+100+100")
    app = MyFrame(root)
    root.mainloop()