from tkinter import *
from PIL import Image, ImageTk
from pytube import YouTube
import pyperclip as clipboard
# from pytube.cli import on_progress
from tkinter import messagebox
from urllib.request import urlopen
from tkinter import filedialog
import tkinter
import customtkinter
import random
import os, threading, base64
from io import BytesIO

customtkinter.set_appearance_mode("system")
audio= False
audio_proceed= False

class App(customtkinter.CTk, tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.once = 1
        self.download_int = 0
        self.runningtask = 0
        self.color_list = ["red", "green", "white", "pink", "yellow", "blue"]
        self.called = ""
        self.frame_1 = customtkinter.CTkFrame(master=self, width=830, height=250)
        self.frame_1.place(x=10, y=10)

        self.frame_2 = customtkinter.CTkFrame(master=self, width=830, height=290)
        self.frame_2.place(x=10, y=380)
        # Mode switch
        self.mode_switch = customtkinter.CTkSwitch(master=self, text="Mode", text_color=("black", "white"),
                                                   command=self.mode, font=(None, 11, "bold"))
        self.mode_switch.place(x=10, y=675)

    def frame_1_build(self):
        self.bg_color = "#c71c72"
        self.hoverr_color = "#660d3a"
        self.border_colorr = "#383838"
        self.down = 10
        self.new = "1"
        self.search_entry = customtkinter.CTkEntry(master=self.frame_1, placeholder_text="URL", fg_color=("white"),
                                                   text_color=("black"), height=35, font=(None, 15), width=500,
                                                   border_width=0, border_color="#c71c72", )
        self.search_entry.place(x=30, y=30)

        self.paste_btn = customtkinter.CTkButton(master=self.frame_1, text="Paste", height=35, fg_color=(self.bg_color),
                                                 font=(None, 13,), border_width=0, border_color=self.border_colorr,
                                                 hover_color=self.hoverr_color, command=self.paste_fnc)
        self.paste_btn.place(x=30, y=68, relwidth=0.105)

        self.search_btn = customtkinter.CTkButton(master=self.frame_1, text="Search", height=35,
                                                  fg_color=(self.bg_color), font=(None, 11,), border_width=0,
                                                  border_color="#c71c72", hover_color=self.hoverr_color,
                                                  command=self.youtubefetchthread)
        self.search_btn.place(x=535, y=30, relwidth=0.1)

        self.btn_1080 = customtkinter.CTkButton(master=self.frame_1, text="1080p", text_color_disabled="black",
                                                state=DISABLED, height=35, fg_color=("red"),
                                                font=(None, 11,), corner_radius=16, border_width=0,
                                                border_color=self.border_colorr, hover_color=self.hoverr_color,
                                                command=self.t1080)
        self.btn_1080.place(x=30, y=200, relwidth=0.1)

        self.btn_720 = customtkinter.CTkButton(master=self.frame_1, text="720p", text_color_disabled="black",
                                               state=DISABLED, height=35, fg_color=("red"),
                                               font=(None, 11,), corner_radius=16, border_width=0,
                                               border_color=self.border_colorr, hover_color=self.hoverr_color,
                                               command=self.t720)
        self.btn_720.place(x=120, y=200, relwidth=0.1)

        self.btn_480 = customtkinter.CTkButton(master=self.frame_1, text="480p", text_color_disabled="black",
                                               state=DISABLED, height=35, fg_color=("red"),
                                               font=(None, 11,), corner_radius=16, border_width=0,
                                               border_color=self.border_colorr, hover_color=self.hoverr_color,
                                               command=self.t480)
        self.btn_480.place(x=210, y=200, relwidth=0.1)

        self.btn_360 = customtkinter.CTkButton(master=self.frame_1, text="360p", text_color_disabled="black",
                                               state=DISABLED, height=35, fg_color=("red"),
                                               font=(None, 11,), corner_radius=16, border_width=0,
                                               border_color=self.border_colorr, hover_color=self.hoverr_color,
                                               command=self.t360)
        self.btn_360.place(x=300, y=200, relwidth=0.1)

        self.btn_240 = customtkinter.CTkButton(master=self.frame_1, text="240p", text_color_disabled="black",
                                               state=DISABLED, height=35, fg_color=("red"),
                                               font=(None, 11,), corner_radius=16, border_width=0,
                                               border_color=self.border_colorr, hover_color=self.hoverr_color,
                                               command=self.t240)
        self.btn_240.place(x=390, y=200, relwidth=0.1)

        self.btn_144 = customtkinter.CTkButton(master=self.frame_1, text="144p", text_color_disabled="black",
                                               state=DISABLED, height=35, fg_color=("red"),
                                               font=(None, 11,), corner_radius=16, border_width=0,
                                               border_color=self.border_colorr, hover_color=self.hoverr_color,
                                               command=lambda :threading.Thread(target=self.add_f(self.tag144, self.index144)).start())
        self.btn_144.place(x=480, y=200, relwidth=0.105)

        self.btn_160 = customtkinter.CTkButton(master=self.frame_1, text="Audio",text_color_disabled="black",
                                               height=35, fg_color=("red"),
                                               state=DISABLED,font=(None, 11,), corner_radius=16, border_width=0,
                                               border_color=self.border_colorr, hover_color=self.hoverr_color,
                                               command=self.t160kps)
        self.btn_160.place(x=570, y=200, relwidth=0.105)

        self.thumbnail_lab = customtkinter.CTkLabel(master=self.frame_1, text="", fg_color=("#383838"), height=85,
                                                    width=150)
        # self.thumbnail_lab.place(x=30, y=109)
        # End of thumnail

        self.vid_title = customtkinter.CTkLabel(master=self.frame_1, text="", font=(None, 11, "bold"))
        self.vid_title.place(x=250, y=109)

        self.vid_length = customtkinter.CTkLabel(master=self.frame_1, text="", font=(None, 11, "bold"))
        self.vid_length.place(x=250, y=130)

        self.vid_author = customtkinter.CTkLabel(master=self.frame_1, text="", font=(None, 11, "bold"))
        self.vid_author.place(x=250, y=151)

        self.vid_views = customtkinter.CTkLabel(master=self.frame_1, text="", font=(None, 11, "bold"))
        self.vid_views.place(x=250, y=172)

        _img = Image.open("proxytube1.png")
        _img = _img.resize((400, 120), Image.Resampling.LANCZOS)
        self.text_img = customtkinter.CTkImage(light_image=_img,dark_image=_img, size=(400, 120)
)

        self.size_display = customtkinter.CTkLabel(master=self, text='', image=self.text_img, font=(None, 11, "bold"))
        self.size_display.place(x=170, y=260)

    def frame_2_build(self):
        self.frame_ = customtkinter.CTkFrame(master=self.frame_2, width=790, height=90, )  # fg_color=(self.bg_color))
        self.frame_.place(x=20, y=5)

        self.frame_1 = customtkinter.CTkFrame(master=self.frame_2, width=790, height=90, )  # fg_color=(self.bg_color))
        self.frame_1.place(x=20, y=100)

        self.frame_2 = customtkinter.CTkFrame(master=self.frame_2, width=790, height=88, )  # fg_color=(self.bg_color))
        self.frame_2.place(x=20, y=196)


    def notifyuser(self):
        self.notifyalert = customtkinter.CTkToplevel(master=self, )
        self.notifyalert.title("Error")
        self.nlable = customtkinter.CTkLabel(master=self.notifyalert, text="No room availabel for download!!!",
                                             font=(None, 13, "bold"))
        self.nlable.place(relx=0.13, rely=0.37)
        self.notifyalert.geometry("350x200")

    def mode(self):
        global audio
        if self.mode_switch.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def t1080(self):
        t = threading.Thread(target=self.add_f(self.tag1080, self.index1080))
        t.start()

    def t720(self):
        t = threading.Thread(target=self.add_f(self.tag720, self.index720))
        t.start()

    def t480(self):
        t = threading.Thread(target=self.add_f(self.tag480, self.index480))
        t.start()

    def t360(self):
        t = threading.Thread(target=self.add_f(self.tag360, self.index360))
        t.start()
 
    def t240(self):
        t = threading.Thread(target=self.add_f(self.tag240, self.index240))
        t.start()

    def t160kps(self):
    
        t = threading.Thread(target=self.add_f("audio", "audio"))
        t.start()

    # def t1080(self):
    #     t = threading.Thread(target=self.add_f(self.tag1080, self.index1080))
    #     t.start()

    def add_f(self, tags, indexx):
        if self.runningtask == 3:
            self.notifyuser()
        else:
            # self.pathh1 = filedialog.askdirectory()
            self.t = tags
            self.ix = indexx
            if self.download_int == 0:
                self.dd1 = threading.Thread(target=self.download_one)
                self.dd1.start()
                self.download_int += 1
            elif self.download_int == 1:
                self.dd2 = threading.Thread(target=self.download_two)
                self.dd2.start()
                self.download_int += 1
            else:
                self.dd3 = threading.Thread(target=self.download_three)
                self.dd3.start()
                self.download_int = 0

    def resize_thumbnail(self):
        lis = ["try.jpg", "youtube.jpg"]
        # Resizing of image
        thumbnail_img = Image.open(lis[random.randint(0, 1)])
        thumbnail_img = thumbnail_img.resize((200, 85), Image.Resampling.LANCZOS)
        self.thumbnail_img = customtkinter.CTkImage(light_image=thumbnail_img,dark_image=thumbnail_img, size=(200, 85))

    def paste_fnc(self):
        self.search_entry.delete(0, END)
        self.search_entry.insert(END, clipboard.paste())

    def youtubefetchthread(self):
        thread = threading.Thread(target=self.youtube_fetch)
        thread.start()

    def youtube_fetch(self):
        # self.size_display.configure(text="")
        try:
            self.yt = YouTube(self.search_entry.get())
            self.file_name = self.yt.title
            self.file_length = self.yt.length
            self.file_author = self.yt.author
            self.file_views = self.yt.views
            self.file_thumbnail = self.yt.thumbnail_url
            self.thumbnail_lab.place(x=30, y=109)
            # self.resize_thumbnail()
            # DISPLAYING THUMBNAIL
            self.thumbnail_img_data = urlopen(self.file_thumbnail).read()
            self.thumbnail_img_of_file = Image.open(BytesIO(self.thumbnail_img_data))
            self.thumbnail_img_of_file = self.thumbnail_img_of_file.resize((200, 85), Image.Resampling.LANCZOS)
            self.thumbnail_img_of_file = ImageTk.PhotoImage(self.thumbnail_img_of_file)
            self.thumbnail_lab.configure(image=self.thumbnail_img_of_file)
            # End of thumnail

            self.vid_title.configure(text=f"Title:{self.file_name}    ")

            if self.file_length > 60 and self.file_length < 3600:
                self.minute = self.file_length // 60
                self.second = self.file_length % 60
                self.vid_length.configure(text=f"Length: {self.minute} minutes {self.second} seconds")

            elif self.file_length >= 3600:
                self.hour = (self.file_length // 60) // 60
                self.minute = (self.file_length // 60) % 60
                self.second = self.file_length % 60
                self.vid_length.configure(text=f"Length: {self.hour} hour {self.minute} minutes {self.second} seconds")

            elif self.file_length < 60:
                self.vid_length.configure(text=f"Length: {self.file_length} seconds")

            self.vid_author.configure(text=f"Author:{self.file_author}")

            self.vid_views.configure(text=f"Views:{self.file_views}    ")

            self.streams_availabel = self.yt.streams.filter(file_extension="mp4")
            self.streams_availabel_resolution_list = [stream.resolution for stream in self.streams_availabel]
            self.streams_availabel_itag_list = [stream.itag for stream in self.streams_availabel]
            print(self.streams_availabel_resolution_list)
            self.audio_streams_availabel = self.yt.streams.filter(only_audio=True)
            self.audio_streams_list = [stream.abr for stream in self.audio_streams_availabel]
            print(self.audio_streams_list)
        except:
            messagebox.showerror(title='Error', message='Something went wrong, please check your internet connection and try again!')


        if "240p" in self.streams_availabel_resolution_list:
            self.btn_240.configure(state=NORMAL, fg_color=(self.bg_color))
            self.index240 = self.streams_availabel_resolution_list.index("240p")
            self.tag240 = self.streams_availabel_itag_list[self.index240]
        else:
            self.btn_240.configure(state=DISABLED, fg_color=("red"))

        if "360p" in self.streams_availabel_resolution_list:
            self.btn_360.configure(state=NORMAL, fg_color=(self.bg_color))
            self.filesize360 = self.yt.streams.filter(res="360p").first().filesize
            self.index360 = self.streams_availabel_resolution_list.index("360p")
            self.tag360 = self.streams_availabel_itag_list[self.index360]
        else:
            self.btn_360.configure(state=DISABLED, fg_color=("red"))

        if "720p" in self.streams_availabel_resolution_list:
            self.btn_720.configure(state=NORMAL, fg_color=(self.bg_color))
            self.index720 = self.streams_availabel_resolution_list.index("720p")
            self.tag720 = self.streams_availabel_itag_list[self.index720]
        else:
            self.btn_720.configure(state=DISABLED, fg_color=("red"))

        if "480p" in self.streams_availabel_resolution_list:
            self.btn_480.configure(state=NORMAL, fg_color=(self.bg_color))
            self.index480 = self.streams_availabel_resolution_list.index("480p")
            self.tag480 = self.streams_availabel_itag_list[self.index480]
        else:
            self.btn_480.configure(state=DISABLED, fg_color=("red"))

        if "1080p" in self.streams_availabel_resolution_list:
            self.btn_1080.configure(state=NORMAL, fg_color=(self.bg_color))
            # self.filesize1080 = self.yt.streams.filter(res="1080p").first().filesize
            # print(self.filesize1080 / 1048576)
            self.index1080 = self.streams_availabel_resolution_list.index("1080p")
            self.tag1080 = self.streams_availabel_itag_list[self.index1080]
        else:
            self.btn_1080.configure(state=DISABLED, fg_color=("red"))

        if "144p" in self.streams_availabel_resolution_list:
            self.btn_144.configure(state=NORMAL, fg_color=(self.bg_color))
            self.index144 = self.streams_availabel_resolution_list.index("144p")
            self.tag144 = self.streams_availabel_itag_list[self.index144]
        else:
            self.btn_1080.configure(state=DISABLED, fg_color=("red"))

        self.btn_160.configure(state=NORMAL, fg_color=(self.bg_color))

        if self.once == 1:
            self.frame_2_build()
            self.once += 1

    # https://youtu.be/7-5rwRVeU08 , https://youtu.be/Pr7zc7rUjNA https://www.youtube.com/watch?v=9IeVFyBBtSQ
    # 10 sec https://youtu.be/UT5F9AXjwhg
    # 30 sec https://youtu.be/r4kL2tqwiOE
    # https://www.youtube.com/watch?v=F5mRW0jo-U4&t=614s django
    def download_one(self):
        print(1)
        global audio
        if self.ix == 'audio':
            audio = True
        if audio == True:
            self.file_to_download_size_1 = self.yt.streams.filter(only_audio=True).first().filesize
            self.user_decision_1 = tkinter.messagebox.askyesno("Do You Want To Download",f"File Size: {self.file_to_download_size_1/ 1048576:0.2f} MegaBytes")
            if self.user_decision_1 == True:
                audio_proceed= True
            # audio= False
        else:
            self.file_to_download_size_1 = self.yt.streams.filter(res=self.streams_availabel_resolution_list[self.ix]).first().filesize
            self.user_decision_1 = tkinter.messagebox.askyesno("Do You Want To Download",f"File Size: {self.file_to_download_size_1/ 1048576:0.2f} MegaBytes")
        if self.user_decision_1 == True:
            # download one section
            self.cc = self.color_list[random.randint(0, 5)]
            # Resizing of thumbnail_img
            self.thumbnaill1 = Image.open(BytesIO(self.thumbnail_img_data))
            self.thumbnaill1 = self.thumbnaill1.resize((150, 70), Image.Resampling.LANCZOS)
            self.thumbnaill1 = ImageTk.PhotoImage(self.thumbnaill1)
            # End of resizing
            self.file_thumbnail_1 = customtkinter.CTkLabel(master=self.frame_, text="", image=self.thumbnaill1, fg_color=(self.cc), height=70, width=150)
            self.file_thumbnail_1.place(x=30, y=10)
            self.tittle_to_be_check = self.file_name
            self.tittle = ""
            if len(self.tittle_to_be_check) > 70:
                for i in range(0, 64):
                    self.tittle = self.tittle + self.tittle_to_be_check[i]
                self.tittle = self.tittle + "...."
            else:
                self.tittle = self.tittle_to_be_check

            self.file_title = customtkinter.CTkLabel(master=self.frame_, justify="left", text=self.tittle,
                                                     font=(None, 11, "bold"))
            self.file_title.place(x=190, y=10)  # , relwidth=0.9)

            self.downloaded_remaining = customtkinter.CTkLabel(master=self.frame_, text=f"0mb of {self.file_to_download_size_1/ 1048576:0.2f}mb",
                                                               text_color=(self.bg_color), font=(None, 11, "bold"),
                                                               justify="left",)# relief="solid")
            self.downloaded_remaining.place(x=355, y=40)
            self.download_percentage = customtkinter.CTkLabel(master=self.frame_, text="0%",
                                                              text_color=(self.bg_color), font=(None, 11, "bold"),
                                                              justify="left",)# relief="solid")
            self.download_percentage.place(x=670, y=40)

            self.file_progress_1 = customtkinter.CTkProgressBar(master=self.frame_, width=500,
                                                                progress_color=(self.bg_color))
            self.file_progress_1.place(x=195, y=70)
            self.file_progress_1.set(0)
            try:
                self.pathh1 = filedialog.askdirectory()
                os.chdir(self.pathh1)
                self.runningtask += 1
                if self.called == "3":
                    self.downloaded_remaining3.config(text= "Waiting to download....")
                self.called= "1"
                threading.Thread(target=self.switch_).start()
                # self.yt.register_on_progress_callback(self.progress1)
                # self.yt.streams.filter(res=self.streams_availabel_resolution_list[self.ix]).first().download()
            except OSError as e:
                self.downloaded_remaining.configure(text="Download cancelled")
                audio= False
        else:
            print("Download cancelled")
            self.download_int -= 1
            audio= False
            # self.downloaded_remaining.configure(text="Download cancelled")

    def download_two(self):
        print(2)
        global audio
        if self.ix == 'audio':
            audio = True
        if audio == True:
            self.file_to_download_size_2 = self.yt.streams.filter(only_audio=True).first().filesize
            self.user_decision_2 = tkinter.messagebox.askyesno("Do You Want To Download",f"File Size: {self.file_to_download_size_2/ 1048576:0.2f} MegaBytes")
        else:
            self.file_to_download_size_2 = self.yt.streams.filter(
                res=self.streams_availabel_resolution_list[self.ix]).first().filesize
            self.user_decision_2 = tkinter.messagebox.askyesno("Do You Want To Download",f"File Size: {self.file_to_download_size_2/ 1048576:0.2f} MegaBytes")
        if self.user_decision_2 == True:
            # download two section
            self.cc = self.color_list[random.randint(0, 5)]
            # Resizing of thumbnail_img
            self.thumbnaill2 = Image.open(BytesIO(self.thumbnail_img_data))
            self.thumbnaill2 = self.thumbnaill2.resize((150, 70), Image.Resampling.LANCZOS)
            self.thumbnaill2 = ImageTk.PhotoImage(self.thumbnaill2)
            # End of resizing

            self.file_thumbnail_2 = customtkinter.CTkLabel(master=self.frame_1, text="", image=self.thumbnaill2,
                                                           fg_color=(self.cc), height=70, width=150)
            self.file_thumbnail_2.place(x=30, y=10)

            self.tittle_to_be_check_2 = self.file_name
            self.tittle_2 = ""
            if len(self.tittle_to_be_check_2) > 70:
                for i in range(0, 64):
                    self.tittle_2 = self.tittle_2 + self.tittle_to_be_check_2[i]
                self.tittle_2 = self.tittle_2 + "...."
            else:
                self.tittle_2 = self.tittle_to_be_check_2

            self.file_title = customtkinter.CTkLabel(master=self.frame_1, justify="left", #relief="solid",
                                                     text=self.tittle_2, font=(None, 11, "bold"))
            self.file_title.place(x=190, y=10)

            self.downloaded_remaining2 = customtkinter.CTkLabel(master=self.frame_1, text=f"0mb of {self.file_to_download_size_2/ 1048576:0.2f}mb",
                                                                text_color=(self.bg_color), font=(None, 11, "bold"),
                                                                justify="left")#, relief="solid")
            self.downloaded_remaining2.place(x=355, y=40)
            self.download_percentage2 = customtkinter.CTkLabel(master=self.frame_1, text=f"0%",
                                                               text_color=(self.bg_color), font=(None, 11, "bold"),
                                                               justify="left")#, relief="solid")
            self.download_percentage2.place(x=670, y=40)

            self.file_progress_2 = customtkinter.CTkProgressBar(master=self.frame_1, width=500,
                                                                progress_color=(self.bg_color))
            self.file_progress_2.place(x=195, y=70)
            self.file_progress_2.set(0)
            try:
                self.pathh2 = filedialog.askdirectory()
                os.chdir(self.pathh2)
                self.runningtask += 1
                if self.called == "1":
                    self.downloaded_remaining2.config(text= "Waiting to download....")
                self.called= "2"
                threading.Thread(target=self.switch_).start()
                # self.yt.register_on_progress_callback(self.progress2)
                # self.yt.streams.filter(res=self.streams_availabel_resolution_list[self.ix]).first().download()
            except OSError as e:
                self.downloaded_remaining2.configure(text="Download cancelled")
                audio= False
        else:
            print("Download cancelled")
            self.download_int -= 1
            audio= False
            # self.downloaded_remaining2.configure(text="Download cancelled")

    def download_three(self):
        print(3)
        global audio
        if self.ix == 'audio':
            audio = True
        if audio == True:
            self.file_to_download_size_3 = self.yt.streams.filter(only_audio=True).first().filesize
            self.user_decision_3 = tkinter.messagebox.askyesno("Do You Want To Download",f"File Size: {self.file_to_download_size_3/ 1048576:0.2f} MegaBytes")
        else:
            self.file_to_download_size_3 = self.yt.streams.filter(
                res=self.streams_availabel_resolution_list[self.ix]).first().filesize
            self.user_decision_3 = tkinter.messagebox.askyesno("Do You Want To Download",f"File Size: {self.file_to_download_size_3/ 1048576:0.2f} MegaBytes")
        if self.user_decision_3 == True:
            # download three section
            self.cc = self.color_list[random.randint(0, 5)]
            # Resizing of thumbnail_img
            self.thumbnaill3 = Image.open(BytesIO(self.thumbnail_img_data))
            self.thumbnaill3 = self.thumbnaill3.resize((150, 70), Image.Resampling.LANCZOS)
            self.thumbnaill3 = ImageTk.PhotoImage(self.thumbnaill3)
            # End of resizing
            self.file_thumbnail_3 = customtkinter.CTkLabel(master=self.frame_2, text="", image=self.thumbnaill3,
                                                           fg_color=(self.cc), height=70, width=150)
            self.file_thumbnail_3.place(x=30, y=10)

            self.tittle_to_be_check_3 = self.file_name
            self.tittle_3 = ""
            if len(self.tittle_to_be_check_3) > 70:
                for i in range(0, 64):
                    self.tittle_3 = self.tittle_3 + self.tittle_to_be_check_3[i]
                self.tittle_3 = self.tittle_3 + "...."
            else:
                self.tittle_3 = self.tittle_to_be_check_3

            self.file_title = customtkinter.CTkLabel(master=self.frame_2, justify="left", #relief="solid",
                                                     text=self.tittle_3, font=(None, 11, "bold"))
            self.file_title.place(x=190, y=10)

            self.downloaded_remaining3 = customtkinter.CTkLabel(master=self.frame_2, text=f"0mb of {self.file_to_download_size_3/ 1048576:0.2f}mb",
                                                                text_color=self.bg_color, font=(None, 11, "bold"),
                                                                justify="left",)# relief="solid")
            self.downloaded_remaining3.place(x=355, y=40)
            self.download_percentage3 = customtkinter.CTkLabel(master=self.frame_2, text=f"0%",
                                                               text_color=self.bg_color, font=(None, 11, "bold"),
                                                               justify="left",)# relief="solid")
            self.download_percentage3.place(x=670, y=40)

            self.file_progress_3 = customtkinter.CTkProgressBar(master=self.frame_2, width=500 ,progress_color=(self.bg_color))
            self.file_progress_3.place(x=195, y=70)
            self.file_progress_3.set(0)
            try:
                self.pathh3 = filedialog.askdirectory()
                os.chdir(self.pathh3)
                self.runningtask += 1
                if self.called == "2":
                    self.downloaded_remaining3.config(text= "Waiting to download....")
                self.called= "3"
                threading.Thread(target=self.switch_).start()

                # self.yt.register_on_progress_callback(self.progress3)
                # self.yt.streams.filter(res=self.streams_availabel_resolution_list[self.ix]).first().download()
            except OSError as e:
                self.downloaded_remaining3.configure(text="Download cancelled")
                audio= False
        else:
            print("Download cancelled")
            self.download_int -= 1
            audio= False
            # self.downloaded_remaining3.configure(text="Download cancelled")


    def switch_(self):
        print("Called")
        # if runinng task is >= 1 their lab should display waiting
        self.lock = threading.Lock()
        if self.called == "1":
            self.lock.acquire()
            self.file_d_1()
            
        if self.called == "2":
            self.lock.acquire()
            self.file_d_2()
           
        if self.called == "3":
            self.lock.acquire()
            self.file_d_3()
            

    def file_d_1(self):
        global audio
        self.yt.register_on_progress_callback(self.progress1)
        if audio == True:
            audi= self.yt.streams.filter(only_audio=TRUE).first().download()
            base, ext = os.path.splitext(audi)
            converted=base +'.mp3'
            os.rename(audi,converted)
        else:
            self.yt.streams.filter(res=self.streams_availabel_resolution_list[self.ix]).first().download()
        if self.file_progress_1.get() == 1:
            self.lock.release()
            audio= False
# https://www.youtube.com/watch?v=U75AweDbrZw
    def file_d_2(self):
        global audio
        self.yt.register_on_progress_callback(self.progress2)
        if audio == True:
            audi= self.yt.streams.filter(only_audio=TRUE).first().download()
            base, ext = os.path.splitext(audi)
            converted=base +'.mp3'
            os.rename(audi,converted)
        else:
            self.yt.streams.filter(res=self.streams_availabel_resolution_list[self.ix]).first().download()
        if self.file_progress_2.get() == 1:
            self.lock.release()

    def file_d_3(self):
        global audio
        self.yt.register_on_progress_callback(self.progress3)
        if audio == True:
            audi= self.yt.streams.filter(only_audio=TRUE).first().download()
            base, ext = os.path.splitext(audi)
            converted=base +'.mp3'
            os.rename(audi,converted)
        else:
            self.yt.streams.filter(res=self.streams_availabel_resolution_list[self.ix]).first().download()
        if self.file_progress_3.get() == 1:
            self.lock.release()

    def progress1(self, stream, chunk, bytes_remaining):
        self.bytesrmaining = bytes_remaining
        self.bytes_downloaded_1 = self.file_to_download_size_1 - self.bytesrmaining
        self.bytes_downloaded_percentage_1 = int((self.bytes_downloaded_1 / self.file_to_download_size_1) * 100)
        self.file_progress_1.set(self.bytes_downloaded_percentage_1/100)
        self.download_percentage.configure(text=f"{self.bytes_downloaded_percentage_1}%")
        self.downloaded_remaining.configure(text=f"{self.bytes_downloaded_1 / 1048576:0.2f}mb of {self.file_to_download_size_1/ 1048576:0.2f}mb")
        print(f"{self.bytes_downloaded_1} bytes downloaded\n{self.bytes_downloaded_percentage_1}% downloaded")
        if self.file_progress_1.get() == 1:
            self.complete()

    # def complete1(self):
    #     self.runningtask -= 1
    #     self.complete1alert = customtkinter.CTkToplevel(master=self, )
    #     self.complete1alert.title("Info")
    #     self.dlable = customtkinter.CTkLabel(master=self.complete1alert, text="Download complete!", font=(None, 15, "bold"))
    #     self.dlable.place(relx=0.2, rely=0.37)
    #     self.complete1alert.geometry("350x200")
    #     print("Done")

    def progress2(self, stream, chunk, bytes_remaining):
        self.bytesrmaining = bytes_remaining
        self.bytes_downloaded_2 = self.file_to_download_size_2 - bytes_remaining
        self.bytes_downloaded_percentage_2 = int((self.bytes_downloaded_2 / self.file_to_download_size_2) * 100)
        self.file_progress_2.set(self.bytes_downloaded_percentage_2/100)
        self.download_percentage2.configure(text=f"{self.bytes_downloaded_percentage_2}%")
        self.downloaded_remaining2.configure(text=f"{self.bytes_downloaded_2 / 1048576:0.2f}mb of {self.file_to_download_size_2/ 1048576:0.2f}mb")
        print(f"{self.bytes_downloaded_2} bytes downloaded\n{self.bytes_downloaded_percentage_2}% downloaded")
        if self.file_progress_2.get() == 1:
            self.complete()

    # def complete2(self):
    #     self.runningtask -= 1
    #     self.complete1alert = customtkinter.CTkToplevel(master=self, )
    #     self.complete1alert.title("Info")
    #     self.dlable = customtkinter.CTkLabel(master=self.complete1alert, text="Download complete!", font=(None, 15, "bold"))
    #     self.dlable.place(relx=0.2, rely=0.37)
    #     self.complete1alert.geometry("350x200")
    #     print("Done")

    def progress3(self, stream, chunk, bytes_remaining):
        self.bytesrmaining = bytes_remaining
        self.bytes_downloaded_3 = self.file_to_download_size_3 - bytes_remaining
        self.bytes_downloaded_percentage_3 = int((self.bytes_downloaded_3 / self.file_to_download_size_3) * 100)
        self.file_progress_3.set(self.bytes_downloaded_percentage_3/100)
        self.download_percentage3.configure(text=f"{self.bytes_downloaded_percentage_3}%")
        self.downloaded_remaining3.configure(text=f"{self.bytes_downloaded_3 / 1048576:0.2f}mb of {self.file_to_download_size_3/ 1048576:0.2f}mb")
        print(f"{self.bytes_downloaded_3} bytes downloaded\n{self.bytes_downloaded_percentage_3}% downloaded")
        if self.file_progress_3.get() == 1:
            self.complete()

    def complete(self):
        self.runningtask -= 1
        self.complete1alert = customtkinter.CTkToplevel(master=self, )
        self.complete1alert.title("Info")
        self.dlable = customtkinter.CTkLabel(master=self.complete1alert, text="Download complete!", font=(None, 15, "bold"))
        self.dlable.place(relx=0.2, rely=0.37)
        self.complete1alert.geometry("350x200")
        print("Done")

    def btn_d(self):
        self.youtube_fetch()

    def call_functions(self):
        self.frame_1_build()

    def build(self):
        self.title("Proxytube")
        self.geometry("850x700")
        # self.iconbitmap("ytdicon.ico")
        self.resizable(0, 0)
        self.call_functions()
        self.mainloop()


if __name__ == '__main__':
    App().build()

# https://www.youtube.com/watch?v=cyKblSwOMck