import pytube as pt
import os
import tkinter as tk
import customtkinter
import threading

def startDownload():
    # Create a new thread for the download operation
    download_thread = threading.Thread(target=downloadVideo)
    # Start the new thread
    download_thread.start()

# Quality options
quality = ["720p", "480p", "360p", "240p", "144p"]


# Download the video
def downloadVideo():
    try:
        url = link.get()
        yt = pt.YouTube(url, on_progress_callback=on_progress)
        video = yt.streams.filter(progressive=True, file_extension="mp4", res=quality).first()
        title.configure(text=yt.title)
        video.download(os.getcwd())
    except Exception as e:
        finished.configure(text="An error occurred", text_color="red")
        print(e)

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    percent.configure(text=per + "%")
    percent.update()

    # Update the progress bar
    progress_bar.set(float(percentage_of_completion) / 100)
    if percentage_of_completion == 100:
        progress_bar.configure(progress_color="green")


# Light/Dark mode:
def theme():
    if customtkinter.get_appearance_mode() == "Light":
        customtkinter.set_appearance_mode("dark")
        mode.configure(image=dark_icon)
    else:
        customtkinter.set_appearance_mode("light")
        mode.configure(image=light_icon)

# Create the main window
app = customtkinter.CTk()

dark_icon = tk.PhotoImage(file="assets/light.png")
light_icon = tk.PhotoImage(file="assets/dark.png")

# Main window settings
app.title("YouTube Downloader")
app.geometry("720x480")
app.resizable(False, False)
app.grid_columnconfigure(0, weight=1)

# Title
title = customtkinter.CTkLabel(app, text="Insert a youtube link")
title.grid(row=1, column=0, padx=10, pady=10)

# Light/Dark mode button
mode = customtkinter.CTkButton(app, width=1, image="", text="", fg_color= "transparent", command=theme)
mode.grid(row=1, column=0, padx=10, pady=1, sticky="e")

theme()
    
# Link input
url_var = tk.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.grid(row=2, column=0, padx=0, pady=10)

# Quality combobox
resolution = customtkinter.CTkComboBox(app, width=110, height=40, values=quality, state="readonly")
resolution.grid(row=2, column=0, padx=(0,70), pady=0, sticky="e")

# Download button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.grid(row=3, column=0, padx=20, pady=20)

# Progress bar
percent = customtkinter.CTkLabel(app, text="0%")
percent.grid(row=4, column=0, padx=10, pady=10)

progress_bar = customtkinter.CTkProgressBar(app, width=350, progress_color="blue")
progress_bar.set(0)
progress_bar.grid(row=5, column=0, padx=10, pady=10)

# Finished Downloading
finished = customtkinter.CTkLabel(app, text="")
finished.grid(row=6, column=0, padx=10, pady=10)


app.mainloop()