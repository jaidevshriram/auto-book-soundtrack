import os
import sys
import json
import time
import numpy as np

from tqdm import tqdm

from sentence_transformers import SentenceTransformer

from finch import FINCH

model = SentenceTransformer('all-mpnet-base-v2')

BASE = sys.argv[1]
file_paths = os.listdir(BASE)

def run(file_path):

    # ---- Feature Extraction ----

    name = file_path.split('/')[-1].split('.')[0]
    print(name)

    sentences = list(open(os.path.join(BASE, file_path)).read().splitlines())[1:]
    sentences_all = list(map(lambda x: x.strip(), sentences))

    sentences = []
    for sentence in sentences_all:
        if len(sentence) == 0:
            continue
        sentences.append(sentence)

    sentence_embeddings = model.encode(sentences)
        
    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2], exist_ok=True)

    np.savetxt(f"{sys.argv[2]}/{name}.csv", sentence_embeddings, delimiter=',')

    # ---- FINCH ----

    data = np.genfromtxt(f"{sys.argv[2]}/{name}.csv", delimiter=",").astype(np.float32)
    start = time.time()
    c, num_clust, req_c = FINCH(data, initial_rank=None, req_clust=None, distance='cosine', tw_finch=True, ensure_early_exit=True, verbose=True)
    print('Time Elapsed: {:2.2f} seconds'.format(time.time() - start))

    # Write back        
    if not os.path.exists(f"{sys.argv[3]}/{name}"):
        os.makedirs(f"{sys.argv[3]}/{name}", exist_ok=True)
    
    print('Writing back the results on the provided path ...')
    np.savetxt(f"{sys.argv[3]}/{name}" + '/c.csv', c, delimiter=',', fmt='%d')
    np.savetxt(f"{sys.argv[3]}/{name}" + '/num_clust.csv', np.array(num_clust), delimiter=',', fmt='%d')
    if req_c is not None:
        np.savetxt(f"{sys.argv[3]}/{name}" + '/req_c.csv', req_c, delimiter=',', fmt='%d')

    clusters = c[:, 2]
    
    tiles = []
    txt = ""
    prev_cluster = 0
    for i, sentence in enumerate(sentences):
        
        if i >= len(clusters):
            continue
        
        if clusters[i] != prev_cluster:
            tiles.append(txt)
            prev_cluster = clusters[i]
            txt = ""
            
        txt += sentence + "\n\n"
    tiles.append(txt)
        
    with open(f"{sys.argv[3]}/{name}/{name}.json", "w") as f:
        json.dump({"segmented": tiles}, f, indent=5)

for file_path in tqdm(file_paths):
    run(file_path)

