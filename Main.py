'''
Created on Feb 18, 2017

@author: taoprajjwal
'''

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel,TabbedPanelHeader,TabbedPanelContent
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
    

import os
import subprocess
from glob import glob
import ffvideo
from converter import Converter 


Builder.load_file('Main.kv')

class MainApp(App):
    def build(self):
        return Tabb()
    
class Tabb(TabbedPanel):
    pass
class MainScreen(GridLayout):
    def __init__(self,**kwargs):
        super(MainScreen,self).__init__()
        self.cols=3
        self.spacing=10
        self.size_hint_y=None
        self.bind(minimum_height=self.setter('height'))
        for i in range(0,27):
            self.add_widget(VidWindow())
class Scrool(ScrollView):
    def __init__(self,**kwargs):
        super(Scrool,self).__init__(**kwargs)
        self.add_widget(MainScreen())
class VidWindow(RelativeLayout):
    def __init__(self,**kwargs):
        super(VidWindow,self).__init__(**kwargs)
        self.size_hint_y=None
    def oppen(self):
        subprocess.call(['xdg-open','/home/taoprajjwal/Desktop/pemfc.gif'])

class ImageButton(ButtonBehavior,Image):
    pass

class Main_Load(RelativeLayout):
    _popup=ObjectProperty(None)
    def close_popup(self):
        self._popup.dismiss()
    def open_popup(self):
        Content=Dialog(load=self.Load_dir,cancel=self.close_popup)
        self._popup=Popup(content=Content,title='Choose Directory',size_hint=(0.9,0.9))
        self._popup.open()
    def Load_dir(self,dirr):
        self.close_popup()
        self.add_widget(Scrool_Load(dirr))
    def AddFiles(self,dirr):
        pass

class Dialog(RelativeLayout):
    load=ObjectProperty(None)
    cancel=ObjectProperty(None)
    
class Scrool_Load(ScrollView):
    def __init__(self,dirr,**kwargs):
        super(Scrool_Load,self).__init__(**kwargs)
        self.add_widget(FileGrid(dirr))

class FileGrid(GridLayout):
    directory=StringProperty()
    def __init__(self,dirr,**kwargs):
        super(FileGrid,self).__init__(**kwargs)
        self.cols=3
        self.spacing=10
        self.size_hint_y=None
        self.size_hint_x=1
        self.row_default_height=300
        self.row_force_default=True
        self.bind(minimum_height=self.setter('height'))
    
        self.directory=str(dirr[0])
        files=self.Scanfiles()
        for i in range(0,len(files)):
            self.add_widget(VidWindow_Load(files[i],self.directory))
        
    def Scanfiles(self):
        os.chdir(self.directory)
        extensions=['*.mp4','*.webm','*.flv','*.mkv']
        files=[]
        for tyype in extensions:
            files.extend(glob(tyype))
        return files
        
class VidWindow_Load(BoxLayout):
    files=StringProperty()
    thumblocation=StringProperty()
    directory=StringProperty()
    
    def __init__(self,files,directory,**kwargs):
        super(VidWindow_Load,self).__init__(**kwargs)
        self.size_hint_y=None
        self.files=files
        self.directory=directory
        self.orientation='vertical'
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
MainApp().run()