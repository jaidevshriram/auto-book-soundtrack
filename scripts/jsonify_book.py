import os
import sys
import json

FILE_BASE = sys.argv[1]
NEW_FILE_BASE = sys.argv[2]

if not os.path.exists(NEW_FILE_BASE):
    os.makedirs(NEW_FILE_BASE, exist_ok=True)

file_names = os.listdir(FILE_BASE)

for file_name in file_names:
    f = open(os.path.join(FILE_BASE, file_name), "r")
    content = f.read()
    f.close()

    chapNum = int(file_name.split('-')[0].lstrip('0'))
    chapName = ' '.join(file_name.split('-')[1].split('.')[:-1])

    out = {
        'chapter_name': chapName,
        'chapNum': chapNum,
        'content': content,
    }

    with open(os.path.join(NEW_FILE_BASE, str(chapNum) + '.json'), 'w') as f:
        json.dump(out, f)
