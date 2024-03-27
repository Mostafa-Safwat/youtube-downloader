import os
import re
import threading
import tkinter as tk
import subprocess
import pytube as pt
import customtkinter

ffmpeg_path = os.path.join(os.path.dirname(__file__), 'bin', 'ffmpeg')
quality_choice = ["1080p", "720p", "480p", "360p", "240p", "144p"]
loc = os.getcwd()
playlist_loc = loc

def startDownload():
    download_thread = threading.Thread(target=downloadVideo)
    download_thread.start()

def downloadVideo():
    global loc
    global playlist_loc
    try:
        url = link.get()
        if 'playlist' in url:
            playlist_title = pt.Playlist(url).title
            os.makedirs(os.path.join(loc, playlist_title))
            playlist_loc = os.path.join(loc, playlist_title)
            for video in pt.Playlist(url).video_urls:
                download_video(video, playlist_loc)
        else:
            download_video(url, loc)
    except Exception as e:
        finished.configure(text="An error occurred", text_color="red")
        print(e)

# Download the video
def downloadVideo():
    global loc
    global playlist_loc
    try:
        url = link.get()
        if 'playlist' in url:
            playlist_title = pt.Playlist(url).title
            os.makedirs(os.path.join(loc, playlist_title))
            playlist_loc = os.path.join(loc, playlist_title)
            for video in pt.Playlist(url).video_urls:
                download_video(video, playlist_loc)
        else:
            download_video(url, loc)
    except Exception as e:
        finished.configure(text="An error occurred", text_color="red")
        print(e)

def download_video(url, download_location):
    global ffmpeg_path
    global startupinfo

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    yt = pt.YouTube(url, on_progress_callback=on_progress)
    quality_index = quality_choice.index(quality)
    for i in range(quality_index, len(quality_choice)):
        video_stream = yt.streams.filter(mime_type="video/mp4", res=quality_choice[i]).first()
        audio_stream = yt.streams.filter(type="audio").first()
        if video_stream:
            break
    title.configure(text=yt.title)
    video_filename = re.sub(r"[\/:*?\"<>|]", "", yt.title)  # Remove invalid characters

    progress_bar.set(0)
    percent.configure(text="0%")
    progress_bar.configure(progress_color="blue")

    if check_audio == "on":
        # Download only the audio
        audio_stream.download(download_location, filename="temp_audio.webm")

        # Convert the audio to mp3
        subprocess.run([
            ffmpeg_path, '-i', os.path.join(download_location, "temp_audio.webm"),
            os.path.join(download_location, f"{video_filename}.mp3")
        ], stdout=subprocess.DEVNULL, startupinfo=startupinfo, check=True, )

        # Delete the temporary audio file
        os.remove(os.path.join(download_location, "temp_audio.webm"))
    else:
        # Download both the video and the audio
        video_stream.download(download_location, filename="temp_video.mp4")
        audio_stream.download(download_location, filename="temp_audio.webm")

        # Merge the audio and video
        subprocess.run([
            ffmpeg_path, '-i', os.path.join(download_location, "temp_video.mp4"),
            '-i', os.path.join(download_location, "temp_audio.webm"),
            '-c', 'copy', os.path.join(download_location, f"{video_filename}.mp4")
        ], stdout=subprocess.DEVNULL, startupinfo=startupinfo, check=True)

        # Delete the temporary files
        os.remove(os.path.join(download_location, "temp_audio.webm"))
        os.remove(os.path.join(download_location, "temp_video.mp4"))

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

# Resolution choice
def choice(event):
    global quality
    quality = resolution.get()

# Light/Dark mode:
def theme():
    if customtkinter.get_appearance_mode() == "Light":
        customtkinter.set_appearance_mode("dark")
        mode.configure(image=dark_icon)
    else:
        customtkinter.set_appearance_mode("light")
        mode.configure(image=light_icon)

def chooseLocation():
    global loc
    global playlist_loc

    loc = tk.filedialog.askdirectory()

    # If the user didn't choose a directory, use the current directory
    if not loc:
        loc = os.getcwd()
    else:
        max_length = 13
        if len(loc) > max_length:
            display_text = loc[0:max_length] + '...'
        else:
            display_text = loc
        location.configure(text=display_text)
        location.configure(fg_color = "green")

    playlist_loc = loc

def checkbox_event():
    global check_audio
    check_audio = audio_only.get()

# Create the main window
app = customtkinter.CTk()

# Define check_audio at the start of your script
check_audio = tk.StringVar()

dark_icon = tk.PhotoImage(file="assets/light.png")
light_icon = tk.PhotoImage(file="assets/dark.png")

# Main window settings
app.title("YouTube Downloader")
app.geometry("720x480")
app.resizable(False, False)
app.grid_columnconfigure(0, weight=1)

app.iconbitmap('assets/icon.ico')

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

# Location input
location = customtkinter.CTkButton(app, width=110, height=40, text="Choose location", command=chooseLocation)
location.grid(row=2, column=0, padx=(70,0), pady=0, sticky="w")

# Download button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.grid(row=3, column=0, padx=20, pady=20)

# Audio only checkbox
audio_only = customtkinter.CTkCheckBox(app, text="Audio only", command=checkbox_event, variable=check_audio, onvalue="on", offvalue="off")
audio_only.grid(row=3, column=0, padx=(270,0), pady=0)

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