'''
Created on Feb 19, 2017

@author: taoprajjwal
'''


import os
from glob import glob
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty  
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import ffvideo
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.image import Image
from converter.ffmpeg import FFMpeg
import subprocess


Builder.load_file('Test.kv')

class MainApp(App):
    _Main=ObjectProperty(None)
    def build(self):
        self._Main=Main()
        return self._Main
    def update(self):   
        self._Main.add_widget(Label(text='Hi'))

class Main(RelativeLayout):
    _popup=ObjectProperty(None)
    def close_popup(self):
        self._popup.dismiss()
    def open_popup(self):
        Content=Dialog(load=self.Load_dir,cancel=self.close_popup)
        self._popup=Popup(content=Content,title='Choose Directory',size_hint=(0.9,0.9))
        self._popup.open()
    def Load_dir(self,dirr):
        self.close_popup()
        self.add_widget(Scrool(dirr))
    def AddFiles(self,dirr):
        pass
    
class Dialog(RelativeLayout):
    load=ObjectProperty(None)
    cancel=ObjectProperty(None)

class FileGrid(GridLayout):
    directory=StringProperty()
    def __init__(self,dirr,**kwargs):
        super(FileGrid,self).__init__(**kwargs)
        self.cols=3
        self.spacing=10
        self.size_hint_y=None
        self.size_hint_x=1
        self.row_default_height=200
        self.row_force_default=True
        self.bind(minimum_height=self.setter('height'))
    
        self.directory=str(dirr[0])
        files=self.Scanfiles()
        for i in range(0,len(files)):
            self.add_widget(VidWindow(files[i],self.directory))
        
    def Scanfiles(self):
        os.chdir(self.directory)
        extensions=['*.mp4','*.webm','*.flv','*.mkv']
        files=[]
        for tyype in extensions:
            files.extend(glob(tyype))
        return files
        
        
class VidWindow(BoxLayout):
    files=StringProperty()
    thumblocation=StringProperty()
    directory=StringProperty()
    
    def __init__(self,files,directory,**kwargs):
        super(VidWindow,self).__init__(**kwargs)
        self.size_hint_y=None
        self.files=files
        self.directory=directory
        self.ThumbGenerate()

    def ThumbGenerate(self):
        vidlocation=self.directory+'/'+self.files
        thumbdir='/home/taoprajjwal/.CollectionManager/thumbs'
        if os.path.isfile(thumbdir+'/'+self.files):
            self.thumblocation=thumbdir+'/'+self.files
        else:
            V=ffvideo.VideoStream(vidlocation)
            duration=V.duration
            self.thumblocation=thumbdir+'/'+'{}.png'.format(self.files)
            subprocess.call("ffmpeg -ss {0} -i '{1}' -vframes 1 '{2}'".format(duration/5,vidlocation,self.thumblocation),shell=True)

        
        self.add_widget(ImageButton(source=self.thumblocation,keep_ratio=False,allow_stretch=True))
        
class Scrool(ScrollView):
    def __init__(self,dirr,**kwargs):
        super(Scrool,self).__init__(**kwargs)
        self.add_widget(FileGrid(dirr))

class ImageButton(Image,ButtonBehavior):
    pass

MainApp().run() 
    