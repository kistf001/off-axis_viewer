from tkinter import *
from tkinter.ttk import *
import viewport
import tcp_client
import struct
import pickle
import os

class MyFrame(Frame):

    def config_data_load(self):

        self.my_list = [0.0,0.3,0.7,0.7]
        
        if(os.path.isfile("data.pickle")):
            # Load pickle
            with open("data.pickle","rb") as fr:
                self.my_list = pickle.load(fr)
                print(self.my_list)
            fr.close()
        
        else:
            ## Save pickle
            with open("data.pickle","wb") as fw:
                pickle.dump(self.my_list, fw)
            fw.close()

        return self.my_list
    def config_data_save(self):

        ## Save pickle
        with open("data.pickle","wb") as fw:
            pickle.dump(self.my_list, fw)
        fw.close()
        
        print("save")
    def config_data_2_opengl(self,AAAA):
        self.light_ambient (AAAA[0])
        self.light_diffuse (AAAA[1])
        self.light_specular(AAAA[2])
        self.light_position(AAAA[3])

    def okClick0(self, event):
        self.adfad[self.asdsw][0], self.adfad[self.asdsw][1] = event.x, event.y
        self.asdsw = (self.asdsw+1) & 0b11
        print(self.adfad)
    def okClick2(self, event):
        tcp_client.SEND_INIT_POINTS_TO_CAMERA(
            struct.pack( '!llllllll', 
                self.adfad[0][0],self.adfad[0][1],
                self.adfad[1][0],self.adfad[1][1],
                self.adfad[2][0],self.adfad[2][1],
                self.adfad[3][0],self.adfad[3][1]
            )
        )
        print("EVENT_MBUTTONDOWN", self.adfad)

    def eye_gap(self,asddasd) :
        self.gaq = float(asddasd)
        viewport.adfadf[0] = self.pos_x + self.gaq
        viewport.adfadf[3] = self.pos_x - self.gaq

    def posx(self,asddasd) :
        self.pos_x = float(asddasd)
        viewport.adfadf[0] = self.pos_x + self.gaq
        viewport.adfadf[3] = self.pos_x - self.gaq

    def light_ambient (self,asddasd) :
        self.my_list[0] = asddasd
        viewport.gui_ambient= (viewport.pyrr.Vector3(
            [float(asddasd),float(asddasd),float(asddasd)]))
    def light_diffuse (self,asddasd) :
        self.my_list[1] = asddasd
        viewport.gui_diffuse= (viewport.pyrr.Vector3(
            [float(asddasd),float(asddasd),float(asddasd)]))
    def light_specular(self,asddasd) :
        self.my_list[2] = asddasd
        viewport.gui_specular= (viewport.pyrr.Vector3(
            [float(asddasd),float(asddasd),float(asddasd)]))
    def light_position(self,asddasd) :
        self.my_list[3] = asddasd
        viewport.gui_position=(viewport.pyrr.Vector3(
            [float(asddasd),float(asddasd),4.0]))

    def reload_image(self) :
        self.img = tcp_client.IMAGE_LOAD_FROM_CAMERA('RAW')
        self.img = PhotoImage(data=self.img)
        self.panel.configure(image=self.img)
        self.panel.image = self.img
    
    def __init__(self, master):
        Frame.__init__(self, master)

        data = self.config_data_load()
        self.config_data_2_opengl(data)

        # 포인트 정보 전송
        self.adfad = [[0,0],[0,0],[0,0],[0,0]]
        self.asdsw = 0

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
        
        Label(frame5, text="ambient ", width=10).pack(fill=X)
        aa0 = Scale(frame5, from_=0, to=0.7, command = self.light_ambient )
        aa0.pack()
        aa0.set(data[0])

        Label(frame5, text="diffuse ", width=10).pack(fill=X)
        aa1 = Scale(frame5, from_=0, to=0.7, command = self.light_diffuse )
        aa1.pack()
        aa1.set(data[1])

        Label(frame5, text="specular", width=10).pack(fill=X)
        aa2 = Scale(frame5, from_=0, to=0.7, command = self.light_specular)
        aa2.pack()
        aa2.set(data[2])

        Label(frame5, text="position", width=10).pack(fill=X)
        aa3 = Scale(frame5, from_=0, to=0.7, command = self.light_position)
        aa3.pack()
        aa3.set(data[3])

        Button(frame5, text = 'Button save', command = self.config_data_save).pack()
        Button(frame5, text = 'Button 1', command = self.reload_image).pack()

        self.qqqqq = tcp_client.IMAGE_LOAD_FROM_CAMERA('RAW')
        self.pytho = PhotoImage(data=self.qqqqq)
        self.panel = Label(self, image=self.pytho)
        self.panel.pack()

        self.panel.bind("<Button-1>", self.okClick0)
        self.panel.bind("<Button-3>", self.okClick2)
 
def main():
    root = Tk()
    root.geometry("700x800+100+100")
    app = MyFrame(root)
    root.mainloop()