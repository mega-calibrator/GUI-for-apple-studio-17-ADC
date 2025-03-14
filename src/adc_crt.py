from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askokcancel
from pywinusb import hid
from monitorcontrol import get_monitors
import sv_ttk

def main():
    window = Tk()
    window.title("Control for ADC CRT")
    window.tk.call('tk', 'scaling', 1)
    s = ttk.Style()
    usbfilter = hid.HidDeviceFilter(vendor_id = 0x05AC, product_id = 0x9213)
    vsync_usage = hid.get_full_usage_id(0x82, 0xAE)
    degauss_usage = hid.get_full_usage_id(0x82, 0x01)
    resizable = False
    vsync = 0
    if window.winfo_screenheight() < 769 or window.winfo_screenwidth() < 1025:
        lowres = True
        tabfont = 10
        buttonfont = 10
        sliderlength = 256
        entryfont = 10
        padsmall = 0
        padmedium = 0
        padlarge = 0
        padXL = 0
        rightarrowimg = PhotoImage(data=r"iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAP0lEQVQYlY3PMQ6AIBQE0RePQW0sjOH+jachFMRLUNDykakn2VkGCS8uATca6krK+HalghOOyJzxrCZ+I8ObHahHDJ/5N0/LAAAAAElFTkSuQmCC")
        leftarrowimg = PhotoImage(data=r"iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAQ0lEQVQYlY3OMQrAIABD0YfHKJ2KYwfvD56mo3gFcRWrYKaQH0L4KyLjXjARHwreHaxIM3x2MAy+LbKzleOTYynjgg72vw2fCIi97QAAAABJRU5ErkJggg==")
    else:
        lowres = False
        tabfont = 18
        buttonfont = 16
        sliderlength = 320
        entryfont = 15
        padsmall = 2
        padmedium = 4
        padlarge = 8
        padXL = 12
        rightarrowimg = PhotoImage(data=r"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAfklEQVQ4jbXTQQrCMBRF0SClCy3ifqSIuAAHIsUV6unAgjEUm6/2TZN74f38pFQEHXpsyrPFYIu7Z44hCRLO3hOWNLjOSEI1GgyF5BCVtLitIen/IdnnkpoJl3ce61f46SU+7MJy3Qm+fAvPrfKpCs4kO6/PFIMzSTcNrAoeAV5STb5AuWlOAAAAAElFTkSuQmCC")
        leftarrowimg = PhotoImage(data=r"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAc0lEQVQ4jb2SQQqAQAgAl4joqRHRNzrE0ksiIqK/dZmOkUjpFnkTnUHFEAwBBCACtaVfgwfOaN/AACOQDE9AkQovHjgKeP0N7r1wJvJd5LnS8zhFJ6bYgNIr0VZxS9KOKSTyF+YvJLZXvpE0dvoqiUAlawf0GU2w8QV3KQAAAABJRU5ErkJggg==")
    window.configure(padx=padlarge, pady=padlarge)

    vcp_codes = {
        "0x12": "Contrast",
        "0x20": "H Phase",
        "0x22": "H Size",
        "0x30": "V Phase",
        "0x32": "V Size",
        "0x24": "H Pin",
        "0x42": "H Keystone",
        "0x40": "H Key Balance",
        "0x44": "Rotation",
        "0x28": "H Stat conv",
        "0x38": "V Stat conv",
    }
    vcp_code_max = {
        "0x12": 97,
        "0x20": 127,
        "0x22": 97,
        "0x30": 127,
        "0x32": 127,
        "0x24": 127,
        "0x42": 127,
        "0x40": 127,
        "0x44": 255,
        "0x28": 255,
        "0x38": 255,
    }

    class dong_button():
        def __init__(self, parent, monitor):
            self.parent = parent
            self.monitorobj = monitor

        def make_button(self):
            def dong():
                try:
                    self.monitorobj.open()
                    for report in self.monitorobj.find_feature_reports():
                        if degauss_usage in report:
                            report[degauss_usage] = 1
                            report.send()
                finally:
                    self.monitorobj.close()
            self.button = ttk.Button(self.parent, text="Degauss", command=dong, takefocus=False)
            self.button.pack(side=LEFT, expand=YES, padx=padmedium)

    class code_refresher():
        def __init__(self, parent, adjustersdict, vsyncobj, displayname):
            self.vsyncobj = vsyncobj
            self.parent = parent
            self.adjustersdict = adjustersdict
            self.displayname = displayname

        def make_button(self):
            def refresh():
                print("\nNow refreshing values from monitor....")
                for code in self.adjustersdict.keys():
                    try:
                        self.adjustersdict[code].monitorobj.open()
                        target_usage = hid.get_full_usage_id(0x82, int(code, 16))
                        for report in self.adjustersdict[code].monitorobj.find_feature_reports():
                            if target_usage in report:
                                report.get()
                                new_value = list(report[target_usage])[0]
                                self.adjustersdict[code].slider.set(new_value)
                    finally:
                        self.adjustersdict[code].monitorobj.close()
                try:
                    self.adjustersdict["0x12"].monitorobj.open()
                    for report in self.adjustersdict["0x12"].monitorobj.find_feature_reports():
                        if vsync_usage in report:
                            report.get()
                            vsynclabel.configure(text="V. Rate: "+str(report[vsync_usage].get_value()/100)+" Hz") 
                finally:
                    adc_crt.close()
                showinfo(title="Notice", message="Values refreshed for "+self.displayname)
            self.button = ttk.Button(self.parent, text="Read", command=refresh, takefocus=False)
            self.button.pack(side=LEFT, expand=YES, padx=padmedium)

    class code_applier:
        def __init__(self, parent, monitor, displayname):
            self.parent = parent
            self.monitorobj = monitor
            self.displayname = displayname

        def make_button(self):    
            def apply():
                try:
                    self.monitorobj.open()
                    for report in self.monitorobj.find_feature_reports():
                        if hid.get_full_usage_id(0x82, 0xB0) in report:
                            report[hid.get_full_usage_id(0x82, 0xB0)] = 1
                            report.send()
                finally:
                    self.monitorobj.close()
                    showinfo(title='Notice', message='Values applied to '+self.displayname)

            self.button = ttk.Button(self.parent, text="Write", command=apply, takefocus=False)
            self.button.pack(side=LEFT, expand=YES, padx=padmedium)

    class power_toggles:
        def __init__(self, parent, monitor, index):
            self.parent = parent
            self.monitorobj = monitor
            self.index = index
            self.radiovar = IntVar(value=self.monitorobj.vcp.get_vcp_feature(code=int("0xD6", 16))[0])
            
        def make_buttons(self):
            def poweroff():
                with self.monitorobj:
                    while True:
                        try:
                            self.monitorobj.vcp.set_vcp_feature(code=int("0xD6", 16), value=4)
                        except:
                            pass
                        else:
                            break

            def poweron():
                with self.monitorobj:
                    while True:
                        try:
                            self.monitorobj.vcp.set_vcp_feature(code=int("0xD6", 16), value=1)
                        except:
                            pass
                        else:
                            break
            
            powerlabel = ttk.Label(self.parent, padding=padmedium, text="Monitor "+str(i))
            powerlabel.grid(row=self.index, column=0)
            for option in range(2):
                if option == 1:
                    powradio = ttk.Radiobutton(self.parent, text="off", value=4, variable=self.radiovar, command=poweroff)
                    powradio.grid(row=self.index, column=1)
                else:
                    powradio = ttk.Radiobutton(self.parent, text="on", value=1, variable=self.radiovar, command=poweron)
                    powradio.grid(row=self.index, column=2)

    class adjustment_box:
        def __init__(self, crtcodevalues, parent, monitor, code, index):
            self.codevalues = crtcodevalues
            self.parent = parent
            self.monitorobj = monitor
            self.code = code
            self.index = index
            self.usagecode = hid.get_full_usage_id(0x82, int(code, 16))
            self.boxvalue = IntVar(value=self.codevalues[0])
            self.label = ttk.Label(self.parent, text=vcp_codes[self.code])
            self.label.grid(row=self.index, column=3, padx=padlarge, sticky=W)

        def new_sliderbox(self):
            def field_entered(event):
                newentry = self.boxvalue.get()
                if int(newentry) > 255:
                    self.slider.set(255)
                else:
                    self.slider.set(int(newentry))

            def slider_changed(value):
                if not self.monitorobj.is_opened():
                    self.boxvalue.set(int(float(value)))
                    try:
                        self.monitorobj.open()
                        for report in self.monitorobj.find_feature_reports():
                            if self.usagecode in report:
                                report[self.usagecode] = [self.boxvalue.get(), 0] 
                                report.send()
                    finally:
                        self.monitorobj.close()

            def buttondown():
                self.downone.state(["disabled"])
                self.slider.set(self.boxvalue.get()-1)
                self.downone.state(["!disabled"])

            def buttonup():
                self.upone.state(["disabled"])
                self.slider.set(self.boxvalue.get()+1)
                self.upone.state(["!disabled"])

            self.slidervalue = ttk.Entry(self.parent, width=4, justify=CENTER, textvariable=self.boxvalue)
            self.slidervalue.bind("<Return>", field_entered)
            self.slidervalue.config(takefocus=0)
            self.downone = ttk.Button(self.parent, image=leftarrowimg, command=buttondown, takefocus=False)
            self.upone = ttk.Button(self.parent,image=rightarrowimg, command=buttonup, takefocus=False)
            print("Creating slider with value", self.boxvalue.get(), "for", vcp_codes[self.code])
            self.slider = ttk.Scale(self.parent, from_=0, to=self.codevalues[1], length=sliderlength, value=self.codevalues[0], command=slider_changed)
            self.slider.grid(row=self.index, column=4, padx=padXL)
            self.downone.grid(row=self.index, column=0, padx=padsmall, pady=padsmall)
            self.slidervalue.grid(row=self.index, column=1, padx=padmedium)
            self.upone.grid(row=self.index, column=2, padx=padsmall, pady=padsmall)


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
    print("\nThis is a test for apple M7768. Now detecting DDC capable monitors.....\n")
    progress.configure(maximum=(32))   

    adc_crt_devices = usbfilter.get_devices()
    if not adc_crt_devices:
        progress.stop()
        print("\nCannot connect to ADC monitor over USB...")
        showerror(title="Oh no.....", message="Sorry!\nUSB connection not found!")
        loading.destroy()
        window.destroy()
    else:
        main_notebook = ttk.Notebook(window, padding=4)
        main_notebook.pack(side=TOP)

        print("\nReading current values!")
        for i, adc_crt in enumerate(adc_crt_devices):
            progress.update()
            noteframe = ttk.Frame(main_notebook, padding=4, borderwidth=3)
            main_notebook.add(noteframe, text="ADC Monitor "+str(i+1))
            adjusterindex = 0
            adjustersdict = {}
            try:
                adc_crt.open()
                print(adc_crt, "\n")
                for code in vcp_codes.keys():
                    progress.update()
                    target_usage = hid.get_full_usage_id(0x82, int(code, 16))
                    for report in adc_crt.find_feature_reports():
                        if target_usage in report:
                            report.get()
                            codevalue = list(report[target_usage])[0]
                            coderange = [codevalue, vcp_code_max[code]]
                            adjuster = adjustment_box(coderange, noteframe, adc_crt, code, adjusterindex)
                            adjuster.new_sliderbox()
                            adjusterindex += 1
                            adjustersdict[code] = adjuster
            finally:
                adc_crt.close()
            try:
                adc_crt.open()
                for report in adc_crt.find_feature_reports():
                    if vsync_usage in report:
                        report.get()
                        vsync = report[vsync_usage].get_value()/100
                        print("\nV. refresh rate:", vsync, " Hz")
            finally:
                adc_crt.close()

            buttonframe = ttk.Frame(noteframe, borderwidth=2, relief=SUNKEN)
            buttonframe.grid(row=adjusterindex+1, column=0, columnspan=5, ipadx=padlarge, ipady=padlarge, pady=padXL)
            vsynclabel = ttk.Label(buttonframe, text="V. Rate: "+str(vsync)+"Hz")
            vsynclabel.pack(side=LEFT, padx=padXL)
            donger = dong_button(buttonframe, adc_crt)
            donger.make_button()
            refresher = code_refresher(buttonframe, adjustersdict, vsynclabel, "ADC Monitor "+str(i+1))
            refresher.make_button()
            applier = code_applier(buttonframe, adc_crt, "ADC Monitor "+str(i+1))
            applier.make_button()
            noteframe.columnconfigure(3, weight=1)

        radiobox = ttk.LabelFrame(window, text="Power", padding=padXL, borderwidth=2, relief=RAISED)
        radiobox.pack(side=TOP, pady=padlarge)
        print("\nAssembling power toggles")
        for i, monitor in enumerate(get_monitors()):
            with monitor:
                try:
                    monitor.get_vcp_capabilities()
                except:
                    progress.update()
                    try:
                        monitor.vcp.get_vcp_feature(code=int("0xD6", 16))
                    except:
                        progress.update()
                    else:
                        progress.update()
                        print("Monitor", i, "appears to be an M7768 CRT!")
                        toggles = power_toggles(radiobox, monitor, i)
                        toggles.make_buttons()

        loading.destroy()
        if lowres:
            print("\nLow resolution detected on main monitor, activating small UI mode...")
            s.theme_use("alt")
            s.configure('TNotebook.Tab', font=("",tabfont))
            s.configure('TLabel', font=("",tabfont))
            s.configure('TButton', font=("",buttonfont))
            s.configure('TRadiobutton', font=("",buttonfont))
        else:
            sv_ttk.set_theme("dark")
            s.configure('TNotebook.Tab', font=("", tabfont, "bold"), padding=[20,0])
            s.configure('TLabel', font=("", entryfont, "bold"))
            s.configure('TButton', font=("", buttonfont, "bold"))
            s.configure('TRadiobutton', font=("", buttonfont, "bold"))
        print("\nReady set go!")
        window.deiconify()
        window.resizable(False, resizable)
        window.focus_force()
        window.protocol("WM_DELETE_WINDOW", lambda: window.destroy() if askokcancel("Warning", "Do you want to quit?") else False)
    window.mainloop()