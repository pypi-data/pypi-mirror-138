from typing import *
import numpy as np
from PIL import Image
from enum import Enum
from random import randint
import os
import ntpath
import posixpath

class ImageFlip(Enum):
	"""Specifies how the image will be flipped"""
	VERTICAL   = 0
	HORIZONTAL = 1

def rotate_image(image: Image, angle: float, out_path: str = None) -> Image:
	"""
	Rotates the image by the given angle and saves it if specified

	Parameters
	----------
	image : Image
		The image to rotate
	angle : float
		The number of degrees to rotate the image
	out_path : str
		The path to save the image.\n
		DEFAULT: None

	Returns
	-------
	Image
		The rotated image
	"""
	output_image = image.rotate(angle)
	if out_path is not None:
		output_image.save(out_path)
	return output_image

def flip_image(image: Image, state: ImageFlip, out_path: str = None) -> Image:
	"""
	Flips the image as specified by the state

	Parameters
	----------
	image : Image
		The image to flip
	state : ImageFlip
		Specifies how the image will be flipped.
	out_path : str
		The path to save the file

	Returns
	-------
	Image
		The flipped image
	"""
	# Generates The Output Image
	output_image = None
	if (state == ImageFlip.VERTICAL):
		output_image = image.transpose(Image.FLIP_LEFT_RIGHT)
	elif (state == ImageFlip.HORIZONTAL):
		output_image = image.transpose(Image.FLIP_TOP_BOTTOM)

	# Saves The Output Image
	if out_path is not None:
		output_image.save(out_path)

	return output_image

def randomize_image_color(image: Image, path: str = None) -> Image:
	"""
	Randomly changes the image's color

	Parameters
	----------
	image : Image
		The image to modify
	path : str
		The path where the new image will be saved

	Returns
	-------
	Image
		The modified image
	"""
	# Converts the image into a 3-channel RGB array
	img = image.convert("RGB")
	img_data = img.getdata()

	# Gets the new RGB value
	output_image = Image.new("RGB", image.size)
	output_image_value = []

	r_delta = randint(0, 256)
	g_delta = randint(0, 256)
	b_delta = randint(0, 256)

	for value in img_data:
		r = abs(value[0] - r_delta)
		g = abs(value[1] - g_delta)
		b = abs(value[2] - b_delta)
		output_image_value.append((r, g, b))

	output_image.putdata(output_image_value)

	# Saves the output image
	if path is not None:
		output_image.save(path)

	return output_image

def get_file_name_from_path(path: str) -> str:
	"""
	Extracts the filename from a path-like string

	Parameters
	----------
	path : str
		A path like string to extract the file name from. Works on both
		Windows and POSIX systems.

	Returns
	-------
	str
		The name of the file
	"""
	if os.name == "nt":
		return ntpath.basename(path)
	else:
		return posixpath.basename(path)

def print_progress_bar(current: int, total: int, bar_length: int = 30):
	"""
	Prints a CLI progress bar

	Parameters
	----------
	current : int
		How much we have progressed
	total : int
		The number of steps we need to progress
	bar_length : int
		How long the bar will be
	"""
	percent = "{:.2f}".format(100 * (current / float(total)))
	fill_progress = int(bar_length * current // total)
	bar = "=" * (fill_progress-1) + ">" + "." * (bar_length - fill_progress)
	print(f"\rProgress: |{bar}| {percent}% {current}/{total}", end = "\r")

	if current == total:
		print()

def trim_data(data: np.ndarray, batch_size: int):
	"""
	Trims out the extra data that does not fit into batches

	Parameters
	----------
	data: ndarray
	  The data that you want to trim
	batch_size: int
	  The batch size
	"""
	extra = data.shape[0] % batch_size
	if (extra == 0):
		return data
	return data[:-extra]

def resize_image_keep_ratio(image: Image, size: int, path: str = None, based_on_width: bool = False) -> Image:
	"""
	Resizes the input image and keep the aspect ratio

	Parameters
	----------
	image : Image
		The image you want to be resized
	size : int
		If based_on_width is False, size is the height of the new image. If it is True, size is the width of the new image
	path : str
		The path to save the new image
	based_on_width : bool
		Determines whether size is the height or width of the new image

	Returns
	-------
	Image
		The output image
	"""
	# Finding the Original Image's Ratio
	width, height = image.size
	ratio = width/height

	# Calculating the dimensions of the new Image
	new_height, new_width = (0, 0)
	if not based_on_width:
		new_height = size
		new_width  = int(size * ratio)
	else:
		new_width  = size
		new_height = int(size / ratio)

	output_image = image.resize((new_width, new_height))

	# Saves the new Image
	if path is not None:
		output_image.save(path)
	return output_image
