from tkinter import *
from PIL import Image, ImageTk
from pytube import YouTube
import pyperclip as clipboard
from pytube.cli import on_progress
from urllib.request import urlopen
from tkinter.filedialog import asksaveasfile
import tkinter
import customtkinter
import random
import base64, threading
from io import BytesIO

customtkinter.set_appearance_mode("dark")


class App(customtkinter.CTk, tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.once = 1
        self.download_int = 0
        self.runningtask = 0
        self.color_list = ["red", "green", "white", "pink", "yellow", "blue"]
        self.frame_1 = customtkinter.CTkFrame(master=self, width=830, height=250)
        self.frame_1.place(x=10, y=10)

        self.frame_2 = customtkinter.CTkFrame(master=self, width=830, height=310)
        self.frame_2.place(x=10, y=380)

    def frame_1_build(self):
        self.bg_color = "#c71c72"
        self.hoverr_color = "#660d3a"
        self.border_colorr = "#383838"
        self.down = 10
        self.new = "1"
        self.search_entry = customtkinter.CTkEntry(master=self.frame_1, placeholder_text="URL", fg_color=("white"),
                                                   text_color=("black"), height=35, text_font=(None, 15), width=500,
                                                   border_width=0, border_color="#c71c72", )
        self.search_entry.place(x=30, y=30)

        self.paste_btn = customtkinter.CTkButton(master=self.frame_1, text="Paste", height=35, fg_color=(self.bg_color),
                                                 text_font=(None, 13,), border_width=0, border_color=self.border_colorr,
                                                 hover_color=self.hoverr_color, command=self.paste_fnc)
        self.paste_btn.place(x=30, y=68, relwidth=0.105)

        self.search_btn = customtkinter.CTkButton(master=self.frame_1, text="Search", height=35,
                                                  fg_color=(self.bg_color), text_font=(None, 11,), border_width=0,
                                                  border_color="#c71c72", hover_color=self.hoverr_color,
                                                  command=self.youtubefetchthread)
        self.search_btn.place(x=535, y=30, relwidth=0.1)

        self.btn_1080 = customtkinter.CTkButton(master=self.frame_1, text="1080p", text_color_disabled="black",
                                                state=DISABLED, height=35, fg_color=("red"),
                                                text_font=(None, 11,), corner_radius=16, border_width=0,
                                                border_color=self.border_colorr, hover_color=self.hoverr_color,
                                                command=lambda :self.add_f(self.tag1080, self.index1080))
        self.btn_1080.place(x=30, y=200, relwidth=0.1)

        self.btn_720 = customtkinter.CTkButton(master=self.frame_1, text="720p", text_color_disabled="black",
                                               state=DISABLED, height=35, fg_color=("red"),
                                               text_font=(None, 11,), corner_radius=16, border_width=0,
                                               border_color=self.border_colorr, hover_color=self.hoverr_color,
                                               command=lambda :self.add_f(self.tag720, self.index720))
        self.btn_720.place(x=120, y=200, relwidth=0.1)

        self.btn_480 = customtkinter.CTkButton(master=self.frame_1, text="480p", text_color_disabled="black",
                                               state=DISABLED, height=35, fg_color=("red"),
                                               text_font=(None, 11,), corner_radius=16, border_width=0,
                                               border_color=self.border_colorr, hover_color=self.hoverr_color,
                                               command=lambda :self.add_f(self.tag480, self.index480))
        self.btn_480.place(x=210, y=200, relwidth=0.1)

        self.btn_360 = customtkinter.CTkButton(master=self.frame_1, text="360p", text_color_disabled="black",
                                               state=DISABLED, height=35, fg_color=("red"),
                                               text_font=(None, 11,), corner_radius=16, border_width=0,
                                               border_color=self.border_colorr, hover_color=self.hoverr_color,
                                               command=lambda :self.add_f(self.tag360, self.index360))
        self.btn_360.place(x=300, y=200, relwidth=0.1)

        self.btn_240 = customtkinter.CTkButton(master=self.frame_1, text="240p", text_color_disabled="black",
                                               state=DISABLED, height=35, fg_color=("red"),
                                               text_font=(None, 11,), corner_radius=16, border_width=0,
                                               border_color=self.border_colorr, hover_color=self.hoverr_color,
                                               command=lambda :self.add_f(self.tag240, self.index240))
        self.btn_240.place(x=390, y=200, relwidth=0.1)

        self.btn_144 = customtkinter.CTkButton(master=self.frame_1, text="144p", text_color_disabled="black",
                                               state=DISABLED, height=35, fg_color=("red"),
                                               text_font=(None, 11,), corner_radius=16, border_width=0,
                                               border_color=self.border_colorr, hover_color=self.hoverr_color,
                                               command=lambda :self.add_f(self.tag144, self.index144))
        self.btn_144.place(x=480, y=200, relwidth=0.105)

        self.btn_160 = customtkinter.CTkButton(master=self.frame_1, text="Audio", text_color_disabled="black",
                                               state=DISABLED, height=35, fg_color=("red"),
                                               text_font=(None, 11,), corner_radius=16, border_width=0,
                                               border_color=self.border_colorr, hover_color=self.hoverr_color,
                                               command=lambda :self.add_f())
        self.btn_160.place(x=570, y=200, relwidth=0.105)

        self.thumbnail_lab = customtkinter.CTkLabel(master=self.frame_1, text="", fg_color=("#383838"), height=85,
                                                    width=150)
        # self.thumbnail_lab.place(x=30, y=109)
        # End of thumnail

        self.vid_title = customtkinter.CTkLabel(master=self.frame_1, text="", text_font=(None, 11, "bold"))
        self.vid_title.place(x=250, y=109)

        self.vid_length = customtkinter.CTkLabel(master=self.frame_1, text="", text_font=(None, 11, "bold"))
        self.vid_length.place(x=250, y=130)

        self.vid_author = customtkinter.CTkLabel(master=self.frame_1, text="", text_font=(None, 11, "bold"))
        self.vid_author.place(x=250, y=151)

        self.vid_views = customtkinter.CTkLabel(master=self.frame_1, text="", text_font=(None, 11, "bold"))
        self.vid_views.place(x=250, y=172)

    def frame_2_build(self):
        self.frame_ = customtkinter.CTkFrame(master=self.frame_2, width=790, height=90, )  # fg_color=(self.bg_color))
        self.frame_.place(x=20, y=10)

        self.frame_1 = customtkinter.CTkFrame(master=self.frame_2, width=790, height=90, )  # fg_color=(self.bg_color))
        self.frame_1.place(x=20, y=110)

        self.frame_2 = customtkinter.CTkFrame(master=self.frame_2, width=790, height=90, )  # fg_color=(self.bg_color))
        self.frame_2.place(x=20, y=210)

    # self.main_frame = tkinter.Frame(self.frame_2)
    # self.main_frame.pack(fill=BOTH, expand=1)

    # self.lab_frame = tkinter.Canvas(self.main_frame)
    # self.lab_frame.pack(side=LEFT, fill=BOTH, expand=1)

    # self.lab = tkinter.Tk(self, text="Hell0",)
    def notifyuser(self):
        self.notifyalert = customtkinter.CTkToplevel(master=self, )
        self.notifyalert.title("Error")
        self.nlable = customtkinter.CTkLabel(master=self.notifyalert, text="No room availabel for download!!!",
                                             text_font=(None, 13, "bold"))
        self.nlable.place(relx=0.13, rely=0.37)
        self.notifyalert.geometry("350x200")


    def add_f(self, tags, indexx):
        if self.runningtask == 3:
            self.notifyuser()
        else:
            if self.download_int == 0:
                self.dd1 = threading.Thread(target=self.download_one(tags, indexx))
                self.dd1.start()
                self.download_int += 1
                self.runningtask += 1
            elif self.download_int == 1:
                self.dd2 = threading.Thread(target=self.download_two(tags, indexx))
                self.dd2.start()
                self.download_int += 1
                self.runningtask += 1
            else:
                self.dd3 = threading.Thread(target=self.download_three(tags, indexx))
                self.dd3.start()
                self.download_int = 0
                self.runningtask += 1

    def resize_thumbnail(self):
        lis = ["try.jpg", "youtube.jpg"]
        # Resizing of image
        self.thumbnail_img = Image.open(lis[random.randint(0, 1)])
        self.thumbnail_img = self.thumbnail_img.resize((200, 85), Image.Resampling.LANCZOS)
        self.thumbnail_img = ImageTk.PhotoImage(self.thumbnail_img)

    def paste_fnc(self):
        self.search_entry.delete(0, END)
        self.search_entry.insert(END, clipboard.paste())

    def youtubefetchthread(self):
        thread = threading.Thread(target=self.youtube_fetch)
        thread.start()

    def youtube_fetch(self):
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
        # print(self.streams_availabel_resolution_list)
        # print(self.streams_availabel_itag_list)
        # resolution = [stream.resolution for stream in , progressive=True).all()]
        # print(resolution)

        if "240p" in self.streams_availabel_resolution_list:
            self.btn_240.configure(state=NORMAL, fg_color=(self.bg_color))
            self.index240 = self.streams_availabel_resolution_list.index("240p")
            self.tag240 = self.streams_availabel_itag_list[self.index240]
        else:
            self.btn_240.configure(state=DISABLED, fg_color=("red"))

        if "360p" in self.streams_availabel_resolution_list:
            self.btn_360.configure(state=NORMAL, fg_color=(self.bg_color))
            self.filesize360 = self.yt.streams.filter(res="360p").first().filesize
            # print(self.filesize360 / 1048576)
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
            self.filesize1080 = self.yt.streams.filter(res="1080p").first().filesize
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

        # if "160kbps" in self.streams_availabel_resolution_list:
        #     self.btn_160.configure(state=DISABLED)
        # else:
        #     self.btn_160.configure(state=DISABLED)

        if self.once == 1:
            self.frame_2_build()
            self.once += 1

    # https://youtu.be/7-5rwRVeU08 , https://youtu.be/Pr7zc7rUjNA https://www.youtube.com/watch?v=9IeVFyBBtSQ
    # 10 sec https://youtu.be/UT5F9AXjwhg
    # 30 sec https://youtu.be/r4kL2tqwiOE
    def download_one(self, t, ix):
        print(t, ix)
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
        self.file_to_download_size_1 = self.yt.streams.filter(res=self.streams_availabel_resolution_list[ix]).first().filesize
        if len(self.tittle_to_be_check) > 70:
            for i in range(0, 64):
                self.tittle = self.tittle + self.tittle_to_be_check[i]
            self.tittle = self.tittle + "...."
        else:
            self.tittle = self.tittle_to_be_check

        self.file_title = customtkinter.CTkLabel(master=self.frame_, justify="left", relief="solid", text=self.tittle,
                                                 text_font=(None, 11, "bold"))
        self.file_title.place(x=190, y=10)  # , relwidth=0.9)

        self.downloaded_remaining = customtkinter.CTkLabel(master=self.frame_, text=f"",
                                                           text_color=(self.bg_color), text_font=(None, 11, "bold"),
                                                           justify="left", relief="solid")
        self.downloaded_remaining.place(x=355, y=40)
        self.pathh1 = asksaveasfile(initialfile=self.tittle + " " + self.streams_availabel_resolution_list[ix],
                      defaultextension=".mp4",
                      filetypes=[("All Files", "*.*"), ("Video File", "*.mp4")])
        self.download_percentage = customtkinter.CTkLabel(master=self.frame_, text="0%",
                                                          text_color=(self.bg_color), text_font=(None, 11, "bold"),
                                                          justify="left", relief="solid")
        self.download_percentage.place(x=670, y=40)

        self.file_progress_1 = customtkinter.CTkProgressBar(master=self.frame_, width=500,
                                                            progress_color=(self.bg_color))
        self.file_progress_1.place(x=195, y=70)
        # self.file_progress_1.set(0)
        print(self.pathh1)
        self.yt.register_on_progress_callback(self.progress1)
        self.yt.register_on_complete_callback(self.complete1())
        self.yt.streams.filter(res=self.streams_availabel_resolution_list[ix]).first().download()

    def download_two(self, t, ix):
        print(t,ix)
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

        self.file_title = customtkinter.CTkLabel(master=self.frame_1, justify="left", relief="solid",
                                                 text=self.tittle_2, text_font=(None, 11, "bold"))
        self.file_title.place(x=190, y=10)

        self.downloaded_remaining2 = customtkinter.CTkLabel(master=self.frame_1, text="15mb of 120mb",
                                                            text_color=(self.bg_color), text_font=(None, 11, "bold"),
                                                            justify="left", relief="solid")
        self.downloaded_remaining2.place(x=355, y=40)

        self.download_percentage2 = customtkinter.CTkLabel(master=self.frame_1, text=f"{random.randint(0, 100)}%",
                                                           text_color=(self.bg_color), text_font=(None, 11, "bold"),
                                                           justify="left", relief="solid")
        self.download_percentage2.place(x=670, y=40)

        self.file_progress_2 = customtkinter.CTkProgressBar(master=self.frame_1, width=500,
                                                            progress_color=(self.bg_color))
        self.file_progress_2.place(x=195, y=70)

    def download_three(self, t, ix):
        print(t,ix)
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

        self.file_title = customtkinter.CTkLabel(master=self.frame_2, justify="left", relief="solid",
                                                 text=self.tittle_3, text_font=(None, 11, "bold"))
        self.file_title.place(x=190, y=10)

        self.downloaded_remaining3 = customtkinter.CTkLabel(master=self.frame_2, text="15mb of 120mb",
                                                            text_color=self.bg_color, text_font=(None, 11, "bold"),
                                                            justify="left", relief="solid")
        self.downloaded_remaining3.place(x=355, y=40)

        self.download_percentage3 = customtkinter.CTkLabel(master=self.frame_2, text=f"0%",
                                                           text_color=self.bg_color, text_font=(None, 11, "bold"),
                                                           justify="left", relief="solid")
        self.download_percentage3.place(x=670, y=40)

        self.file_progress_3 = customtkinter.CTkProgressBar(master=self.frame_2, width=500,
                                                            progress_color=(self.bg_color))
        self.file_progress_3.place(x=195, y=70)

    def progress1(self, stream, chunk, bytes_remaining):
        self.bytes_downloaded_1 = self.file_to_download_size_1 - bytes_remaining
        self.bytes_downloaded_percentage_1 = int((self.bytes_downloaded_1 / self.file_to_download_size_1) * 100)
        self.file_progress_1.set(self.bytes_downloaded_percentage_1/100)
        self.download_percentage.configure(text=f"{self.bytes_downloaded_percentage_1}%")
        self.downloaded_remaining.configure(text=f"{self.bytes_downloaded_1 / 1048576:0.2f}mb of {self.file_to_download_size_1/ 1048576:0.2f}mb")

    def complete1(self):
        self.runningtask -= 1
        self.complete1alert = customtkinter.CTkToplevel(master=self, )
        self.complete1alert.title("Info")
        self.dlable = customtkinter.CTkLabel(master=self.complete1alert, text="Download complete!", text_font=(None, 15, "bold"))
        self.dlable.place(relx=0.2, rely=0.37)
        self.complete1alert.geometry("350x200")
        print("Done")

    def btn_d(self):
        self.youtube_fetch()

    def call_functions(self):
        self.frame_1_build()

    def build(self):
        self.title("Youtube Downloader")
        self.geometry("850x700")
        self.resizable(0, 0)
        self.call_functions()
        self.notifyuser()
        self.mainloop()


if __name__ == '__main__':
    App().build()
