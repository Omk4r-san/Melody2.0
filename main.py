import os
import pickle
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer


class player(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        mixer.init()

        if os.path.exists('songs.pickle'):
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = []
        self.current = 0
        self.paused = True
        self.played = False

        self.create_frame()
        self.track_widgets()
        self.controls_widgets()
        self.songslist_widgets()

    def create_frame(self):
        # main screen
        self.track = tk.LabelFrame(self, text="ALBUM", font=("times new roman", 15, "bold"), fg="white", bg="grey",
                                   relief=tk.GROOVE)
        self.track.configure(width=400, height=300)
        self.track.grid(row=0, column=0, padx=0, pady=10)

        # bottom screen
        self.track_controls = tk.LabelFrame(self, font=("times new roman", 15, "bold"), fg="white", bg="white",
                                            relief=tk.GROOVE)
        self.track_controls.configure(width=500, height=200)
        self.track_controls.grid(row=1, column=0, pady=1, padx=15)

        # right screen
        self.track_songslist = tk.LabelFrame(self, text=f'playlist- no. {str(len(self.playlist))}',
                                             font=("times new roman", 15, "bold"), fg="white", bg="black",
                                             relief=tk.GROOVE)
        self.track_songslist.configure(width=150, height=450)
        self.track_songslist.grid(row=0, column=1, rowspan=3, pady=5, padx=10)

    def track_widgets(self):
        self.canvas = tk.Label(self.track, image=img)
        self.canvas.configure(width=390, height=240)
        self.canvas.grid(row=0, column=0)

        self.canvas = tk.Label(self.track, font=("times new roman", 15, "bold"), fg="dark blue", bg="white")
        self.canvas['text'] = "music player"
        self.canvas.configure(width=30, height=1)
        self.canvas.grid(row=1, column=0)

    # creating buttons
    def controls_widgets(self):
        self.loadsongs = tk.Button(self.track_controls, fg="white", bg="green", font="5")
        self.loadsongs['text'] = "Load songs"
        self.loadsongs['command'] = self.retrieve_song
        self.loadsongs.grid(row=0, column=0, padx=10)

        self.prev = tk.Button(self.track_controls, image=prev)
        self.prev['command'] = self.prev_song
        self.prev.grid(row=0, column=1)

        self.pause = tk.Button(self.track_controls, image=pause)
        self.pause['command'] = self.pause_song
        self.pause.grid(row=0, column=2)

        self.nex = tk.Button(self.track_controls, image=nex)
        self.nex['command'] = self.next_song
        self.nex.grid(row=0, column=3)

        self.volume = tk.DoubleVar()
        self.slider = tk.Scale(self.track_controls, from_=0, to=10, orient=tk.HORIZONTAL)
        self.slider["variable"] = self.volume
        self.slider['command'] = self.volume_tune
        self.slider.set(5)
        self.slider.grid(row=0, column=4)

    # creating scrollbar and listbox
    def songslist_widgets(self):
        self.scrollbar = tk.Scrollbar(self.track_songslist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=2, rowspan=5, sticky='ns')

        self.list = tk.Listbox(self.track_songslist, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar,
                               selectbackground="sky blue")
        self.enumerate_songs()
        self.list.configure(height=22)
        self.list.bind('<Double-1>', self.play_song)

        self.scrollbar.configure(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)

    # displaying list
    def enumerate_songs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))

    # reading files
    def retrieve_song(self):
        self.songlist = []
        directory = filedialog.askdirectory()
        for root_, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == ".mp3":
                    path = (root_ + "/" + file).replace("\\", "/")
                    self.songlist.append(path)

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songlist, f)

        self.playlist = self.songlist
        self.track_songslist['text'] = f'playlist- no. {str(len(self.playlist))}'
        self.list.delete(0, tk.END)
        self.enumerate_songs()

    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg='white')

        mixer.music.load(self.playlist[self.current])
        mixer.music.play()

    def prev_song(self):
        pass

    def pause_song(self):
        pass

    def next_song(self):
        pass

    def volume_tune(self, event=None):
        self.v = self.volume.get()
        print(self.v)


root = tk.Tk()
root.geometry("600x400")
root.title("Melody 2.0")

img = PhotoImage(file="C:/Users/omkar-chan/PycharmProjects/melody2/icons/background.png")
play = PhotoImage(file="C:/Users/omkar-chan/PycharmProjects/melody2/icons/play.jpg ")
pause = PhotoImage(file="C:/Users/omkar-chan/PycharmProjects/melody2/icons/pause.jpg")
prev = PhotoImage(file="C:/Users/omkar-chan/PycharmProjects/melody2/icons/prev.jpg")
nex = PhotoImage(file="C:/Users/omkar-chan/PycharmProjects/melody2/icons/next.jpg")

app = player(master=root)
app.mainloop()
