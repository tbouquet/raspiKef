import datetime
import json
import tkinter as tk
from tkinter.constants import LEFT

from PIL import Image, ImageTk
from pykefcontrol.kef_connector import KefConnector

my_speaker = KefConnector("192.168.1.116")

fenetre = tk.Tk()
fenetre.geometry('800x480')


labelSongArtist = tk.Label(fenetre,  justify='left',
                           borderwidth=2, relief="groove")
labelSongTitle = tk.Label(fenetre,  justify='left',
                          borderwidth=2, relief="groove")
labelSongAlbum = tk.Label(fenetre,  justify='left',
                          borderwidth=2, relief="groove")
labelSongCoverUrl = tk.Label(fenetre,  justify='left',
                             borderwidth=2, relief="groove")
labelTime = tk.Label(fenetre, justify='left', borderwidth=2, relief="groove")
labelVolume = tk.Label(fenetre, justify='left', borderwidth=2, relief="groove")
labelPlayerStatus = tk.Label(fenetre, justify='left', borderwidth=2, relief="groove")


labelSongArtist.pack(padx=5, pady=5)
labelSongTitle.pack(padx=5, pady=5)
labelSongAlbum.pack(padx=5, pady=5)
labelSongCoverUrl.pack(padx=5, pady=5)
labelTime.pack(padx=5, pady=5)
labelVolume.pack(padx=5, pady=5)
labelPlayerStatus.pack(padx=5, pady=5)
# json_data = my_speaker._get_player_data()


def Refresher():

    songInfo = my_speaker.get_song_information()
    playerData = my_speaker._get_player_data()
    # print(playerData)

    # print(songInfo)
    playerStatus = playerData['state']
    songArtist = 'Artist : ' + songInfo['artist']
    songTitle = ' Title : ' + songInfo['title']
    songAlbum = 'Album : ' + songInfo['album']
    songCover = songInfo['cover_url']

    labelPlayerStatus.configure(text=playerStatus)
    labelSongArtist.configure(text=songArtist)
    labelSongTitle.configure(text=songTitle)
    labelSongAlbum.configure(text=songAlbum)
    labelSongCoverUrl.configure(text=songCover)
    if playerStatus == 'playing':
        songTimings = formatMilSec(
            my_speaker.song_status), '/', formatMilSec(my_speaker.song_length)
        labelTime.configure(text=songTimings)
    labelVolume.configure(text=my_speaker.volume)
    fenetre.after(500, Refresher)


def formatMilSec(millis):
    return datetime.datetime.utcfromtimestamp(millis/1000).strftime('%H:%M:%S')


Refresher()
fenetre.mainloop()
