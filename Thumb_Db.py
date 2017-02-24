'''
Created on Feb 22, 2017

@author: taoprajjwal
'''

import ffvideo 
from converter.ffmpeg import FFMpeg

c=ffvideo.VideoStream('/home/taoprajjwal/PornMegaLoad_17_02_22_Hailey_Little_Private_School_Pussy_XXX_1080p_MP4_KTR_mp4_496kFf91t8CSiwd.mp4')
print(c.duration)


v=FFMpeg()
info=v.probe('/home/taoprajjwal/PornMegaLoad_17_02_22_Hailey_Little_Private_School_Pussy_XXX_1080p_MP4_KTR_mp4_496kFf91t8CSiwd.mp4')
print(info.format.duration)