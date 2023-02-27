# ismir-2022
Work in progrss repo for ISMIR'22 code release - Sonus Texere

Data required:

- Movie (mp4)
- Movie Audio Track (wav)
- Book (partitioned into chapters as text files)
- Subtitles
- Transcript

Refer to `data/hp` to see how the data is typically stored.

# Steps


## 1. Video Processing

1. Clone the repository here - https://github.com/xavierpuigf/shotdetection/ and follow installation instructions as described.
2. Run the script as described on your chosen movie file

```
sh run_shot_detection.sh data/{movie_name}/movie.mp4 processed/{movie_name}/
```

This should create a set of files named `movie.dfd`, `movie.matidx`, and `movie.videvents`.

Now, we move on to scene detection. Note that the implementation used was originally built for Big Bang Theory (BBT) - hence a lot of the naming used in these scripts reflects that.

3. Edit line 31 in `scenes/low_level_shot_similarity.m` to the path to the movie. This is used to compute histograms for the movie.

4. Copy `processed/{movie_name}/movie.videvents` to `VideoSceneDetection/data/shot_boundaries/bbt_s01e01.videvents`.

5.  Convert the shots extracted to the required format for scene detection:

```
python scripts/convert_to_bbt.py processed/{movie_name}/
```

This will overwrite some files in `VideoSceneDetection/data`, so be careful if you are dealing with multiple movies.

6. Open the folder `VideoSceneDetection` in MATLAB and run `runall.m`. 

Optional: You can use the script `visualization/visualize_scenes_via_htmlrender.m` to output a HTML files with all scenes visualized.

## 2. Process the Book

1. Run `scripts/jsonify_book.py`

```
python scripts/jsonify_book.py data/{movie_name}/book processed/{movie_name}/book/
```

2. Extract emotion labels for the book

```
python scripts/extract-text-emotion.py data/{movie_name}/book processed/{movie_name}/book_emotions/
```

3. Segment the book

```
python scripts/text-segment.py data/{movie_name}/book processed/{movie_name}/text_features processed/{movie_name} text_segments/
```

## 3. Process the Audio

1. Extract emotions by running `scripts/extractemotion.m` in MATLAB. Edit line `1` to change the path to the soundtrack (MP3 files). Save the extracted emotion files to an appropriate directory.

2. Segment the audio using `segment_audio.m`. Edit line `1` to change the path. Run `emotionToPython.m` to convert the data to python friendly files. Save the files to an appropriate directory.

3. Run shazam over the movie track (will take time)

```
python scripts/music-detect.py data/<movie_name>/audio.wav processed/<movie_name>/songInfo.npy
```

## 4. Align Book-Movie and Generate Soundtrack

1. Open the notebook `book-movie-align.ipynb` and run all cells. This alignment process is quite involved, so its better to run the cells one by one and set the file paths as prompted. Follow some of the instructions in the notebook to check if the data is processed correctly.

2. Open the notebook `alignment-2-soundtrack.ipynb` and run all cells. This is quite an involved process, so best to follow the instructions in the notebook and change file paths as required.