from tkinter import *
from qlark_gui_class import ThreadedQlarkClient

class MyFirstGUI:
    def __init__(self, master):
        self.input_truthtable = []
        self.temp = []
        self.master = master

        self.initdict = dict()

        master.title("AI CIRCUIT DESIGN")

        self.label1 = Label(master, text="Select Bot")
        # self.label1.grid(row=0,column=0)


#------Column 0 ----------

        self.qlarksetup_button = Button(master, text="\nQlark\n", width= 20, command=self.qlarkgui)
        self.qlarksetup_button.grid(row=1,column=0)

        self.cvsrun_button = Button(master, text="\nLuca\n",width= 20, command=self.yeet)
        self.cvsrun_button.grid(row=2,column=0)

        self.close_button = Button(master, text="     Close     ", command=master.quit)
        self.close_button.grid(row=3,column=0)




    def qlarkgui(self):
        from qlark_gui_class import QlarkGui

        root = Tk()

        client = ThreadedQlarkClient(root)
        root.mainloop()



        # rootq = Tk(className='Python Examples - Window Size')
        # qlark_gui = QlarkGui(rootq)
        # print("huh")


        #if error return maybe display in window

    def yeet(self):
        print("Will can figure this part out")
        #if error return maybe display in window


