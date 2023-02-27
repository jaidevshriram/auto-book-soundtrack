import bs4
import regex as re
import pandas as pd

import os
import re
import copy
import json
import numpy as np
import codecs
import pylcs
import matplotlib.pyplot as plt

from collections import Counter
from pysrt.srttime import SubRipTime

from utils import *

class Video:
    def __init__(self, subtitles, scene_breaks, process=lower_text):
        self.srt = subtitles
        self.scene_breaks = scene_breaks
        self.process = process
       
           
    def get_subtitles(self, start, end):
        matched_subs = []
        for subtitle in self.srt:

            if subtitle['type']:
                continue

            time = subtitle['time']
            time_s = SubRipTime.from_string(subtitle['time'].split("-->")[0])
            time_ms = time_s.ordinal // 1000

            if time_ms >= start and time_ms <= end:
                matched_subs.append(self.process(subtitle['line']))
        return matched_subs        
    
    def get_subtitles_in_scene(self, scene_id):
        start, end, num, start_time, end_time = self.scene_breaks[scene_id]
        return self.get_subtitles(start_time, end_time)
        
    def __len__(self):
        return len(self.scene_breaks)