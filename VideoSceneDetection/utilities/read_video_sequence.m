function EventsStruct = read_video_sequence(videvents_fname)
% READ VIDEO SEQUENCE reads the shots that were extracted and passes it
% back as a list

verbose = false;

if ~isstr(videvents_fname)
   % assume that the parameter is a video struct
   assert(isstruct(videvents_fname));
   videvents_fname = videvents_fname.labels.videoevents.combined;
end

readme = fopen(videvents_fname,'r');

EventsStruct = struct;
count = 1;

tline = fgetl(readme);
while ischar(tline)
    if strfind(tline,'CVHCI')
        if verbose
            fprintf('Found %s\n',tline);
        end
    else
        a = regexp(tline, ' ', 'split');
        EventsStruct(count).startFrame = str2double(a{1});
        EventsStruct(count).startTime = str2double(a{2});
        EventsStruct(count).type = a{3};
        
        % if endframe and endtime exist, read
        if length(a) > 4 && ~isempty(a{4})
            EventsStruct(count).endFrame = str2double(a{4});
            EventsStruct(count).endTime = str2double(a{5});
        else
            EventsStruct(count).endFrame = -1;
            EventsStruct(count).endTime = -1;
        end
        
        count = count + 1;
    end
    tline = fgetl(readme);
end


fclose(readme);


end

