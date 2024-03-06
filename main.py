import pytube as pt
import os
import tkinter as tk
import customtkinter

# Download the video
def startDownload():
    try:
        url = link.get()
        yt = pt.YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
        video.download(os.getcwd())
    except:
        print("An error occurred while downloading the video")
    finished.configure(text="Finished downloading")

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

app.title("YouTube Downloader")
app.geometry("720x480")

# app.resizable(False, False)
customtkinter.set_appearance_mode("System")
app.grid_columnconfigure(0, weight=1)

# Title
title = customtkinter.CTkLabel(app, text="Insert a youtube link")
title.grid(row=1, column=0, padx=10, pady=10)

# Light/Dark mode button
mode = customtkinter.CTkButton(app, width=1, image="", text="", fg_color= "transparent", command=theme)
mode.grid(row=1, column=0, padx=10, pady=1, sticky="e")

# Light/Dark mode icon
if customtkinter.get_appearance_mode() == "Light":
    mode.configure(image=light_icon)
else:
    mode.configure(image=dark_icon)

# Link input
url_var = tk.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.grid(row=2, column=0, padx=10, pady=10)

# Download button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.grid(row=3, column=0, padx=20, pady=20)

# Finished Downloading
finished = customtkinter.CTkLabel(app, text="")
finished.grid(row=4, column=0, padx=10, pady=10)


app.mainloop()