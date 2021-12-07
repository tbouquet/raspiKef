

import datetime
import json
import tkinter as tk
from tkinter import ttk

import pykefcontrol.kef_connector as kef


class RaspiKef(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry('800x480')
        self.title('RaspiKef')
        self.resizable(0, 0)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.my_speaker = kef.KefConnector("192.168.1.116")

        self.create_widgets()

    def create_widgets(self):
        print(json.dumps(self.my_speaker._get_player_data(), indent=4))
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side='top', fill='both',
                             expand='true')

        artiste_label = ttk.Label(self.main_frame, text='Artist : ')
        artiste_label.grid(column=0, row=0, sticky=tk.NW, padx=5, pady=5)
        self.artiste_entry = ttk.Label(
            self.main_frame)
        self.artiste_entry.grid(column=1, row=0, sticky=tk.NW, padx=5, pady=5)
        self.album_label = ttk.Label(self.main_frame, text='Album : ')
        self.album_label.grid(column=0, row=1, sticky=tk.NW, padx=5, pady=5)
        self.album_entry = ttk.Label(
            self.main_frame)
        self.album_entry.grid(column=1, row=1, sticky=tk.NW, padx=5, pady=5)
        self.title_label = ttk.Label(self.main_frame, text='Title : ')
        self.title_label.grid(column=0, row=2, sticky=tk.NW, padx=5, pady=5)
        self.title_entry = ttk.Label(
            self.main_frame)
        self.title_entry.grid(column=1, row=2, sticky=tk.NW, padx=5, pady=5)
        self.label_timing = ttk.Label(self.main_frame)
        self.label_timing.grid(column=0, row=3, sticky=tk.NW, padx=5, pady=5)
        self.volume_slider = ttk.Scale(self.main_frame, from_=0, to=100)
        self.volume_slider.grid(row=4, sticky=tk.NSEW,
                                padx=5, pady=5, columnspan=3)

        self.statusbar = tk.Label(self,  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def refresher(self):
        songinfo = self.my_speaker.get_song_information()
        player_data = self.my_speaker._get_player_data()

        player_state = player_data['state']
        if player_state != ['stopped', "transitionning"]:
            # print(player_state)
            self.artiste_entry.configure(text=songinfo['artist'])
            self.album_entry.configure(text=songinfo['album'])
            self.title_entry.configure(text=songinfo['title'])
        else:
            self.artiste_entry.configure(text='')
            self.album_entry.configure(text='')
            self.title_entry.configure(text='')

        if player_state == 'playing':
            try:
                if self.my_speaker.song_length:
                    song_timmings = self.formatMilSec(
                        self.my_speaker.song_status), '/', self.formatMilSec(self.my_speaker.song_length)
                    self.volume_slider.configure(
                        from_=0, to=self.my_speaker.song_length)
                    self.volume_slider.set(self.my_speaker.song_status)
                else:
                    song_timmings = self.formatMilSec(self.my_speaker.song_status)

                self.label_timing.configure(text=song_timmings)
            except:
                print('Error')

            

        self.statusbar.configure(text=player_state)

        self.after(500, self.refresher)

    def formatMilSec(self, millis):
        return datetime.datetime.utcfromtimestamp(millis/1000).strftime('%H:%M:%S')


if __name__ == "__main__":
    raspikef = RaspiKef()
    raspikef.refresher()
    raspikef.mainloop()
