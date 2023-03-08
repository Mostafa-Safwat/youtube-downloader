import ttkbootstrap as tk
from tkinter import filedialog, ttk
import yt_dlp
from threading import Thread

root = tk.Window(themename="superhero")
root.title('Youtube Downloader')

current_var = tk.StringVar()
combobox = ttk.Combobox(root, textvariable=current_var)
combobox['values'] = ('320', '480', '720', '1080')

labelcombo = tk.Label(root, text="Quality: ")
labelcombo.grid(row=2, column=0)
combobox.grid(row=2, column=1)

def choose_link():
    text = text_field.get()    
    return text

label = tk.Label(root, text="Enter a link:")
text_field = tk.Entry(root)

label.grid(row=0, column=0)
text_field.grid(row=0, column=1)

directory_path = tk.StringVar()

def choose_path():
    directory_path.set (filedialog.askdirectory())
    directory_label.config(text = directory_path.get())
    return directory_path
    
def download(download_path, download_link, download_resolution):
    ydl_opts = {
    'format': 'best[height<='+download_resolution+']',
    'outtmpl': download_path + '/%(title)s.%(ext)s',
    }
    print(download_path)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['{}'.format(download_link)])

def startDownloadThread():
    downloadThread = Thread(target=download, args=(directory_path.get(), choose_link(), current_var.get()))
    downloadThread.start()


choose_button = tk.Button(root, text="Choose Directory Path", command=choose_path)
choose_button.grid(row=1, column=1)

directory_label = tk.Label(root, text="No directory path selected")
directory_label.grid(row=1, column=0)

button = tk.Button(root, text="Download", command=startDownloadThread)
button.grid(row=3, column=1)


root.mainloop()
