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

def getChapterQuotes(path):
    chapter = chapterText(path)
    quotes = chapter.getQuotes()
    
    return quotes

class chapterText:
    def __init__(self, path):
        self.path = path
        self.lines = self.getText()
        self.allText = self.getAll()
        
    def getAll(self):
        with open(self.path, 'r') as f:
            lines = f.read()
            return lines
        
    def getText(self):
        self.sentences = []
        with codecs.open(self.path, 'r', encoding='utf-8',
                 errors='ignore') as f:
            lines = f.read()
#             lines = re.sub('[A-Za-z](\')[A-Za-z]', "", lines)
            lines = re.findall('(?:\"(.*?)\"[^A-Za-z])', lines)
            lines = list(map(lambda x: x.lower().strip(), lines))
            lines = list(filter(lambda x: len(x.split(' ')) > 5, lines))
        
            self.sentences = lines
            return lines
    
    def getQuotes(self):
        return self.getText()
        
    def searchLine(self, query):
        
        result = None
        maxS = 0
        maxI = -1
        for i, line in enumerate(self.lines):
            score = pylcs.lcs(line, query)
#             score /= max(len(line), len(query[0]))
            if score > maxS:
                maxS = score
                maxI = i
                
        if maxS > 0:
            return maxI, maxS
        return result, -1
    
    def __str__(self):
        return self.path
    
class Book:
    def __init__(self, chapters, base="."):
        self.chapterPaths = chapters
        self.base = base
        self.chapterContent = self.getChapterContent()
        
    def getChapterContent(self):
        chapter = []
        for chapterPath in self.chapterPaths:
            chapter.append(chapterText(os.path.join(self.base, "data", "HP", "chapters", chapterPath)))
        return chapter
    
    def findLineInChapter(self, query):
        query = query.lower().strip()

        maxScore = -1
        result = None
        chapterFinal = None
        for chapter in self.chapterContent:

            ret, score = chapter.searchLine(query)
            if ret is not None:
                if score > maxScore:
                    maxScore = score
                    result = ret
                    chapterFinal = chapter
        if result is not None:
#             print(query, chapterFinal.path)
            return (chapter.path, result, query)
        else:
            return ("Couldn't find", -1, query)
        
    def getAllLines(self):
        allLines = []
        allChapters = []
        for chapter in self.chapterContent:
            for line in chapter.lines:
                allLines.append(line)
                allChapters.append(chapter.path)
        return allLines, allChapters
    
    def getAllText(self):
        lines, _ = self.getAllLines()
        return " ".join(lines)

class BookChunked:
    def __init__(self, chapters, base="."):
        self.chapterPaths = chapters
        self.base = base
        self.chapterContent = self.getChapterContent()
        
    def getChapterContent(self):
        chapter = []
        for chapterPath in self.chapterPaths:
            chapter.append(chapterText(os.path.join(self.base, chapterPath)))
        return chapter
    
    def getAllChunks(self):
        chapterChunks = []
        for chapterPath in self.chapterPaths:
            with open(os.path.join(self.base, chapterPath), 'r') as f:
                chunks = json.load(f)['segmented']
                chapterChunks.append(chunks)
        return chapterChunks            
            
    def getAllLines(self):
        allLines = []
        allChapters = []
        for chapter in self.chapterContent:
            for line in chapter.lines:
                allLines.append(line)
                allChapters.append(chapter.path)
        return allLines, allChapters
    
    def getAllText(self):
        allText = []
        allChapters = []
        for chapter in self.chapterContent:
            text = chapter.getAll()
            allText.append(text)
        return " ".join(allText)