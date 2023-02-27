VideoStruct = BBT(1, 1); initParams;
ssim = shot_similarity(VideoStruct, params);
[Threads, shot_assigned] = similarity_to_threads(ssim);
visualize_threads_via_htmlrender(VideoStruct, Threads, shot_assigned);
% load
scene_breaks = dp_scenes(VideoStruct, params);
visualize_scenes_via_htmlrender(VideoStruct, scene_breaks, params);
save("scene_detect_output.mat")