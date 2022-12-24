import cv2
import os
import numpy as np

if __name__ == "__main__":
	PRIMARY_PATH = "D:\\Video Projects\\Videos\\Misc\\Primary\\Make Believe.mp4"
	SECONDARY_DIR = "D:\\Video Projects\\Videos\\Misc"
	secondary_video_paths = []
	for file in os.listdir(SECONDARY_DIR):
		if file.endswith(".mp4"):
			secondary_video_paths.append(os.path.join(SECONDARY_DIR, file))
	size = (1080, 1920)  # tiktok resolution. it may be slightly different
	primary_cap = cv2.VideoCapture(PRIMARY_PATH)
	primary_height = size[0] / primary_cap.get(cv2.CAP_PROP_FRAME_WIDTH) * primary_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	out = cv2.VideoWriter('output.mp4', fourcc, primary_cap.get(cv2.CAP_PROP_FPS), size)
	blank_frame = np.zeros(shape=(size[0], size[1], 3), dtype=np.uint8);
	blank_frame = cv2.resize(blank_frame, size)  # no clue why but this makes it work
	while primary_cap.isOpened():
		ret, primary_frame = primary_cap.read()  # ret is True if there is a frame
		if not ret:
			print("No more frames can be read.")
			break
		output_frame = blank_frame.copy()
		primary_frame = cv2.resize(primary_frame, (size[0], int(primary_height)))  # resize frame to fit output
		# primary_frame = cv2.resize(primary_frame, size)  # resize frame to fit output
		output_frame[0:primary_frame.shape[0], 0:primary_frame.shape[1], :] = primary_frame
		out.write(output_frame)
	primary_cap.release()
	out.release()