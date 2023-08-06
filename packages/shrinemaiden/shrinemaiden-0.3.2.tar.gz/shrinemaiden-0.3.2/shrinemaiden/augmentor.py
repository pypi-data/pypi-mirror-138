from shrinemaiden.util import *
from PIL import Image
from typing import *
from dataclasses import dataclass, field
import random
import os

@dataclass
class ImageCategory:
	"""Class for keeping track of the image label and its paths"""
	label: str
	path : str
	image_paths: List[str] = field(default_factory=list)

class ImageAugmentor:
	"""Augments the images"""
	def __init__(self, path: str = None, new_size: float = None, size_is_width: bool = False):
		"""
		Parameters
		----------
		path : str
			The path to the root image directory\n
			DEFAULT: None
		new_size : float
			The new size of the image. If not specified, the images won't be resized\n
			DEFAULT: None
		size_is_width : bool
			Determines whether the specified new_size is the width of the new image
			DEFAULT: False
		"""
		self.base_path = path
		self.image_categories = []
		self.total_image_number = 0
		self.new_size = new_size
		self.size_is_width = size_is_width

		if path is not None:
			assert os.path.exists(self.base_path), "Path doesn't exist"
			self.load_image_from_directory(self.base_path)
		else:
			print("Path not specified. Please run load_image_from_directory before augmentation")

	def load_image_from_directory(self, path: str):
		"""
		Loads the images into the augmentor

		Parameters
		----------
		path : str
			A path-like string that leads to the directory containing
			the images to be augmented
		"""
		assert os.path.exists(path), "Path doesn't exist"

		if self.base_path is None:
			self.base_path = path

		# Iterate through each label
		for label in os.listdir(path):
			image_label_path = os.path.join(path, label)
			category = ImageCategory(label, image_label_path)

			# Iterate through each image
			for image_file_name in os.listdir(image_label_path):
				if not (image_file_name.endswith(".jpg") or image_file_name.endswith(".png") or image_file_name.endswith(".bmp")):
					continue
				image_path = os.path.join(image_label_path, image_file_name)
				category.image_paths.append(image_path)

			self.image_categories.append(category)
			self.total_image_number += len(category.image_paths)

	def augment(self, output_path: str, rotate_degree: float = 45.0, flip: str = "none", color_adjustment_prob: float = 0.0, copy_original: bool = True):
		"""
		Starts the image augmentation process
		output_path : str
			Which folder to save the file in. The folder will be created
			if it doesn't exist.
		rotate_degree : float
			How many degrees to rotate the image each time\n
			DEFAULT = 45.0
		flip : str
			Determines if and how the image will be flipped\n
			none       = No flipping\n
			vertical   = Vertical flipping only\n
			horizontal = Horizontal flipping only\n
			both       = Both vertical and horizontal flipping\n
			DEFAULT: "none"
		color_adjustment_prob : float
			The chance for the image's hue to randomly be adjusted\n
			DEFAULT: 0.0
		copy_original : bool
			Whether to copy the original file into the output folder or not\n
			DEFAULT: True
		"""
		assert output_path is not None and output_path != "", "Output path is missing"
		assert abs(color_adjustment_prob) <= 1.0, "Color adjustment_probability is not between 0 and 1"

		# Checks if the output directory exists, if not create one
		if not os.path.exists(output_path):
			os.mkdir(output_path)

		current_progress = 0

		# Iterates through each 'label' directories
		for category in self.image_categories:
			output_category_path = os.path.join(output_path, category.label)

			# Checks if the output 'label' directory exists, if not create one
			if not os.path.exists(output_category_path):
				os.mkdir(output_category_path)

			# Iterates through each label
			for image_path in category.image_paths:
				image_file_name = get_file_name_from_path(image_path)
				image = Image.open(image_path)

				# Determines whether to resize the Image
				if self.new_size is not None:
					new_image = resize_image_keep_ratio(
						image,
						size=self.new_size,
						based_on_width=self.size_is_width
					)
					image.close()
					image = new_image

				# Determines whether or not to copy the original image to the location directory
				# If a new size is specified, the resized image will be saved instead
				if copy_original:
					new_image_path = os.path.join(output_category_path, image_file_name)
					image.save(new_image_path)

				# Determines how many times the image can be rotated
				rotate_output_no = int(360 // rotate_degree)
				for i in range(rotate_output_no):
					if rotate_degree * (i+1) >= 360.0:
						continue

					# Determines whether the image's color will be randomized
					color_randomization_probability = random.uniform(0, 1.0)
					randomize = color_randomization_probability <= color_adjustment_prob

					# Generates the output image's name
					new_image_file_name_prefix = "aug_" + str(rotate_degree * (i + 1)) + "_"
					new_image_file_name = new_image_file_name_prefix + image_file_name
					new_image_path = os.path.join(output_category_path, new_image_file_name)

					# Rotates the image and save it on at a designated path
					if not randomize:
						rotate_image(image, rotate_degree * (i+1), new_image_path)
					else:
						new_image = rotate_image(image, rotate_degree * (i+1))
						randomize_image_color(new_image, new_image_path)

				# Determines how the image will be flipped
				if flip == "vertical" or "both":
					# Determines whether the image's color will be randomized
					color_randomization_probability = random.uniform(0, 1.0)
					randomize = color_randomization_probability <= color_adjustment_prob

					# Generates the new image's file name
					new_image_file_name_prefix = "aug_vertical_"
					new_image_file_name = new_image_file_name_prefix + image_file_name
					new_image_path = os.path.join(output_category_path, new_image_file_name)

					# Flips the image and save it
					if not randomize:
						flip_image(image, ImageFlip.VERTICAL, new_image_path)
					else:
						new_image = flip_image(image, ImageFlip.VERTICAL)
						randomize_image_color(new_image, new_image_path)

				if flip == "horizontal" or "both":
					# Determines whether the image's color will be randomized
					color_randomization_probability = random.uniform(0, 1.0)
					randomize = color_randomization_probability <= color_adjustment_prob

					# Generates the new image's file name
					new_image_file_name_prefix = "aug_horizontal_"
					new_image_file_name = new_image_file_name_prefix + image_file_name
					new_image_path = os.path.join(output_category_path, new_image_file_name)

					# Flips the image and save it
					if not randomize:
						flip_image(image, ImageFlip.HORIZONTAL, new_image_path)
					else:
						new_image = flip_image(image, ImageFlip.HORIZONTAL)
						randomize_image_color(new_image, new_image_path)

				# Closes the image
				image.close()

				# Updates and prints the progress bar
				current_progress += 1
				print_progress_bar(current_progress, self.total_image_number)

	def get_image_root_path(self) -> str:
		"""
		Returns the root image directory path

		Returns
		-------
		str
			The root path to the image directory
		"""
		return self.base_path

	def get_image_labels(self) -> Tuple[str]:
		"""
		Returns a tuple containing the labels of the images

		Returns
		-------
		Tuple[str]
			A tuple containing the labels of the images
		"""
		return ([category.label for category in self.image_categories])

	def get_category_objects(self) -> Tuple[ImageCategory]:
		"""
		Returns ImageCategory objects

		Returns
		-------
		Tuple[str]
			A tuple containing the ImageCategory objects
		"""
		return ([category for category in self.image_categories])

	def get_total_image_number(self) -> int:
		"""
		Returns the number of images to be processed

		Returns
		-------
		int
			The total number of images to be processed
		"""
		return self.total_image_number
