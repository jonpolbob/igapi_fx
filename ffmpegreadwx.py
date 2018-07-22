



#lecture d'une video image par image en python avec ffmpeg
#avec wxwidgets
#et sans opencv

import json
import subprocess as sp
import matplotlib.pyplot as plt
import os
import time

#lecture des metadata
#ffmpeg -i <videofile> -f ffmetadata metadata.txt


filename="C:\\tmp\\Zebrafish_Swimming_SD.avi"
cmdprobe = r"""c:\program files\ffmpeg\bin\ffprobe.exe""" 

command = [cmdprobe,
           "-v","quiet",
           "-print_format","json",
           "-show_streams",
           filename,
           ]

ffprobeOutput = sp.check_output(command).decode('utf-8')
ffprobeOutput = json.loads(ffprobeOutput)

height = ffprobeOutput['streams'][0]['height']
width = ffprobeOutput['streams'][0]['width']
pixfmt = ffprobeOutput['streams'][0]['pix_fmt']

#pipe=sp.Popen(command,stdout = sp.PIPE, bufsize=10**8)
#b=pipe.communicate()
print ("-----------------------------")
print(ffprobeOutput)
print ("-----------------------------")

cmd = r"""c:\program files\ffmpeg\bin\ffmpeg.exe"""

command = [cmd,
           "-i",filename,
           '-f', 'image2pipe',
           '-pix_fmt','rgb24',
           '-vcodec','rawvideo',
           '-']

if os.name == 'nt' :
    startupinfo = sp.STARTUPINFO()
    startupinfo.dwFlags |= sp.STARTF_USESHOWWINDOW
 
pipe=sp.Popen(command,stdout = sp.PIPE, bufsize=10**8)


import numpy

encore = True

#plt.show()
nbimage=0


#plt.ion()

while encore:
    raw_image=pipe.stdout.read(height*width*3)
    image=numpy.fromstring(raw_image, dtype='uint8')
    if len(image) ==height*width*3:
        image = image.reshape((height,width,3))
        pipe.stdout.flush()
        nbimage = nbimage+1
        if nbimage == 1:
             myobj = plt.imshow(image)
        else:
            myobj.set_data(image)
        plt.pause(.01)
        
    else:
        encore =0
    

    
