import os
import struct

for nome in os.listdir("input//"):
    os.mkdir("input//temp")
    if(".mp4" in nome and ".ckd" not in nome):
        os.system('ffmpeg -i input//' + nome + ' -ar 32000 -filter:a "volume=12dB" -map_channel 0.1.0 input//temp//left.wav -ar 32000 -filter:a "volume=12dB" -map_channel 0.1.1 input//temp//right.wav')
    if(".wav" in nome and ".ckd" not in nome or ".mp3" in nome):
        os.system("ffmpeg -i input//" + nome + " -ar 32000 -map_channel 0.0.0 input//temp//left.wav -ar 32000 -map_channel 0.0.1 input//temp//right.wav")
    if(".ckd" not in nome and os.path.isfile("input//temp//left.wav")):
        os.system("VGAudioCli input//temp//left.wav input//temp//left.dsp")
        os.system("VGAudioCli input//temp//right.wav input//temp//right.dsp")
        rightbytes = []
        leftbytes = []
        filesize = (os.path.getsize("input//temp//left.dsp") - 96)
        leftcoefs = b''
        rightcoefs = b''

        with open("input//temp//left.dsp", "rb") as f:
            leftcoefs = f.read(96)
            for i in range(int(filesize/8)): 
                byte = f.read(8)
                leftbytes.append(byte)

        with open("input//temp//right.dsp", "rb") as f:
            rightcoefs = f.read(94)
            byte = f.read(2)
            for i in range(int(filesize/8)): 
                byte = f.read(8)
                rightbytes.append(byte)
        
        os.remove("input//temp//left.wav")
        os.remove("input//temp//right.wav")
        os.remove("input//temp//left.dsp")
        os.remove("input//temp//right.dsp")
        os.rmdir("input//temp")

        denc = open("output//" + nome + ".ckd", "wb")
        denc.write(b'\x52\x41\x4B\x49\x00\x00\x00\x0B\x57\x69\x69\x20\x61\x64\x70\x63\x00\x00\x01\x22\x00\x00\x01\x40\x00\x00\x00\x04\x00\x00\x00\x03\x66\x6D\x74\x20\x00\x00\x00\x50\x00\x00\x00\x12\x64\x73\x70\x4C\x00\x00\x00\x62\x00\x00\x00\x60\x64\x73\x70\x52\x00\x00\x00\xC2\x00\x00\x00\x60\x64\x61\x74\x53\x00\x00\x01\x40\x00\x73\x27\x00\x00\x02\x00\x02\x00\x00\x7D\x00\x00\x00\xFA\x00\x00\x02\x00\x10\x00\x00')
        denc.write(leftcoefs)
        denc.write(rightcoefs)
        for i in range(int(filesize/8)):
            denc.write(leftbytes[i])
            denc.write(rightbytes[i])   
        denc.close()
        print("DONE: " + nome + ".ckd")
