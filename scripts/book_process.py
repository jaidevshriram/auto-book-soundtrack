import os
import sys
from tqdm import tqdm

from booknlp.booknlp import BookNLP

model_params={
        "pipeline":"entity,quote,event,coref", 
        "model":"big", 
}

booknlp=BookNLP("en", model_params)

FILE_BASE = sys.argv[1]
OUTPUT_FILE_BASE = sys.argv[2]

if not os.path.exists(OUTPUT_FILE_BASE):
    os.makedirs(OUTPUT_FILE_BASE, exist_ok=True)

for file_name in tqdm(os.listdir(FILE_BASE)):
    input_file = os.path.join(FILE_BASE, file_name)
    output_dir = os.path.join(OUTPUT_FILE_BASE, file_name.split('.')[0]) 
    idd = file_name.split('.')[0]
    
    booknlp.process(input_file, output_dir, idd)