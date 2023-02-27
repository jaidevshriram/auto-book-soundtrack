folder = './data//HP/soundtrack/';
audio_files = dir(folder);

for i = 1:numel(audio_files)
    if audio_files(i).isdir
        continue;
    end
    
    song_folder = audio_files(i).folder;
    song_name = audio_files(i).name;
    song_path = fullfile(song_folder, song_name);
    
    info = audioinfo(song_path);
    total_time = info.Duration;
    
    novel = mirnovelty(mirsimatrix(mirkeystrength(song_path,'Frame',10, 0.85)), 'Width', 64);
    novel_peaks = mirpeaks(novel, 'Threshold', 0.5);
    novel_peaks = mirgetdata(novel_peaks);
    
    [m, n] = size(novel_peaks);
    segments = {};
    
    prev_time = -100;
    
    for j = 1:n
        end_t = novel_peaks(2, j);        
        
        if ((start_t+end_t)/2 - prev_time < 30 && (start_t+end_t)/2 > prev_time ) || (prev_time - (start_t+end_t)/2 < 30 && prev_time > (start_t+end_t)/2)
            disp("Continuing");
            disp(start_t);
            disp(end_t);
            disp(prev_time);
            continue
        end
            
        segments = [segments, (start_t+end_t)/2];
        prev_time = (start_t+end_t)/2;
    end
    
    segments = sort(cell2mat(segments));
    
    segment_mode_info = [];
    start = 0;
    for j = 1:numel(segments)
        segment_mode_info = [segment_mode_info, mean(mirgetdata(mirmode(miraudio(song_path, 'Extract', start, segments(j)), 'Frame', 5)))];
        start = segments(j);
    end
    segment_mode_info = [segment_mode_info, mean(mirgetdata(mirmode(miraudio(song_path, 'Extract', segments(numel(segments)), total_time), 'Frame', 5)))];
    
    segment_rms_info = [];
    start = 0;
    for j = 1:numel(segments)
        segment_rms_info = [segment_rms_info, mean(mirgetdata(mirrms(miraudio(song_path, 'Extract', start, segments(j)), 'Frame', 5)))];
        start = segments(j);
    end
    segment_rms_info = [segment_rms_info, mean(mirgetdata(mirrms(miraudio(song_path, 'Extract', segments(numel(segments)), total_time), 'Frame', 5)))];

    song_segmented.segments = segments;    
    song_segmented.mode = segment_mode_info;
    song_segmented.rms = segment_rms_info;
    
    song_segmented_json = jsonencode(song_segmented);
    
%    sp = mirsegment(song_path, 'Keystrength', 'Frame', 10, 0.85);
%    segments = get(sp, 'FramePos');
    
    saveFileName = [erase(song_name, '.mp3'), '.mat'];
    save(saveFileName, 'song_segmented_json');
    
%    break;
end