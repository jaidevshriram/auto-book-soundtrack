import os
import sys

from pydub import AudioSegment
from voiceResult import Result
from ShazamAPI import Shazam

from pydub import AudioSegment
import os
import math

from tqdm import tqdm

class SplitWavAudioMubin():
    def __init__(self):
        self.filename = os.path.basename(sys.argv[1])        
        self.audio = AudioSegment.from_wav(sys.argv[1])
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(os.path.join("temp", split_filename), format="wav")
        
    def multiple_split(self, min_per_split):
        total_mins = math.ceil(self.get_duration() / 60)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i+min_per_split, split_fn)
            # print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')
                
split_wav = SplitWavAudioMubin()
split_wav.multiple_split(min_per_split=10)

# audio = AudioSegment.from_wav(sys.argv[1])

# print(len(audio))
# exit()

# for i in range(len(audio)//10000): # Splt audio into 10 minute intervals
#     newAudio = audio[i*1000:i*1000 + 100000]
#     newAudio.export(f"temp/{i}.wav", format="wav")
# newAudio = audio[i:]
# newAudio.export(f"temp/{i}.wav", format="wav")

filenames = sorted(os.listdir("temp/"), key=lambda x: int(x.split('_')[0]))

songInfo = []
for i, file in enumerate(filenames):
    f = open(os.path.join("temp", file), 'rb').read()
    shazam = Shazam(
        f,
    )
    recognize_generator = shazam.recognizeSong()
    print(f"Processing {i}th split...")
    pbar = tqdm(total=600/8, position=0, leave=True) # Shazam processes 8 seconds at a time
    while True:
        tqdm._instances.clear()
        try:
            time, result = next(recognize_generator)
            
            time += i*600
            
            songResult = Result(time, result)
            songInfo.append(songResult)
            print(songResult)
            pbar.update(1)
        except:
            break
    pbar.close()

for info in songInfo:
    print(info)

np.save(sys.argv[2], songInfo)