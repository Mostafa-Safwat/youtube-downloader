import pytube as pt
import os
import tkinter as tk
import customtkinter
import threading
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import re
from PIL import Image, ImageTk

#TODO add an icon to the app
#TODO try and fix some videos that does not have stream
#TODO make it so that the user can choose the download location
#TODO add an option to download only the audio

def startDownload():
    # Create a new thread for the download operation
    download_thread = threading.Thread(target=downloadVideo)
    # Start the new thread
    download_thread.start()

# Quality options
quality_choice = ["1080p", "720p", "480p", "360p", "240p", "144p"]

def choice(event):
    global quality
    quality = resolution.get()

# Download the video
def downloadVideo():
    try:
        url = link.get()
        if 'playlist' in url:
            for video in pt.Playlist(url).video_urls:
                download_video(video)
        else:
            download_video(url)
    except Exception as e:
        finished.configure(text="An error occurred", text_color="red")
        print(e)

def download_video(url):
    yt = pt.YouTube(url, on_progress_callback=on_progress)
    quality_index = quality_choice.index(quality)
    for i in range(quality_index, len(quality_choice)):
        video_stream = yt.streams.filter(mime_type="video/mp4", res=quality_choice[i]).first()
        audio_stream = yt.streams.filter(mime_type="audio/webm").first()
        if video_stream:
            break
    title.configure(text=yt.title)
    video_filename = re.sub(r"[\/:*?\"<>|]", "", yt.title)  # Remove invalid characters

    progress_bar.set(0)
    percent.configure(text="0%")
    progress_bar.configure(progress_color="blue")

    video_stream.download(os.getcwd(), filename="video.mp4")
    audio_stream.download(os.getcwd(), filename="audio.webm")
    video_clip = VideoFileClip("video.mp4")
    audio_clip = AudioFileClip("audio.webm")
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(f"{video_filename}.mp4")
    # Close the clips
    video_clip.close()
    audio_clip.close()
    final_clip.close()
    # Delete the temporary files
    os.remove("audio.webm")
    os.remove("video.mp4")

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
        finished.configure(text="")
    else:
        progress_bar.configure(progress_color="blue")


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

app.iconbitmap('youtube.png')

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
resolution = customtkinter.CTkComboBox(app, width=110, height=40, values=quality_choice, state="readonly", command=choice)
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