# Import necessary modules
import ttkbootstrap as tk
from tkinter import filedialog, ttk
import yt_dlp
from threading import Thread

# Create main window
root = tk.Window(themename="superhero")
root.title('Youtube Downloader')

# Create a string variable to store the selected quality
current_var = tk.StringVar()

# Create a combobox with the available qualities
combobox = ttk.Combobox(root, textvariable=current_var)
combobox['values'] = ('320', '480', '720', '1080')

# Create a label for the combobox and display it
labelcombo = tk.Label(root, text="Quality: ")
labelcombo.grid(row=2, column=0)
combobox.grid(row=2, column=1)

# Define a function to retrieve the link entered in the text field
def choose_link():
    text = text_field.get()    
    return text

# Create a label and text field for entering the link
label = tk.Label(root, text="Enter a link:")
text_field = tk.Entry(root)

# Display the label and text field
label.grid(row=0, column=0)
text_field.grid(row=0, column=1)

# Create a string variable to store the selected directory path
directory_path = tk.StringVar()

# Define a function to choose the directory path and update the label
def choose_path():
    directory_path.set(filedialog.askdirectory())
    directory_label.config(text=directory_path.get())
    return directory_path
    
# Define a function to download the video
def download(download_path, download_link, download_resolution):
    # Set the options for the youtube-dl downloader
    ydl_opts = {
        'format': 'best[height<='+download_resolution+']',
        'outtmpl': download_path + '/%(title)s.%(ext)s',
    }
    # Download the video using youtube-dl
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['{}'.format(download_link)])

# Define a function to start the download thread
def startDownloadThread():
    downloadThread = Thread(target=download, args=(directory_path.get(), choose_link(), current_var.get()))
    downloadThread.start()

# Create a button to choose the directory path
choose_button = tk.Button(root, text="Choose Directory Path", command=choose_path)
choose_button.grid(row=1, column=1)

# Create a label to display the selected directory path
directory_label = tk.Label(root, text="No directory path selected")
directory_label.grid(row=1, column=0)

# Create a button to start the download
button = tk.Button(root, text="Download", command=startDownloadThread)
button.grid(row=3, column=1)

# Start the main event loop
root.mainloop()