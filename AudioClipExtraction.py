
from PyQt5.QtCore import *
class AudioClipExtractor(QThread):
     def __init__(self,parent):
        QThread.__init__(self, parent)

     def run(self):
        self.audio_events()
     def audio_events(self):  
         import librosa 
         import matplotlib.pyplot as plt 
         import numpy as np
         import pandas as pd
         from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
         import moviepy.editor as mp
         import wave 
         import glob
         import wave
         import scipy.io.wavfile as wav
         import numpy as np 
         
         #change the path with cricket match video path
         file_path =glob.glob('./cricket_video.mp4')
         print(file_path[0])
        
        
         filename=mp.VideoFileClip(file_path[0])
         filename.audio.write_audiofile('./cricket_video/Highlights' +'.wav')
         filename='./cricket_video/Highlights.wav'
         

         
         sample_rate, data= wav.read(filename)
         length = data.shape[0] / sample_rate
         print(f"Duration of Whole Video in Seconds = {length}s")
         print(f"Number of channels = {data.shape[1]}")

         #Convert to mono channel
         data = data.astype(np.float32)
         def read_data(data):
             yield (data[:,0]+data[:,1]/2)
         for i in  read_data(data):
             wave_array=i

         def find_energy(moving_average_list):
             energy=[]
             for array in moving_average_list:
                 yield np.square(array)
         def subsample(array,step):
             ssarray=array[::step].copy()
             return ssarray
         
         #Calling Methods   
         SAMPLING_FACTOR=4
         sampled_array=subsample(wave_array, SAMPLING_FACTOR)
         energy=list(find_energy(sampled_array)) 
        
        #Find The exact time in secwhere the noise comes 
         def find_highlight_times(array, threshold, sample_rate):
           chunks = []
           for i in range(len(array)-1):
             if (array[i]<threshold<array[i+1] or array[i]>threshold>array[i+1]):
               yield (i*SAMPLING_FACTOR/sample_rate)
        
         threshold=np.max(energy)*(4/5)
         times = list (find_highlight_times(energy, threshold, sample_rate))


        #Removing the same secs from lists
         new_list=[]
         for i in times:
             if int(i) not in new_list:
                 new_list.append(int(i))
        
        
        #Removing also the clips or sec which have duration of 20 sec 
         i = 0
         while i < len(new_list)-1:
            if new_list[i+1] - new_list[i]<=20:
                new_list.pop(i)
            else:
                i += 1   
            
        #Making Clips list        
         Clips_list=[]
         for i in new_list:
             if i>=10 or i<=length-10:
                 Clips_list.append([i-10,i+10])  
        
         #Making Clips List         
         for i in Clips_list:
             start_lim=i[0]
             end_lim=i[1]
             filename= './Runs/Events/'+str(start_lim) + "_" +str(end_lim)  + ".mp4"
             ffmpeg_extract_subclip(file_path[0],start_lim,end_lim,targetname=filename)
     
		          
             

  
  
