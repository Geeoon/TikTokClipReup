import cv2
import os
import numpy as np

if __name__ == "__main__":
	PRIMARY_PATH = "D:\\Video Projects\\Videos\\Misc\\Primary\\Make Believe.mp4"
	SECONDARY_DIR = "D:\\Video Projects\\Videos\\Misc"
	secondary_videos = []
	for file in os.listdir(SECONDARY_DIR):
		if file.endswith(".mp4"):
			secondary_videos.append(os.path.join(SECONDARY_DIR, file))
	
	size = (1080, 1920)  # tiktok resolution, although it may be sligithly different

	