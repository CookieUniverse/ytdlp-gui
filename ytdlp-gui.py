import tkinter as tk
from tkinter import BOTH, BOTTOM, LEFT, RIGHT, TOP, filedialog, NONE
import os
import yt_dlp
from PIL import Image
import customtkinter as CTk
from urllib.parse import urlparse, parse_qs
from urllib.request import urlretrieve
import darkdetect
import tempfile
import pyglet

def defineConstants():
    global os, user, path
    path = f"{tempfile.gettempdir()}/tempthumb.png"
    user = os.getlogin
    if (os.name == "nt"):
        os = "win"
    else:
        os = "other"

class CenterFrame(CTk.CTkFrame):
    def __init__(self, m):
        super().__init__(m)

    def close(self):
        self.destroy()

class checkInfo():
    def __init__(self, link):
        ydl_opts = {
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(link, download=False)
            formats = result.get('formats', [result])

            if 'entries' in result:
                video = result['entries'][0]

            else:
                video = result

            self.ar = [
                "298",
                "299",
                "398",
                "399",
                "400",
                "401",
                "271",
                "308",
                "313",
                "315",
                "136",
                "137",
                "397",
                "396",
                "395",
                "394",
                "135",
                "134",
                "133",
                "160",
                "571"
            ]

            self.ar2 = [
                "140",
                "251",
                "250",
                "249",
                "139"
            ]

            self.ar3 = [
                "298",
                "299",
                "398",
                "399",
                "400",
                "401",
                "271",
                "308",
                "313",
                "315",
                "136",
                "137",
                "397",
                "396",
                "395",
                "394",
                "135",
                "134",
                "133",
                "160",
                "571",
                "140",
                "251",
                "250",
                "249",
                "139"
            ]

            self.arposvid = []
            self.arposaud = []
            self.arpospl = []

            for f in formats:

                fid = f['format_id']

                if fid in self.ar:
                    formatsvid = f"{fid}"
                    pos = self.ar.index(formatsvid)
                    self.arposvid.append(pos)
                if fid in self.ar2:
                    formatsaud = f"{fid}"
                    pos = self.ar2.index(formatsaud)
                    self.arposaud.append(pos)
                if fid in self.ar3:
                    formatspl = f"{fid}"
                    pos = self.ar3.index(formatspl)
                    self.arpospl.append(pos)

            self.video_title = video['title']
            self.video_channel = video['channel']
            self.durationraw = video['duration']
            self.views = video['view_count']

class MainFrame(CTk.CTkFrame):
    def __init__(self, m):
        super().__init__(m)
        self.pack(fill=BOTH, expand=True)
        centerFrame = CenterFrame(self)
        centerFrame.place(relx=0.5, rely=0.5, anchor='center')
        linkInput = CTk.CTkEntry(centerFrame, width=500)
        linkInput.grid()

        def setVideoLink():
            self.videoLink=linkInput.get()

        dButton = CTk.CTkButton(centerFrame, text="Download", width=150, height=40, font=CTk.CTkFont(
            "Calibri", 30), command=lambda: [setVideoLink(), videoInfo(self.videoLink, centerFrame, m)])
        if (darkdetect.isDark()):
            dButton.configure(text_color="Black", image=CTk.CTkImage(
                Image.open("images/arrow-dark.png")))
        else:
            dButton.configure(image=CTk.CTkImage(
                Image.open("images/arrow-light.png")))
        dButton.grid(pady=100)

class MainWindow(CTk.CTk):
    def __init__(self):
        super().__init__()
        CTk.set_appearance_mode("System")
        self.geometry("850x750")
        self.title(string="Youtube Video Downloader")
        self.resizable(False, False)
        if os == "win":
            self.wm_iconbitmap(bitmap="images/icon.ico")
            self.iconbitmap("images/icon.ico")
        else:
            icon = tk.PhotoImage(file='images/icon.png')
            self.tk.call('wm', 'iconphoto', root._w, icon)
        pyglet.font.add_file("fonts/ConfigRoundedMedium.ttf")
        self.startFrame()

        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.mainloop()

    def startFrame(self):
        self.counter = 0
        self.mainFrame = MainFrame(self)
        bottomFrame = CTk.CTkFrame(self.mainFrame)
        bottomFrame.pack(pady=14, side=BOTTOM)

        rButton = CTk.CTkButton(bottomFrame, text="Reset", font=CTk.CTkFont("Calibri", 30), width=100, height=40, command=lambda: [self.reset()])
        rButton.grid()

    def closing(self):
        self.destroy()

    def reset(self):
        self.mainFrame.destroy()
        self.startFrame()

    def videoInfoFrame(self, link):
        self.frame = CenterFrame(self.mainFrame)
        self.frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

        frameBottomText = CTk.CTkFrame(self.frame)
        frameBottomText.pack(side=BOTTOM, pady=5)
        self.frameBottomBar = CTk.CTkFrame(self.frame, height=38, width=0)
        self.frameBottomBar.pack(side=BOTTOM, fill="none")
        frameLeft = CTk.CTkFrame(self.frame)
        frameLeft.pack(side=LEFT, pady=10)
        self.mainFrameRight = CTk.CTkFrame(self.frame)
        self.mainFrameRight.pack(side=RIGHT, padx=10)

        img = Image.open(path)
        thumbfinal = CTk.CTkImage(img, size=(496, 279))
        thumb = CTk.CTkLabel(frameLeft, image=thumbfinal, text="")
        thumb.image = thumbfinal
        thumb.pack(side=LEFT)
        self.videoInfo = checkInfo(link)
        tFont = CTk.CTkFont(family="Config Rounded Medium", size=19)
        videoTitleLabel = CTk.CTkLabel(
            frameBottomText, text=self.videoInfo.video_title, font=tFont)
        videoChannelLabel = CTk.CTkLabel(
            frameBottomText, text=f"From: {self.videoInfo.video_channel}", font=tFont)
        videoDurationLabel = CTk.CTkLabel(
            frameBottomText, font=tFont)
        videoViewsLabel = CTk.CTkLabel(
            frameBottomText, font=tFont)
        checkDuration(self.videoInfo.durationraw, videoDurationLabel)
        checkViews(self.videoInfo.views, videoViewsLabel)

        videoViewsLabel.pack(side=BOTTOM)
        videoDurationLabel.pack(side=BOTTOM)
        videoChannelLabel.pack(side=BOTTOM)
        videoTitleLabel.pack(side=BOTTOM)

        self.downloadOptsBox = CTk.CTkComboBox(self.mainFrameRight, state="disabled", width=267, command=self.getChoiceBox)
        self.downloadOptsBox.grid()

        self.mainFrameBottom = CTk.CTkFrame(self.mainFrame)
        self.mainFrameBottom.pack(side=BOTTOM)

        def whichButton(opt):
            self.buttonClicked = opt

        self.videoButton = CTk.CTkButton(self.mainFrameBottom, text="Video", font=CTk.CTkFont("Calibri", 30), 
            width=70, command=lambda opt="Video":[self.destroyOpts(), whichButton(opt), self.loadOptsBox(), self.loadOtherOpts()])
        self.audioButton = CTk.CTkButton(self.mainFrameBottom, text="Audio", font=CTk.CTkFont("Calibri", 30), 
            width=70, command=lambda opt="Audio":[self.destroyOpts(), whichButton(opt), self.loadOptsBox(), self.loadOtherOpts()])
        self.plButton = CTk.CTkButton(self.mainFrameBottom, text="Playlist", font=CTk.CTkFont("Calibri", 30), 
            width=70, command=lambda opt="Playlist":[whichButton(opt), self.loadOptsBox()])
        self.videoButton.grid(row=1, column=0, padx=10)
        self.audioButton.grid(row=1,column=1, padx=10)
        self.plButton.grid(row=1, column=2, padx=10)

    def getChoiceBox(self, choice):
        self.selected = f"{choice}"
        match self.buttonClicked:
            case "Video":
                self.optIdx = self.aroptallvid.index(self.selected)
            case "Audio":
                self.optIdx = self.aroptallaud.index(self.selected)
            case "Playlist":
                self.optIdx = self.aroptallpl.index(self.selected)

    def destroyOpts(self):
        self.videoButton.destroy()
        self.audioButton.destroy()
        self.plButton.destroy()
    
    def loadOptsBox(self):
        match self.buttonClicked:
            case "Video":
                self.aroptallvid = [
                    '720P 60fps (.mp4)',
                    '1080P 60fps (.mp4)',
                    '720P 30fps (.mp4) (2)',
                    '1080P 30fps (.mp4) (2)',
                    '1440P 60/30fps (.mp4)',
                    '4K 60/30fps (.mp4)',
                    '1440P 30fps (.webm)',
                    '1440P 60fps (.webm)',
                    '4K 30fps (.webm)',
                    '4K 60fps (.webm)',
                    '720P 30fps (.mp4) (1)',
                    '1080P 30fps (.mp4) (1)',
                    '480P 30fps (.mp4) (2)',
                    '360P 30fps (.mp4) (2)',
                    '240P 30fps (.mp4) (2)',
                    '144P 30fps (.mp4) (2)',
                    '480P 30fps (.mp4) (1)',
                    '360P 30 fps (.mp4) (1)',
                    '240P 30 fps (.mp4) (1)',
                    '144P 30fps (.mp4) (1)',
                    '8K 30fps (.mp4)'
                ]
                
                aroptvid = []

                for i in self.videoInfo.arposvid:
                    aux = self.aroptallvid[i]
                    aroptvid.append(aux)

                self.downloadOptsBox.configure(values=aroptvid, state="normal")

            case "Audio":
                self.aroptallaud = [
                    'GOOD (AAC Encoder) (.m4a)',
                    'GOOD (OPUS Encoder) (.mp3)',
                    'MEDIUM (OPUS Encoder) (.mp3)',
                    'LOW (OPUS Encoder) (.mp3)',
                    'LOW (AAC Encorder) (.m4a)'
                ]

                aroptaud = []

                for i in self.videoInfo.arposaud:
                    aux = self.aroptallaud[i]
                    aroptaud.append(aux)
                
                self.downloadOptsBox.configure(values=aroptaud, state="normal")

            case "Playlist":
                try:
                        
                    with yt_dlp.YoutubeDL({}) as ydl:
                        resultpl = ydl.extract_info(self.mainFrame.videoLink, download=False)

                    if 'entries' in resultpl:
                        self.vidNum = len(resultpl['entries'])

                    if self.vidNum == 0:
                        raise Exception

                except:
                    tk.messagebox.showerror(title="Error", message="No playlist detected")
                
                else:
                    self.destroyOpts()
                    self.loadOtherOpts()
                    plthumblink = resultpl['thumbnails'][1]['url']
                    pltitle = resultpl['title']

                    self.aroptallpl = [
                        '720P 60fps (.mp4)',
                        '1080P 60fps (.mp4)',
                        '720P 30fps (.mp4) (2)',
                        '1080P 30fps (.mp4) (2)',
                        '1440P 60/30fps (.mp4)',
                        '4K 60/30fps (.mp4)',
                        '1440P 30fps (.webm)',
                        '1440P 60fps (.webm)',
                        '4K 30fps (.webm)',
                        '4K 60fps (.webm)',
                        '720P 30fps (.mp4) (1)',
                        '1080P 30fps (.mp4) (1)',
                        '480P 30fps (.mp4) (2)',
                        '360P 30fps (.mp4) (2)',
                        '240P 30fps (.mp4) (2)',
                        '144P 30fps (.mp4) (2)',
                        '480P 30fps (.mp4) (1)',
                        '360P 30 fps (.mp4) (1)',
                        '240P 30 fps (.mp4) (1)',
                        '144P 30fps (.mp4) (1)',
                        '8K 30fps (.mp4)',
                        'GOOD (AAC Encoder) (.m4a)',
                        'GOOD (OPUS Encoder) (.mp3)',
                        'MEDIUM (OPUS Encoder) (.mp3)',
                        'LOW (OPUS Encoder) (.mp3)',
                        'LOW (AAC Encorder) (.m4a)'
                    ]

                    aroptpl = []

                    for i in self.videoInfo.arpospl:
                        aux = self.aroptallpl[i]
                        aroptpl.append(aux)

                    self.downloadOptsBox.configure(values=aroptpl, state="normal")

    def loadOtherOpts(self):
        self.embedState = 0
        def checkState():
            self.embedState = embedThumbOpt.get()

        embedThumbOpt = CTk.CTkCheckBox(self.mainFrameRight, text="Embed Thumbnail", command=checkState)
        embedThumbOpt.grid()

        dButton = CTk.CTkButton(self.mainFrameBottom, text="Download", width=150, height=40, font=CTk.CTkFont(
            "Calibri", 30), command=lambda:[self.download()])
        dButton.grid()

    def download(self):
        try:
            if self.optIdx is None:
                raise Exception
        except:
            tk.messagebox.showerror(title="Error", message="Please Specify a Format")
        else:
            ydl_opts = {
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.mainFrame.videoLink, download=False)
                fileName = ydl.prepare_filename(info)

            fileSplit = fileName.split(f" [{video_id}")[0]
            self.checkFormats()
            match self.buttonClicked:
                case "Playlist":
                    self.saveAs = filedialog.askdirectory()
                    if not self.saveAs:
                        return
                case _:
                    self.saveAs = filedialog.asksaveasfilename(initialfile=f"{fileSplit}", defaultextension=f".{self.format}", 
                        confirmoverwrite=False, filetypes=[(f"{self.buttonClicked}", f".{self.format}"), ("All Files", "*.*")])
                    if not self.saveAs:
                        return

            self.defineOpts()
            
            self.startBar()

            with yt_dlp.YoutubeDL(self.dOptions) as ydl:
                ydl.download(self.mainFrame.videoLink)

            self.counter = 0
            self.perLabel.destroy()
            self.progress.destroy()
            self.frameBottomBar.configure(width=0)

    def checkFormats(self):
        #arMp4 = ['298','299','398', '399', '400', '401', '136', '137', '394', '395', '396', '397','133','134','135','160','571']
        arWebmVid = [
            '271', 
            '308', 
            '313', 
            '315'
            ]
        arWebmAud = [
            '251',
            '250',
            '249'
        ]
        arM4a = [
            '139',
            '140'
            ]

        match self.buttonClicked:
            case "Video":
                self.optNum = self.videoInfo.ar[self.optIdx]
            case "Audio":
                self.optNum = self.videoInfo.ar2[self.optIdx]
            case "Playlist":
                self.optNum = self.videoInfo.ar3[self.optIdx]

        if self.optNum in arM4a:
            self.format = "m4a"
        elif self.optNum in arWebmVid:
            self.format = "webm"
        elif self.optNum in arWebmAud:
            self.format = "mp3"
        else:
            self.format = "mp4"

    def defineOpts(self):
        match self.buttonClicked:
            case "Video":
                self.limit=2
                if self.format == "mp4":
                    self.audioFormat = "m4a"
                else:
                    self.audioFormat = "webm"
                if self.embedState == 1:
                    self.dOptions = {
                        'format': f'{self.videoInfo.ar[self.optIdx]}+bestaudio[ext={self.audioFormat}]',
                        'writethumbnail': True,
                        'noplaylist': True,
                        'continue': True,
                        'outtmpl': f'{self.saveAs}',
                        'progress_hooks': [self.hook],
                        'postprocessors': [
                            {'key': 'FFmpegMetadata', 'add_metadata': 'True'},
                            {'key': 'EmbedThumbnail', 'already_have_thumbnail': False, }
                        ]
                    }
                else:
                    self.dOptions = {
                        'format': f'{self.videoInfo.ar[self.optIdx]}+bestaudio[ext={self.audioFormat}]',
                        'writethumbnail': False,
                        'noplaylist': True,
                        'continue': True,
                        'outtmpl': f'{self.saveAs}',
                        'progress_hooks': [self.hook],
                        'postprocessors': [
                            {'key': 'FFmpegMetadata', 'add_metadata': 'True'}
                        ]
                    }

            case "Audio":
                self.limit=1
                if self.embedState == 1:
                    self.dOptions = {
                        'format': f'{self.videoInfo.ar2[self.optIdx]}',
                        'writethumbnail': True,
                        'noplaylist': True,
                        'continue': True,
                        'outtmpl': f'{self.saveAs}',
                        'progress_hooks': [self.hook],
                        'audioformat': f"{self.format}",
                        'postprocessors': [
                            {'key': 'FFmpegExtractAudio', 'preferredcodec': f'{self.format}'},
                            {'key': 'FFmpegMetadata', 'add_metadata': 'True'},
                            {'key': 'EmbedThumbnail',
                                'already_have_thumbnail': False, }
                        ]
                    }
                else:
                    self.dOptions = {
                        'format': f'{self.videoInfo.ar2[self.optIdx]}',
                        'writethumbnail': False,
                        'noplaylist': True,
                        'continue': True,
                        'outtmpl': f'{self.saveAs}',
                        'progress_hooks': [self.hook],
                        'audioformat': f"{self.format}",
                        'postprocessors': [
                            {'key': 'FFmpegExtractAudio', 'preferredcodec': f'{self.format}'},
                            {'key': 'FFmpegMetadata', 'add_metadata': 'True'},
                        ]
                    }

            case "Playlist":
                self.limit = self.vidNum
                if self.format == "mp4":
                    self.audioFormat = "m4a"
                else:
                    self.audioFormat = self.format
                
                arWebmAudio = ['249', '250']
                match self.format:
                    case "mp4":
                        if self.embedState == 1:
                            self.dOptions = {
                                'format': f'{self.videoInfo.ar[self.optIdx]}+bestaudio[ext={self.audioFormat}]',
                                'writethumbnail': True,
                                'continue': True,
                                'outtmpl': f'{self.saveAs}/%(title)s.%(ext)s',
                                'progress_hooks': [self.hook],
                                'postprocessors': [
                                    {'key': 'FFmpegMetadata', 'add_metadata': 'True'},
                                    {'key': 'EmbedThumbnail',
                                        'already_have_thumbnail': False, }
                                ]
                            }
                        else:
                            self.dOptions = {
                                'format': f'{self.videoInfo.ar[self.optIdx]}+bestaudio[ext={self.audioFormat}]',
                                'writethumbnail': False,
                                'continue': True,
                                'outtmpl': f'{self.saveAs}/%(title)s.%(ext)s',
                                'progress_hooks': [self.hook],
                                'postprocessors': [
                                    {'key': 'FFmpegMetadata', 'add_metadata': 'True'}
                                ]
                            }
                    case "m4a":
                        if self.embedState == 1:
                            self.dOptions = {
                                'format': f'{self.videoInfo.ar2[self.optIdx]}',
                                'writethumbnail': True,
                                'continue': True,
                                'outtmpl': f'{self.saveAs}/%(title)s.%(ext)s',
                                'progress_hooks': [self.hook],
                                'audioformat': f"{self.format}",
                                'postprocessors': [
                                    {'key': 'FFmpegExtractAudio', 'preferredcodec': f'{self.format}'},
                                    {'key': 'FFmpegMetadata', 'add_metadata': 'True'},
                                    {'key': 'EmbedThumbnail',
                                        'already_have_thumbnail': False, }
                                ]
                            }
                        else:
                            self.dOptions = {
                                'format': f'{self.videoInfo.ar2[self.optIdx]}',
                                'writethumbnail': False,
                                'continue': True,
                                'outtmpl': f'{self.saveAs}/%(title)s.%(ext)s',
                                'progress_hooks': [self.hook],
                                'audioformat': f"{self.format}",
                                'postprocessors': [
                                    {'key': 'FFmpegExtractAudio', 'preferredcodec': f'{self.format}'},
                                    {'key': 'FFmpegMetadata', 'add_metadata': 'True'},
                                ]
                            }
                    case "webm":
                        if self.format in arWebmAudio:
                            if self.embedState == 1:
                                self.dOptions = {
                                    'format': f'{self.videoInfo.ar2[self.optIdx]}',
                                    'writethumbnail': True,
                                    'continue': True,
                                    'outtmpl': f'{self.saveAs}/%(title)s.%(ext)s',
                                    'progress_hooks': [self.hook],
                                    'audioformat': f"{self.format}",
                                    'postprocessors': [
                                        {'key': 'FFmpegExtractAudio',
                                            'preferredcodec': f'{self.format}'},
                                        {'key': 'FFmpegMetadata',
                                            'add_metadata': 'True'},
                                        {'key': 'EmbedThumbnail',
                                            'already_have_thumbnail': False, }
                                    ]
                                }
                            else:
                                self.dOptions = {
                                    'format': f'{self.videoInfo.ar2[self.optIdx]}',
                                    'writethumbnail': False,
                                    'continue': True,
                                    'outtmpl': f'{self.saveAs}/%(title)s.%(ext)s',
                                    'progress_hooks': [self.hook],
                                    'audioformat': f"{self.format}",
                                    'postprocessors': [
                                        {'key': 'FFmpegExtractAudio',
                                            'preferredcodec': f'{self.format}'},
                                        {'key': 'FFmpegMetadata',
                                            'add_metadata': 'True'},
                                    ]
                                }
                        else:
                            if self.embedState == 1:
                                self.dOptions = {
                                    'format': f'{self.videoInfo.ar[self.optIdx]}+bestaudio[ext={self.audioFormat}]',
                                    'writethumbnail': True,
                                    'continue': True,
                                    'outtmpl': f'{self.saveAs}/%(title)s.%(ext)s',
                                    'progress_hooks': [self.hook],
                                    'postprocessors': [
                                        {'key': 'FFmpegMetadata',
                                            'add_metadata': 'True'},
                                        {'key': 'EmbedThumbnail',
                                            'already_have_thumbnail': False, }
                                    ]
                                }
                            else:
                                self.dOptions = {
                                    'format': f'{self.videoInfo.ar[self.optIdx]}+bestaudio[ext={self.audioFormat}]',
                                    'writethumbnail': False,
                                    'continue': True,
                                    'outtmpl': f'{self.saveAs}/%(title)s.%(ext)s',
                                    'progress_hooks': [self.hook],
                                    'postprocessors': [
                                        {'key': 'FFmpegMetadata',
                                            'add_metadata': 'True'}
                                    ]
                                }

    def startBar(self):
        self.progress = CTk.CTkProgressBar(
            self.frameBottomBar, orientation="horizontal", width=400, height=10)
        self.progress.set(0)
        self.progress.pack(side=BOTTOM)

        self.perLabel = CTk.CTkLabel(self.frameBottomBar, text="0%", font=CTk.CTkFont(family="Config Rounded Medium"))
        self.perLabel.pack(side=TOP)

    def hook(self, d):
        if d['status'] == 'downloading':
            try:
                downloaded_percent = (d["downloaded_bytes"])/d["total_bytes"]
            except:
                downloaded_percent = (d["downloaded_bytes"])/d["total_bytes_estimate"]

            self.progress.set(downloaded_percent)
            self.progress.update_idletasks()
            percent = round((downloaded_percent * 100), 2)
            self.perLabel.configure(text=f"{percent}%")
            self.perLabel.update_idletasks()

        if d['status'] == 'finished':
            self.counter += 1
            if self.counter == self.limit:
                tk.messagebox.showinfo(
                    title="Download", message="Your file has been downloaded.")

def videoInfo(link, frame, root):
    global video_id
    try:
        video_id = parse_qs(urlparse(link).query)['v'][0]
        try:
            thumblink = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
            urlretrieve(thumblink, path)
        except:
            thumblink = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
            urlretrieve(thumblink, path)
    except:
        tk.messagebox.showerror(title="Error", message="Invalid URL")
    else:
        frame.close()
        root.videoInfoFrame(link)

def checkDuration(duration, label):
    import datetime
    if duration < 60:
        label.configure(text=f"Duration: {duration} seconds")
    else: 
        if duration >= 60 and duration < 3600:
            duration = str(datetime.timedelta(seconds=duration))
            minutes = int(duration.split(":")[1])
            seconds = int(duration.split(":")[2])
            if seconds < 10:
                label.configure(text=f"Duration: {minutes}:0{seconds} min")
            else:
                label.configure(text=f"Duration: {minutes}:{seconds} min")
        else:
            if duration >= 3600:
                duration = str(datetime.timedelta(seconds=duration))
                hours = int(duration.split(":")[0])
                minutes = int(duration.split(":")[1])
                seconds = int(duration.split(":")[2])
                if seconds < 10:
                    label.configure(text=f"Duration: {hours}:{minutes}:0{seconds} hours")
                else:
                    label.configure(text=f"Duration: {hours}:{minutes}:{seconds} hours")

def checkViews(views, label):
        if views < 1000:
           label.configure(text=f"Views: {views}")

        if views >= 1000 and views < 1000000:
            views = round(views/1000)
            label.configure(text=f"Views: {views}K")

        if views >= 1000000:
            views = round(views/1000000, 1)
            label.configure(text=f"Views: {views}M")

if __name__ == "__main__":
    defineConstants()
    root = MainWindow()
