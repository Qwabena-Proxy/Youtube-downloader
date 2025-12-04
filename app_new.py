import customtkinter
import threading
import random
import os
from tkinter import messagebox
from downloader import fetch_video, download_stream
from ui import UIBuilder

customtkinter.set_appearance_mode("system")


class AppNew(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.once = 1
        self.download_int = 0
        self.runningtask = 0
        self.color_list = ["red", "green", "white", "pink", "yellow", "blue"]
        self.called = ""
        self.ui = UIBuilder(self)
        self.ui.build_frames()

        # placeholders for fetched video info
        self.yt = None
        self.streams_available = []

    def mode(self):
        if self.mode_switch.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    # --- button handlers ---
    def paste_fnc(self):
        try:
            import pyperclip as clipboard
            self.search_entry.delete(0, 'end')
            self.search_entry.insert('end', clipboard.paste())
        except Exception:
            pass

    def youtubefetchthread(self):
        t = threading.Thread(target=self.youtube_fetch)
        t.start()

    def youtube_fetch(self):
        url = self.search_entry.get()
        try:
            info = fetch_video(url)
            self.yt = info['yt']
            self.file_name = info['title']
            self.file_length = info['length']
            self.file_author = info['author']
            self.file_views = info['views']
            self.file_thumbnail = info['thumbnail_url']

            # update UI
            self.vid_title.configure(text=f"Title:{self.file_name}    ")
            # length formatting
            if self.file_length > 60 and self.file_length < 3600:
                minute = self.file_length // 60
                second = self.file_length % 60
                self.vid_length.configure(text=f"Length: {minute} minutes {second} seconds")
            elif self.file_length >= 3600:
                hour = (self.file_length // 60) // 60
                minute = (self.file_length // 60) % 60
                second = self.file_length % 60
                self.vid_length.configure(text=f"Length: {hour} hour {minute} minutes {second} seconds")
            else:
                self.vid_length.configure(text=f"Length: {self.file_length} seconds")

            self.vid_author.configure(text=f"Author:{self.file_author}")
            self.vid_views.configure(text=f"Views:{self.file_views}    ")

            self.streams_availabel = info['video_streams']
            self.streams_availabel_resolution_list = info['video_resolutions']
            self.streams_availabel_itag_list = info['video_itags']
            self.audio_streams_availabel = info['audio_streams']
            self.audio_streams_list = info['audio_abrs']

            # show thumbnail
            self.ui.show_thumbnail(self.file_thumbnail)

            # enable buttons conditionally
            self.enable_buttons()

            if self.once == 1:
                # create extra frames like original app
                self.frame_ = customtkinter.CTkFrame(master=self.frame_2, width=790, height=90)
                self.frame_.place(x=20, y=5)
                self.frame_1 = customtkinter.CTkFrame(master=self.frame_2, width=790, height=90)
                self.frame_1.place(x=20, y=100)
                self.frame_2b = customtkinter.CTkFrame(master=self.frame_2, width=790, height=88)
                self.frame_2b.place(x=20, y=196)
                self.once += 1

        except Exception:
            messagebox.showerror(title='Error', message='Something went wrong, please check your internet connection and try again!')

    def enable_buttons(self):
        # map existence of resolution to button state
        self.ui.set_button_state(self.btn_240, "240p" in self.streams_availabel_resolution_list)
        self.ui.set_button_state(self.btn_360, "360p" in self.streams_availabel_resolution_list)
        self.ui.set_button_state(self.btn_480, "480p" in self.streams_availabel_resolution_list)
        self.ui.set_button_state(self.btn_720, "720p" in self.streams_availabel_resolution_list)
        self.ui.set_button_state(self.btn_1080, "1080p" in self.streams_availabel_resolution_list)
        self.ui.set_button_state(self.btn_144, "144p" in self.streams_availabel_resolution_list)
        # audio always allow if there are audio streams
        self.ui.set_button_state(self.btn_160, len(self.audio_streams_availabel) > 0)

    # quality handlers simply call add_f with index/itag
    def t1080(self):
        try:
            self.add_f(self.tag1080, self.index1080)
            return
        except Exception:
            pass
        try:
            idx = self.streams_availabel_resolution_list.index("1080p")
            itag = self.streams_availabel_itag_list[idx]
            self.add_f(itag, idx)
        except Exception:
            messagebox.showinfo("Info", "Please fetch the video first or 1080p not available")

    def t720(self):
        try:
            self.add_f(self.tag720, self.index720)
            return
        except Exception:
            pass
        try:
            idx = self.streams_availabel_resolution_list.index("720p")
            itag = self.streams_availabel_itag_list[idx]
            self.add_f(itag, idx)
        except Exception:
            messagebox.showinfo("Info", "Please fetch the video first or 720p not available")

    def t480(self):
        try:
            self.add_f(self.tag480, self.index480)
            return
        except Exception:
            pass
        try:
            idx = self.streams_availabel_resolution_list.index("480p")
            itag = self.streams_availabel_itag_list[idx]
            self.add_f(itag, idx)
        except Exception:
            messagebox.showinfo("Info", "Please fetch the video first or 480p not available")

    def t360(self):
        try:
            self.add_f(self.tag360, self.index360)
            return
        except Exception:
            pass
        try:
            idx = self.streams_availabel_resolution_list.index("360p")
            itag = self.streams_availabel_itag_list[idx]
            self.add_f(itag, idx)
        except Exception:
            messagebox.showinfo("Info", "Please fetch the video first or 360p not available")

    def t240(self):
        try:
            self.add_f(self.tag240, self.index240)
            return
        except Exception:
            pass
        try:
            idx = self.streams_availabel_resolution_list.index("240p")
            itag = self.streams_availabel_itag_list[idx]
            self.add_f(itag, idx)
        except Exception:
            messagebox.showinfo("Info", "Please fetch the video first or 240p not available")

    def t144(self):
        try:
            self.add_f(self.tag144, self.index144)
            return
        except Exception:
            pass
        try:
            idx = self.streams_availabel_resolution_list.index("144p")
            itag = self.streams_availabel_itag_list[idx]
            self.add_f(itag, idx)
        except Exception:
            messagebox.showinfo("Info", "Please fetch the video first or 144p not available")

    def t160kps(self):
        self.add_f("audio", "audio")

    def add_f(self, tags, indexx):
        if self.runningtask == 3:
            self.ui.notify_no_room()
        else:
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

    # the download_{one,two,three} methods mimic structure in original file
    def download_one(self):
        print(1)
        global_audio = False
        if self.ix == 'audio':
            global_audio = True
        if global_audio:
            size = self.yt.streams.filter(only_audio=True).first().filesize
            decision = self.ui.ask_confirm_download(size)
        else:
            size = self.yt.streams.filter(res=self.streams_availabel_resolution_list[self.ix]).first().filesize
            decision = self.ui.ask_confirm_download(size)
        if decision:
            # simple UI elements for download row
            self.cc = self.color_list[random.randint(0, 5)]
            self.thumbnaill1 = None
            try:
                # reuse UI thumbnail
                self.thumbnaill1 = self.thumbnail_lab.image
            except Exception:
                pass
            self.file_thumbnail_1 = customtkinter.CTkLabel(master=self.frame_, text="", image=self.thumbnaill1 if self.thumbnaill1 else None, fg_color=(self.cc), height=70, width=150)
            self.file_thumbnail_1.place(x=30, y=10)
            # title
            title = self.file_name if len(self.file_name) < 70 else self.file_name[:64] + "...."

            self.file_title = customtkinter.CTkLabel(master=self.frame_, justify="left", text=title,
                                                     font=(None, 11, "bold"))
            self.file_title.place(x=190, y=10)

            self.downloaded_remaining = customtkinter.CTkLabel(master=self.frame_, text=f"0mb of {size/ 1048576:0.2f}mb",
                                                               text_color=(self.bg_color), font=(None, 11, "bold"),
                                                               justify="left",)
            self.downloaded_remaining.place(x=355, y=40)
            self.download_percentage = customtkinter.CTkLabel(master=self.frame_, text="0%",
                                                              text_color=(self.bg_color), font=(None, 11, "bold"),
                                                              justify="left",)
            self.download_percentage.place(x=670, y=40)

            self.file_progress_1 = customtkinter.CTkProgressBar(master=self.frame_, width=500,
                                                                progress_color=(self.bg_color))
            self.file_progress_1.place(x=195, y=70)
            self.file_progress_1.set(0)
            try:
                outdir = self.ui.ask_save_dir()
                os.chdir(outdir)
                self.runningtask += 1
                if self.called == "3":
                    try:
                        self.downloaded_remaining3.config(text= "Waiting to download....")
                    except Exception:
                        pass
                self.called= "1"
                # perform download synchronously here but in a thread already
                # register progress callback to update UI
                def progress_cb(stream, chunk, bytes_remaining):
                    bytes_downloaded = size - bytes_remaining
                    pct = int((bytes_downloaded / size) * 100) if size else 0
                    try:
                        self.file_progress_1.set(pct/100)
                        self.download_percentage.configure(text=f"{pct}%")
                        self.downloaded_remaining.configure(text=f"{bytes_downloaded / 1048576:0.2f}mb of {size/ 1048576:0.2f}mb")
                    except Exception:
                        pass

                if global_audio:
                    download_stream(self.yt, only_audio=True, output_path=outdir, progress_callback=progress_cb)
                else:
                    itag = self.streams_availabel_itag_list[self.ix]
                    download_stream(self.yt, itag=itag, output_path=outdir, progress_callback=progress_cb)

                # on complete
                self.runningtask -= 1
                messagebox.showinfo("Info", "Download complete!")
            except Exception:
                try:
                    self.downloaded_remaining.configure(text="Download cancelled")
                except Exception:
                    pass
        else:
            print("Download cancelled")
            self.download_int -= 1

    def download_two(self):
        print(2)
        global_audio = False
        if self.ix == 'audio':
            global_audio = True
        if global_audio:
            size = self.yt.streams.filter(only_audio=True).first().filesize
            decision = self.ui.ask_confirm_download(size)
        else:
            size = self.yt.streams.filter(
                res=self.streams_availabel_resolution_list[self.ix]).first().filesize
            decision = self.ui.ask_confirm_download(size)
        if decision:
            # download two section
            self.cc = self.color_list[random.randint(0, 5)]
            # Resizing of thumbnail_img
            self.thumbnaill2 = None
            try:
                self.thumbnaill2 = self.thumbnail_lab.image
            except Exception:
                pass

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
                                                     text=self.tittle_2, font=(None, 11, "bold"))
            self.file_title.place(x=190, y=10)

            self.downloaded_remaining2 = customtkinter.CTkLabel(master=self.frame_1, text=f"0mb of {size/ 1048576:0.2f}mb",
                                                                text_color=(self.bg_color), font=(None, 11, "bold"),
                                                                justify="left", relief="solid")
            self.downloaded_remaining2.place(x=355, y=40)
            self.download_percentage2 = customtkinter.CTkLabel(master=self.frame_1, text=f"0%",
                                                               text_color=(self.bg_color), font=(None, 11, "bold"),
                                                               justify="left", relief="solid")
            self.download_percentage2.place(x=670, y=40)

            self.file_progress_2 = customtkinter.CTkProgressBar(master=self.frame_1, width=500,
                                                                progress_color=(self.bg_color))
            self.file_progress_2.place(x=195, y=70)
            self.file_progress_2.set(0)
            try:
                outdir = self.ui.ask_save_dir()
                os.chdir(outdir)
                self.runningtask += 1
                if self.called == "1":
                    try:
                        self.downloaded_remaining2.config(text= "Waiting to download....")
                    except Exception:
                        pass
                self.called= "2"
                def progress_cb(stream, chunk, bytes_remaining):
                    bytes_downloaded = size - bytes_remaining
                    pct = int((bytes_downloaded / size) * 100) if size else 0
                    try:
                        self.file_progress_2.set(pct/100)
                        self.download_percentage2.configure(text=f"{pct}%")
                        self.downloaded_remaining2.configure(text=f"{bytes_downloaded / 1048576:0.2f}mb of {size/ 1048576:0.2f}mb")
                    except Exception:
                        pass

                if global_audio:
                    download_stream(self.yt, only_audio=True, output_path=outdir, progress_callback=progress_cb)
                else:
                    itag = self.streams_availabel_itag_list[self.ix]
                    download_stream(self.yt, itag=itag, output_path=outdir, progress_callback=progress_cb)
            except Exception:
                try:
                    self.downloaded_remaining2.configure(text="Download cancelled")
                except Exception:
                    pass
        else:
            print("Download cancelled")
            self.download_int -= 1

    def download_three(self):
        print(3)
        global_audio = False
        if self.ix == 'audio':
            global_audio = True
        if global_audio:
            size = self.yt.streams.filter(only_audio=True).first().filesize
            decision = self.ui.ask_confirm_download(size)
        else:
            size = self.yt.streams.filter(
                res=self.streams_availabel_resolution_list[self.ix]).first().filesize
            decision = self.ui.ask_confirm_download(size)
        if decision:
            self.cc = self.color_list[random.randint(0, 5)]
            self.thumbnaill3 = None
            try:
                self.thumbnaill3 = self.thumbnail_lab.image
            except Exception:
                pass
            self.file_thumbnail_3 = customtkinter.CTkLabel(master=self.frame_2b, text="", image=self.thumbnaill3,
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

            self.file_title = customtkinter.CTkLabel(master=self.frame_2b, justify="left", relief="solid",
                                                     text=self.tittle_3, font=(None, 11, "bold"))
            self.file_title.place(x=190, y=10)

            self.downloaded_remaining3 = customtkinter.CTkLabel(master=self.frame_2b, text=f"0mb of {size/ 1048576:0.2f}mb",
                                                                text_color=self.bg_color, font=(None, 11, "bold"),
                                                                justify="left", relief="solid")
            self.downloaded_remaining3.place(x=355, y=40)
            self.download_percentage3 = customtkinter.CTkLabel(master=self.frame_2b, text=f"0%",
                                                               text_color=self.bg_color, font=(None, 11, "bold"),
                                                               justify="left", relief="solid")
            self.download_percentage3.place(x=670, y=40)

            self.file_progress_3 = customtkinter.CTkProgressBar(master=self.frame_2b, width=500 ,progress_color=(self.bg_color))
            self.file_progress_3.place(x=195, y=70)
            self.file_progress_3.set(0)
            try:
                outdir = self.ui.ask_save_dir()
                os.chdir(outdir)
                self.runningtask += 1
                if self.called == "2":
                    try:
                        self.downloaded_remaining3.config(text= "Waiting to download....")
                    except Exception:
                        pass
                self.called= "3"
                def progress_cb(stream, chunk, bytes_remaining):
                    bytes_downloaded = size - bytes_remaining
                    pct = int((bytes_downloaded / size) * 100) if size else 0
                    try:
                        self.file_progress_3.set(pct/100)
                        self.download_percentage3.configure(text=f"{pct}%")
                        self.downloaded_remaining3.configure(text=f"{bytes_downloaded / 1048576:0.2f}mb of {size/ 1048576:0.2f}mb")
                    except Exception:
                        pass

                if global_audio:
                    download_stream(self.yt, only_audio=True, output_path=outdir, progress_callback=progress_cb)
                else:
                    itag = self.streams_availabel_itag_list[self.ix]
                    download_stream(self.yt, itag=itag, output_path=outdir, progress_callback=progress_cb)
            except Exception:
                try:
                    self.downloaded_remaining3.configure(text="Download cancelled")
                except Exception:
                    pass
        else:
            print("Download cancelled")
            self.download_int -= 1

    def build(self):
        self.title("Proxytube")
        self.geometry("850x700")
        self.resizable(0, 0)
        self.mainloop()


if __name__ == '__main__':
    AppNew().build()
