from __future__ import absolute_import

try:
    # for Python2
    import Tkinter as tk
    import ttk
except ImportError:
    # for Python3
    import tkinter as tk
    from tkinter import ttk
import config as EDMCConfig
from igmconfig import IGMConfig
import ttkHyperlinkLabel

class ToggledFrame(tk.Frame):

    def __init__(self, parent, label, status, show, *args, **options):
        theme=EDMCConfig.getint('theme')
        if(theme)
            conf = IGMConfig(config_file='config/igm_alt_config.v3.ini', user_config_file=['config/user_igm_alt_config.v3.ini', 'config/user_igm_alt_config.v2.ini'])
        else
            conf = IGMConfig(config_file='config/igm_light_config.v3.ini', user_config_file=['config/user_igm_light_config.v3.ini', 'config/user_igm_light_config.v2.ini'])
        tk.Frame.__init__(self, parent, *args, **options)
        fg = conf.rgb("status", "body")
        bg = conf.rgb("status", "fill")
        self.tk_setPalette(background=bg, foreground=fg, activeBackground=conf.rgb("status", "active_bg"), activeForeground=conf.rgb("status", "active_fg"))

        self.show = show
        
        self.grid(sticky="nsew")
        self.status_frame = tk.Frame(self)
        self.status_frame.grid(row=0, column=0, sticky="ew")
        self.grid_columnconfigure(0, weight=1)
        
        self.sub_frame = tk.Frame(self, relief="flat", borderwidth=0)
        self.sub_frame.grid(row=1, column=0, sticky="nsew")
        
        separator = ttk.Separator(self.status_frame, orient=tk.HORIZONTAL)
        separator.grid(row=0, columnspan=3, sticky="ew")
        self.status_frame.grid_rowconfigure(0, weight=1)

        label = tk.Label(self.status_frame, text=label, foreground=conf.rgb("status", "label"))
        label.grid(sticky="w", row=1, column=0)
        self.status_ui = ttkHyperlinkLabel.HyperlinkLabel(self.status_frame, textvariable=status, foreground=fg, background=bg)
        self.status_ui.grid(sticky="w", row=1, column=1)
        
        self.toggle_button = tk.Checkbutton(self.status_frame, width=2, text='+', command=self.toggle,
                                            variable=self.show, foreground=conf.rgb("status", "check"))
        self.toggle_button.grid(sticky="e", row=1, column=2)
        self.status_frame.grid_columnconfigure(2, weight=1)


    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.grid(row=1, column=0, sticky="nsew")
            self.sub_frame.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(1,weight=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.grid_forget()
            self.grid_rowconfigure(0,weight=1)
            self.toggle_button.configure(text='+')

class EDRTogglingPanel(ToggledFrame):
    def __init__(self, status, show, parent=0):
        conf = IGMConfig(config_file='config/igm_alt_config.v3.ini', user_config_file=['config/user_igm_alt_config.v3.ini', 'config/user_igm_alt_config.v2.ini'])
        ToggledFrame.__init__(self, parent, label="EDR:", status=status, show=show)
        self.grid(sticky="nswe")
        self.output = tk.Text(self.sub_frame, width=conf.len("general", "body"), height=conf.body_rows("general"),
                                                background=conf.rgb("general", "fill"), foreground=conf.rgb("general", "body"),
                                                wrap=tk.WORD, padx=4, borderwidth=0)
        self.output.grid(row=0, column=0, sticky="nswe")

        self.__configure_tags(conf)
        self.toggle()

    def nolink(self):
        self.status_ui.url = None
        self.status_ui.underline = False

    def link(self, url):
        self.status_ui.underline = True
        self.status_ui.url = url

    def sitrep(self, header, body):
        self.__push_message("sitrep", header, body)

    def intel(self, header, body):
        self.__push_message("intel", header, body)

    def warning(self, header, body):
        self.__push_message("warning", header, body)
    
    def notify(self, header, body):
        self.__push_message("notice", header, body)
    
    def help(self, header, body):
        self.__push_message("help", header, body)

    def __push_message(self, kind, header, body):
        self.output.insert(1.0,u"\n", ("body_"+kind))
        body.reverse()
        for line in body:
            self.output.insert(1.0, line, ("body_"+kind))
            self.output.insert(1.0, u"\n", ("body_"+kind))
        self.output.insert(1.0, header, ("header_"+kind))
        self.output.insert(1.0, "\n", ("header_"+kind))
    
    def clear(self):
        self.output.delete(1.0, tk.END)

    def __configure_tags(self, conf):
        kinds = ["sitrep", "intel", "warning", "notice", "help"]
        for kind in kinds:
            self.output.tag_configure("header_"+kind, foreground=conf.rgb(kind, "header"))
            self.output.tag_configure("body_"+kind, foreground=conf.rgb(kind, "body"))
        
