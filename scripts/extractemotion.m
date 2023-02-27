folder = './data/hp/music/';
audio_files = dir(folder);

for i = 1:numel(audio_files)
    if audio_files(i).isdir
        continue;
    end
    
    song_folder = audio_files(i).folder;
    song_name = audio_files(i).name;
    song_path = fullfile(song_folder, song_name);
    
    song_emotion = getEmotion(song_path);
    
    saveFileName = [erase(song_name, '.mp3'), '.mat'];
    save(saveFileName, 'song_emotion');
end

function out = getEmotion(songPath)
    emotion = miremotion(songPath, 'Frame', 4, 1);
    out = emotion;
end

function out = emotion2Vals(emotion)
    out = cell2mat(emotion{1})
end