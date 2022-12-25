import cv2
import os
import sys
import numpy as np
import moviepy.editor as mp  

# Example command line usage: 
# py main.py "D:/Video Projects/Videos/Misc/Primary/Make Believe.mp4" "D:/Video Projects/Videos/Misc"

# PRIMARY_PATH = "D:\\Video Projects\\Videos\\Misc\\Primary\\Make Believe.mp4"
# SECONDARY_DIR = "D:\\Video Projects\\Videos\\Misc"
PRIMARY_PATH = sys.argv[1]
SECONDARY_DIR = sys.argv[2]
secondary_video_paths = []
secondary_index = 0
for file in os.listdir(SECONDARY_DIR):
	if file.endswith(".mp4"):
		secondary_video_paths.append(os.path.join(SECONDARY_DIR, file))
size = (1080, 1920)  # tiktok resolution. it may be slightly different
primary_cap = cv2.VideoCapture(PRIMARY_PATH)
secondary_cap = cv2.VideoCapture(secondary_video_paths[secondary_index])
primary_height = int(size[0] / primary_cap.get(cv2.CAP_PROP_FRAME_WIDTH) * primary_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
secondary_height = size[1] - primary_height
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_temp.mp4', fourcc, primary_cap.get(cv2.CAP_PROP_FPS), size)
blank_frame = np.zeros(shape=(size[0], size[1], 3), dtype=np.uint8)
blank_frame = cv2.resize(blank_frame, size)  # no clue why but this makes it work
i = 0
while primary_cap.isOpened():
	ret, primary_frame = primary_cap.read()  # ret is True if there is a frame
	ret2, secondary_frame = secondary_cap.read()
	if not ret:
		print("No more frames can be read.")
		break
	if not ret2:
		i = i+1
		if i >= len(secondary_video_paths):
			i = 0
		secondary_cap = cv2.VideoCapture(secondary_video_paths[secondary_index])
		ret2, secondary_frame = secondary_cap.read()
	output_frame = blank_frame.copy()
	primary_frame = cv2.resize(primary_frame, (size[0], primary_height))  # resize frame to fit output
	# primary_frame = cv2.resize(primary_frame, size)  # resize frame to fit output
	# secondary_frame = cv2.resize(secondary_frame, (size[0], int()))
	secondary_shape = (int(secondary_cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(secondary_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
	secondary_ratio = secondary_shape[0] / secondary_shape[1]
	if secondary_ratio > size[0] / secondary_height:
		# preseve height and clip horizontally
		secondary_shape = (int(secondary_height * secondary_ratio), secondary_height)
		secondary_frame = cv2.resize(secondary_frame, secondary_shape)
		clip_amount = int((secondary_shape[0] - size[0]) / 2)
		secondary_frame = secondary_frame[:, clip_amount:-clip_amount, :]
	else:
		# preserve width and clip vertically; haven't tested tbh
		secondary_shape = (size[0], size[0] * secondary_ratio)
		secondary_frame = cv2.resize(secondary_frame, secondary_shape)
		clip_amount = int((secondary_shape[1] - size[1]) / 2)
		secondary_frame = secondary_frame[clip_amount:-clip_amount, :, :]
	output_frame[primary_height:, :size[1], :] = secondary_frame
	output_frame[:primary_height, :size[1], :] = primary_frame
	out.write(output_frame)
primary_cap.release()
out.release()
primary_clip = mp.VideoFileClip(PRIMARY_PATH)
final_clip = mp.VideoFileClip("output_temp.mp4")
final_clip.audio = primary_clip.audio
final_clip.write_videofile("output.mp4")
os.remove("output_temp.mp4")
