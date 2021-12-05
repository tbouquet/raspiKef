import datetime
import json
import tkinter as tk
from tkinter.constants import LEFT

from PIL import Image, ImageTk
from pykefcontrol.kef_connector import KefConnector

my_speaker = KefConnector("192.168.1.116")
print(json.dumps(my_speaker._get_player_data(), indent=4))

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
labelPlayerStatus = tk.Label(
    fenetre, justify='left', borderwidth=2, relief="groove")


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

    playerState = playerData['state']
    labelPlayerStatus.configure(text=playerState)
    labelVolume.configure(text=my_speaker.volume)

    if playerState != 'stopped':
        labelSongArtist.configure(text='Artiste : '+songInfo['artist'])
        labelSongTitle.configure(text='Title : ' + songInfo['title'])
        labelSongAlbum.configure(text='Album : '+songInfo['album'])
        labelSongCoverUrl.configure(text=songInfo['cover_url'])
    else:
        labelSongArtist.configure(text='Artiste : ')
        labelSongTitle.configure(text='Title : ')
        labelSongAlbum.configure(text='Album : ')
        labelSongCoverUrl.configure(text='')

    if playerState == 'playing':
        songTimings = formatMilSec(
            my_speaker.song_status), '/', formatMilSec(my_speaker.song_length)
        labelTime.configure(text=songTimings)

    fenetre.after(500, Refresher)


def formatMilSec(millis):
    return datetime.datetime.utcfromtimestamp(millis/1000).strftime('%H:%M:%S')


Refresher()
fenetre.mainloop()
