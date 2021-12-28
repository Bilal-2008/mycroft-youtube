from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
import vlc
from urllib.request import urlopen
import youtube_dl
import re
import os
class YoutubeSkill(MycroftSkill):
    def __init__(self):
        super().__init__()
    def initialize(self):
        self.my_setting = self.settings.get('my_setting')
    @intent_handler('youtube.intent')
    def handle_youtube(self, message):
        self.yt=message.data.get("name")
        if self.yt==None:
            self.speak_dialog("Specify", wait=True)
            return False
        self.speak_dialog("Search", data={"title":self.yt})
        try:
            self.vid=self.yt.replace(" ", "+")
            self.url=f"https://www.youtube.com/results?search_query={self.vid}"
            self.html=urlopen(self.url)
            self.ids=re.findeall(r"watch\?v=(\S{11})", self.html.read().decode())
            self.id=self.ids[0]
            self.url=f"https://www.youtube.com/watch?v={self.id}"
            os.system("rm /home/pi/youtube.mp3")
            self.ydl_opts={"format":"bestaudio/best","outtmpl":"/home/pi/youtube.wav","postprocessors":[{"key":"FFmpegExtractAudio","preferredcodec":"mp3","preferredquality":"192"}]}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            try:
                self.media.stop()
            except:
                pass
            self.speak_dialog("Play", data={"title": self.yt}, wait=True)
            self.media=vlc.MediaPlayer("/home/pi/youtube.mp3")
            self.media.play()
        except:
            self.speak_dialog("Error", wait=True)
            
    def stop(self):
        self.media.stop()

def creat_skill():
    return YoutubeSkill()
