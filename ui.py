from tkinter import END, DISABLED, NORMAL, filedialog, messagebox
from PIL import Image, ImageTk
import customtkinter
import random
import os
from urllib.request import urlopen
from io import BytesIO


class UIBuilder:
    """Builds the UI and exposes widget references on the provided app instance.

    This mirrors the structure from the original `main.py` but keeps construction
    in a separate module so the app logic can remain cleaner.
    """

    def __init__(self, app):
        self.app = app

    def build_frames(self):
        a = self.app
        a.frame_1 = customtkinter.CTkFrame(master=a, width=830, height=250)
        a.frame_1.place(x=10, y=10)

        a.frame_2 = customtkinter.CTkFrame(master=a, width=830, height=290)
        a.frame_2.place(x=10, y=380)

        a.mode_switch = customtkinter.CTkSwitch(master=a, text="Mode", text_color=("black", "white"),
                                               command=a.mode, font=(None, 11, "bold"))
        a.mode_switch.place(x=10, y=675)

        self.build_frame1_widgets()
        # frame_2 children are created lazily by the app when first needed

    def build_frame1_widgets(self):
        a = self.app
        a.bg_color = "#c71c72"
        a.hoverr_color = "#660d3a"
        a.border_colorr = "#383838"

        a.search_entry = customtkinter.CTkEntry(master=a.frame_1, placeholder_text="URL", fg_color=("white"),
                                               text_color=("black"), height=35, font=(None, 15), width=500,
                                               border_width=0, border_color="#c71c72")
        a.search_entry.place(x=30, y=30)

        a.paste_btn = customtkinter.CTkButton(master=a.frame_1, text="Paste", height=35, fg_color=(a.bg_color),
                                             font=(None, 13,), border_width=0, border_color=a.border_colorr,
                                             hover_color=a.hoverr_color, command=a.paste_fnc)
        a.paste_btn.place(x=30, y=68, relwidth=0.105)

        a.search_btn = customtkinter.CTkButton(master=a.frame_1, text="Search", height=35,
                                              fg_color=(a.bg_color), font=(None, 11,), border_width=0,
                                              border_color="#c71c72", hover_color=a.hoverr_color,
                                              command=a.youtubefetchthread)
        a.search_btn.place(x=535, y=30, relwidth=0.1)

        # quality buttons (state toggled after fetch)
        a.btn_1080 = customtkinter.CTkButton(master=a.frame_1, text="1080p", text_color_disabled="black",
                                            state=DISABLED, height=35, fg_color=("red"),
                                            font=(None, 11,), corner_radius=16, border_width=0,
                                            border_color=a.border_colorr, hover_color=a.hoverr_color,
                                            command=a.t1080)
        a.btn_1080.place(x=30, y=200, relwidth=0.1)

        a.btn_720 = customtkinter.CTkButton(master=a.frame_1, text="720p", text_color_disabled="black",
                                           state=DISABLED, height=35, fg_color=("red"),
                                           font=(None, 11,), corner_radius=16, border_width=0,
                                           border_color=a.border_colorr, hover_color=a.hoverr_color,
                                           command=a.t720)
        a.btn_720.place(x=120, y=200, relwidth=0.1)

        a.btn_480 = customtkinter.CTkButton(master=a.frame_1, text="480p", text_color_disabled="black",
                                           state=DISABLED, height=35, fg_color=("red"),
                                           font=(None, 11,), corner_radius=16, border_width=0,
                                           border_color=a.border_colorr, hover_color=a.hoverr_color,
                                           command=a.t480)
        a.btn_480.place(x=210, y=200, relwidth=0.1)

        a.btn_360 = customtkinter.CTkButton(master=a.frame_1, text="360p", text_color_disabled="black",
                                           state=DISABLED, height=35, fg_color=("red"),
                                           font=(None, 11,), corner_radius=16, border_width=0,
                                           border_color=a.border_colorr, hover_color=a.hoverr_color,
                                           command=a.t360)
        a.btn_360.place(x=300, y=200, relwidth=0.1)

        a.btn_240 = customtkinter.CTkButton(master=a.frame_1, text="240p", text_color_disabled="black",
                                           state=DISABLED, height=35, fg_color=("red"),
                                           font=(None, 11,), corner_radius=16, border_width=0,
                                           border_color=a.border_colorr, hover_color=a.hoverr_color,
                                           command=a.t240)
        a.btn_240.place(x=390, y=200, relwidth=0.1)

        a.btn_144 = customtkinter.CTkButton(master=a.frame_1, text="144p", text_color_disabled="black",
                                            state=DISABLED, height=35, fg_color=("red"),
                                            font=(None, 11,), corner_radius=16, border_width=0,
                                            border_color=a.border_colorr, hover_color=a.hoverr_color,
                                            command=a.t144)
        a.btn_144.place(x=480, y=200, relwidth=0.105)

        a.btn_160 = customtkinter.CTkButton(master=a.frame_1, text="Audio", text_color_disabled="black",
                                           height=35, fg_color=("red"), state=DISABLED, font=(None, 11,),
                                           corner_radius=16, border_width=0, border_color=a.border_colorr,
                                           hover_color=a.hoverr_color, command=a.t160kps)
        a.btn_160.place(x=570, y=200, relwidth=0.105)

        a.thumbnail_lab = customtkinter.CTkLabel(master=a.frame_1, text="", fg_color=("#383838"), height=85,
                                                 width=150)

        a.vid_title = customtkinter.CTkLabel(master=a.frame_1, text="", font=(None, 11, "bold"))
        a.vid_title.place(x=250, y=109)

        a.vid_length = customtkinter.CTkLabel(master=a.frame_1, text="", font=(None, 11, "bold"))
        a.vid_length.place(x=250, y=130)

        a.vid_author = customtkinter.CTkLabel(master=a.frame_1, text="", font=(None, 11, "bold"))
        a.vid_author.place(x=250, y=151)

        a.vid_views = customtkinter.CTkLabel(master=a.frame_1, text="", font=(None, 11, "bold"))
        a.vid_views.place(x=250, y=172)

        # a small display image (original project used an image file)
        try:
            _img = Image.open("proxytube1.png")
            _img = _img.resize((400, 120), Image.Resampling.LANCZOS)
            a.text_img = customtkinter.CTkImage(light_image=_img, dark_image=_img, size=(400, 120))
            a.size_display = customtkinter.CTkLabel(master=a, text='', image=a.text_img, font=(None, 11, "bold"))
            a.size_display.place(x=170, y=260)
        except Exception:
            # ignore missing asset
            pass

    def show_thumbnail(self, thumbnail_url):
        a = self.app
        try:
            data = urlopen(thumbnail_url).read()
            img = Image.open(BytesIO(data))
            img = img.resize((200, 85), Image.Resampling.LANCZOS)
            tkimg = ImageTk.PhotoImage(img)
            a.thumbnail_lab.configure(image=tkimg)
            a.thumbnail_lab.image = tkimg
            a.thumbnail_lab.place(x=30, y=109)
        except Exception:
            # show no thumbnail if failed
            pass

    def notify_no_room(self):
        t = customtkinter.CTkToplevel(master=self.app)
        t.title("Error")
        l = customtkinter.CTkLabel(master=t, text="No room available for download!!!", font=(None, 13, "bold"))
        l.place(relx=0.13, rely=0.37)
        t.geometry("350x200")

    def ask_save_dir(self):
        return filedialog.askdirectory()

    def ask_confirm_download(self, size_in_bytes):
        mb = size_in_bytes / 1048576
        return messagebox.askyesno("Do You Want To Download", f"File Size: {mb:0.2f} MegaBytes")

    def set_button_state(self, widget, enabled):
        widget.configure(state=NORMAL if enabled else DISABLED, fg_color=(self.app.bg_color) if enabled else ("red"))

