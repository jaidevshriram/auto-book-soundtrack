import bs4
import regex as re
import pandas as pd

from collections import Counter
from bs4 import BeautifulSoup

def getMentionedChapterNames(path):
    text = open(path + ".book.html", "r").read()
    outsoup = BeautifulSoup(text, 'html.parser')

    soup = None
    for tag in outsoup:
        soup = tag
    
    start = False
    
    allCharacters = {}
    
    for tag in soup:
        
        if tag.name == "h2":
            start = True
            continue
        elif start and tag.name == "p":
            break
        elif not start or not isinstance(tag, bs4.element.NavigableString):
            continue
            
        line = str(tag).strip()
#         print(line)
        line = re.split(" |/", line)
#         print(line)
        
        if len(line) < 2:
            continue
        
        i = 1
        characters = []
        charName = ""
        while i < len(line):
            if line[i].startswith("("):
                characters.append(charName.strip())
                i += 1
                continue
            charName += line[i] + " "
            i += 1
        if len(characters) < 1:
            continue
            
        allCharacters[characters[0].strip()] = characters
    return allCharacters
    

def getSpeakerChapterNames(path):
#     print(path)
    df = pd.read_csv(path + ".quotes", sep="\t")
    charCountIds = dict(Counter(list(df['char_id'])))
    
    chars = charCountIds.keys()
    charNames = {}
    
#     print(path + ".entities")
    entities = pd.read_csv(path + ".entities", sep="\t")
    
    for char in chars:
        res = entities[entities["COREF"] == char]
        res = res[res["prop"] == "PROP"]
        
        if len(res) == 0:
            continue
           
        name = res.iloc[0]['text']
        
        charNames[name] = charCountIds[char]

#     print(charNames)
    return charNames
    
if __name__ == '__main__':
#     getChapterNames("/mnt/c/Users/jaide/Desktop/book-process/processed_data/Harry_Potter/16-Through_the_Trapdoor/16-Through_the_Trapdoor.book.html")
    getSpeakerChapterNames("/mnt/c/Users/jaide/Desktop/book-process/processed_data/Harry_Potter/16-Through_the_Trapdoor/16-Through_the_Trapdoor")