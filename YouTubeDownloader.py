import tkinter as tk
from tkinter import Frame, Label, Button, Text
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from PIL import ImageTk, Image
from urllib.request import urlopen, Request
from pytube import YouTube
import requests
from io import BytesIO
from bs4 import BeautifulSoup as bs
import tkinter.font as font
from tkinter import filedialog
from pytube import YouTube

class GUI:

    def __init__(self):

        def popUpInfo():
            tk.messagebox.showinfo("Information about the downloader","This is ......" + "\n" + "for extra information: **add github link here**")
        
        def downloadComplete():
            tk.messagebox.showinfo("Download complete!","Nice!")
        

        def error():
             tk.messagebox.showerror("Error!!!","INVALID URL LINK" + "\n" + "put a proper link")

        def browse_directory():
            # Allow user to select a directory and store it in global var
            # called folder_path
            filename = filedialog.askdirectory()
            directoryInput.configure(text=filename)

        def download():
            if (check_modified()):
                print('input text edited')
            else:
                inp = inputText.get('1.0', tk.END)
                print(inp)
                yt = YouTube(inp)
                yt.register_on_progress_callback(on_progress)
                yd = yt.streams.get_highest_resolution()
                dir = directoryInput.cget('text')
                print(dir)
                yd.download(dir)
                print('completed')
                downloadComplete()
        
        def check_modified():
            # If input url has been modified then disable the download button and make user type it again to avoid errors.
            # ask the widget if it has been modified
            if inputText.edit_modified():
                tk.messagebox.showinfo("unluggy", "Input URL has been changed, please retry")
                downloadBtn.configure(state='disabled')
                inputFrame.configure(background='pink')
                progressBarFrame.configure(background='pink')
                informationFrame.configure(background='pink')
                inputText.delete(1.0, "end-1c")
                return True

            # reset the flag to false. If the user modifies the widget the flag
            # will become True again
            inputText.edit_modified(False)
            return False

        # Initialises window
        self.root = tk.Tk()
        
        # Got icon from https://icon-icons.com/icon/social-media-youtube-video-play/128997
        self.root.iconbitmap('icon.ico') 

        # Setting resizeability
        self.root.resizable(False, False)

        # Set title of window
        self.root.title('YouTube Downloader')

        # This determines the size of the screen
        window_width = int(self.root.winfo_screenwidth()/1.3)
        window_height = int(self.root.winfo_screenheight()/1.3)

        # This gets the size of the monitor
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Coordinates of the upper left corner of the window to make the window appear in the center
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/1.85))
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        # Initial value of percentage
        percentage = '0%'

        # Have elements here -----
        
        # Frame for input
        inputFrame = Frame(self.root, background='pink')
        inputFrame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Progress bar at top with % text on the right side of the bar
        progressBarFrame = Frame(self.root, background='pink')
        progressBarFrame.pack(side=tk.TOP, fill=tk.BOTH)
        progressBar = ttk.Progressbar(progressBarFrame, orient='horizontal', length=int(window_width/1.1), mode='determinate')
        progressBar.pack(side='left',pady=20, padx=20)
        progressBarPercentage = Label(progressBarFrame, font='10', text=percentage)
        progressBarPercentage.pack(side='left')

        def on_progress(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage_of_completion = bytes_downloaded / total_size * 100
            inc=int(percentage_of_completion)
            print(inc)
            # progressBar.configure(value=inc)
            progressBar["value"]+=inc-progressBar["value"]
            progressBarPercentage.configure(text=inc)
            if progressBar["value"]==100:
                progressBar.grid_forget()
                progressBarPercentage.grid_forget()
            # progressBarPercentage["text"]="100%"
        
        # Frame for information
        informationFrame = Frame(self.root, background='pink')
        informationFrame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Information button
        infoIcon = ImageTk.PhotoImage(Image.open("info.ico"))
        InfoBtn = Button(inputFrame, command=popUpInfo, borderwidth= 0, image=infoIcon, width=40, height=40)
        InfoBtn.image = infoIcon
        InfoBtn.pack(padx=10, pady=10)

        # URL input
        inputText = Text(inputFrame, height = 1, width = 100, borderwidth=2)
        inputText.pack(pady=10)

        # Function for getting URL input from user
        def inputURL():
            urlInput = inputText.get(1.0, tk.END) # "end-1c"
            inputText.edit_modified(False)
            try:
                yt = YouTube(urlInput)
                yt.check_availability()
                downloadBtn.configure(state='active')
                inputFrame.configure(background='lightgreen')
                progressBarFrame.configure(background='lightgreen')
                informationFrame.configure(background='lightgreen')

                titleLabel.configure(text= "Title: " + yt.title)

                vidLengthMins = int(yt.length / 60)
                vidLengthSecs = yt.length % 60
                min = str(vidLengthMins)
                sec = str(vidLengthSecs)
                vidLength = (min + ":" + sec)
                lengthLabel.configure(text="Length of video: " + vidLength)
                
                viewsStr = str(yt.views)
                viewLabel.configure(text="Number of views: " + viewsStr)

                dateStr = str(yt.publish_date)
                dateLabel.configure(text="Published date: " + dateStr)

                channelIDLabel.configure(text="Channel ID: " + yt.channel_id)

                thumbnailImgUrl = yt.thumbnail_url   
                # Alternative way to get data   
                # u = urlopen(thumbnailImgUrl)
                # raw_data = u.read()
                # u.close()
                response = requests.get(thumbnailImgUrl)
                img_data = response.content
                thumbnailImg = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
                label.configure(image=thumbnailImg)
                label.image = thumbnailImg 

                url_opener = urlopen(Request(urlInput))
                videoInfo = bs(url_opener, features='html.parser')
                channelName = str(videoInfo.find("link", itemprop="name"))
                channelNameStr = channelName[len('<link content="'):-len('" itemprop="name"/>')]
                channelNameLabel.configure(text="Name of channel: " + channelNameStr)

            except:
                print("error")
                downloadBtn.configure(state='disabled')
                inputFrame.configure(background='pink')
                progressBarFrame.configure(background='pink')
                informationFrame.configure(background='pink')
                error()
            
        #Button for submitting URL for checking validity
        submitBtn = Button(inputFrame, text='Submit YouTube URL', command=inputURL)
        submitBtn.pack(pady=5)

        # Label for directory
        directoryLabel = Label(inputFrame, text='Choose directory')
        directoryLabel.pack()

        # Button for browsing directory 
        directoryBtn = Button(inputFrame, text='browse', command=browse_directory)
        directoryBtn.pack(pady=5)
        # Input for which directory to save in 
        directoryInput = Label(inputFrame, height=1, width=100, borderwidth=2)
        directoryInput.pack()

        # Button for downloading submitted video --- try/catch for chosen directory
        downloadBtn = Button(inputFrame, text='DOWNLOAD', state='disabled', font=font.Font(size=30), fg='black', command=download)
        downloadBtn.pack(pady=30, side=tk.BOTTOM)

        img = ImageTk.PhotoImage(Image.open("image.png"))  
        label = Label(informationFrame, image=img)
        label.image = img
        label.pack()
        
        titleLabel = Label(informationFrame, text='Title: ')
        titleLabel.pack()
        channelNameLabel = Label(informationFrame, text='Name of channel: ')
        channelNameLabel.pack()
        lengthLabel = Label(informationFrame, text='Length of video: ')
        lengthLabel.pack()
        viewLabel = Label(informationFrame, text='Number of views: ')
        viewLabel.pack()
        dateLabel = Label(informationFrame, text='Published date: ')
        dateLabel.pack()
        channelIDLabel = Label(informationFrame, text='Channel ID: ')
        channelIDLabel.pack()

        self.root.mainloop()

    

GUI()