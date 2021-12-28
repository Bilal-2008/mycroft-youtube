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
        my_setting = self.settings.get('my_setting')
    @intent_handler('youtube.intent')
    def youtube(self, message):
        yt=message.data.get("name")
        if yt==None:
            self.speak_dialog("Specify", wait=True)
            return False
        self.speak_dialog("Search", data={"title":yt})
        try:
            vid=yt.replace(" ", "+")
            url=f"https://www.youtube.com/results?search_query={vid}"
            html=urlopen(url)
            ids=re.findeall(r"watch\?v=(\S{11})", html.read().decode())
            id=ids[0]
            url=f"https://www.youtube.com/watch?v={id}"
            os.system("rm /home/pi/youtube.mp3")
            ydl_opts={"format":"bestaudio/best","outtmpl":"/home/pi/youtube.wav","postprocessors":[{"key":"FFmpegExtractAudio","preferredcodec":"mp3","preferredquality":"192"}]}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            try:
                self.media.stop()
            except:
                pass
            self.speak_dialog("Play", data={"title": yt}, wait=True)
            self.media=vlc.MediaPlayer("/home/pi/youtube.mp3")
            self.media.play()
        except:
            self.speak_dialog("Error", wait=True)
    def stop(self):
        self.media.stop()

def creat_skill():
    return YoutubeSkill()
