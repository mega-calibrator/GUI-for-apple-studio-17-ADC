from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, askokcancel
from monitorcontrol import get_monitors

def main():
    window = Tk()
    window.title("DDC/CI for CRT")
    window.tk.call('tk', 'scaling', 1)
    s = ttk.Style()
    lowres = True
    tabfont = 10
    buttonfont = 10
    sliderlength = 256
    entryfont = 10
    padsmall = 0
    padmedium = 0
    padlarge = 0
    padXL = 0
    window.configure(padx=padlarge, pady=padlarge)

    class adjustment_box:
        def __init__(self, parent, monitor):
            self.parent = parent
            self.monitorobj = monitor
            self.boxvalue = IntVar()
            self.label = ttk.Label(self.parent, text="Power Mode")
            self.label.grid(row=0, column=3, padx=padlarge, sticky=W)

        def new_radiobutton(self):
            self.boxvalue.set(self.monitorobj.vcp.get_vcp_feature(code=int("0xD6", 16))[0])
            self.radiobox = ttk.Frame(self.parent)
            print("Creating buttons for power mode")
            self.radiobox.grid(row=0, column=4, sticky=EW, padx=padXL)
            def poweron():
                with self.monitorobj:
                    while True:
                        try:
                            self.monitorobj.vcp.set_vcp_feature(code=int("0xD6", 16), value=4)
                        except:
                            pass
                        else:
                            break

            def poweroff():
                with self.monitorobj:
                    while True:
                        try:
                            self.monitorobj.vcp.set_vcp_feature(code=int("0xD6", 16), value=1)
                        except:
                            pass
                        else:
                            break

            for option in range(1, 3, 1):
                if option == 1:
                    self.radio = ttk.Radiobutton(self.radiobox, text="on", value=1, variable=self.boxvalue, command=poweroff)
                else:
                    self.radio = ttk.Radiobutton(self.radiobox, text="off", value=4, variable=self.boxvalue, command=poweron)
                self.radio.pack(side=LEFT)

    monitors = get_monitors()
    monitornum = len(monitors)
    loading = Toplevel()
    loading.geometry("320x180")
    loading.title("Loading")
    loading.resizable(False, False)
    loading.protocol("WM_DELETE_WINDOW", False)
    progress = ttk.Progressbar(loading, length=256, maximum=512)
    progress.start()
    progress.pack(anchor=CENTER, expand=YES)
    window.withdraw()
    progress.update()
    print("This is a test for apple M7768. Now detecting monitors.....\n")
    print(str(monitornum).strip(), "monitors detected!\n")
    badmonitors = []
    for i, monitor in enumerate(get_monitors()):
        with monitor:
            print(i)
            try:
                monitor.get_vcp_capabilities()
            except:
                try:
                    monitor.vcp.get_vcp_feature(code=int("0xD6", 16))
                except:
                    badmonitors.append(i)
                    print("Monitor", i,"unsupported...")
                else:
                    print("Monitor", i, "may be an M7768 CRT!")
            else:
                try:
                    monitor.vcp.get_vcp_feature(code=int("0xD6", 16))
                except:
                    badmonitors.append(i)
                    print("Monitor", i,"supports DDC without VCP D6.")
                else:
                    print("Monitor", i, "supports DDC normally!")

    progress.configure(maximum=(8))                    
    progress.update()
    resizable = False
    if monitornum == len(badmonitors):
        progress.stop()
        print("\nNo compatible monitors found.....")
        showerror(title="Oh no.....", message="Sorry!\nNo ADC CRT displays found!")
        loading.destroy()
        window.destroy()
    else:
        if len(badmonitors) == 0:
            print("\nAll monitors compatible!")
        else:
            print("\nIncompatible monitors:", badmonitors)

        main_notebook = ttk.Notebook(window, padding=4)
        main_notebook.pack()
        print("\nStarting code detection!")
        for i, monitor in enumerate(monitors):
            print("\nNext monitor:", str(i), "compatible:", str(i not in badmonitors).lower())
            if i not in badmonitors:
                progress.update()
                noteframe = ttk.Frame(main_notebook, padding=4, borderwidth=3)
                with monitor:
                    main_notebook.add(noteframe, text="Monitor "+str(i+1))
                    adjuster = adjustment_box(noteframe, monitor)
                    adjuster.new_radiobutton()
                noteframe.columnconfigure(3, weight=1)
        s.theme_use("alt")
        s.configure('TNotebook.Tab', font=("",tabfont))
        s.configure('TLabel', font=("",tabfont))
        s.configure('TButton', font=("",buttonfont))
        s.configure('TRadiobutton', font=("",buttonfont))
        loading.destroy()
        print("\nReady set go!")
        window.deiconify()
        window.resizable(False, resizable)
        window.focus_force()
        window.protocol("WM_DELETE_WINDOW", lambda: window.destroy() if askokcancel("Warning", "Do you want to quit?") else False)
    window.mainloop()