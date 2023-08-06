'''
Author: GT<caogtaa@gmail.com>
Date: 2020-12-24 11:14:35
LastEditors: Please set LastEditors
LastEditTime: 2022-02-15 09:51:24
'''
import os
import numpy as np
import copy
import fire
from os import walk
from PIL import Image

class Dilator(object):
	'''
	Dilate texture with low alpha pixel to prevent "black edge" when rendered by GL\n
		dilator dilate_dir $your_dir
		dilator dilate $input_file_path $output_file_path
	'''

	def list_png_files(self, dir, output):
		root, sub_dirs, file_names = next(walk(dir))
		output.extend([os.path.join(root, x) for x in file_names if os.path.splitext(x)[1] == '.png'])
		for sub_dir in sub_dirs:
			self.list_png_files(os.path.join(root, sub_dir), output)

	def dilate_dir(self, dir):
		file_paths = []
		self.list_png_files(dir, file_paths)
		print('\n'.join(file_paths))

		for file_path in file_paths:
			self.dilate(file_path, file_path)

	def dilate(self, input_path, output_path):
		print("[DILATOR] Dilating %s" % input_path)

		old_size = os.path.getsize(input_path)
		with Image.open(input_path) as im:
			if im.format != 'PNG':
				print("[DILATOR] File %s is not PNG, ignore" % input_path)
				return
		
			if im.mode != 'RGBA':
				print("[DILATOR] File %s is not RGBA format, ignore" % input_path)
				return

			row, col = im.size
			origin_data = im.load()

			for i in range(0, row):
				for k in range(0, col):
					color = origin_data[i, k]
					if color[3] >= 3:
						# alpha already larger than threshold
						continue

					# pick colors from 8 directions, ignore colors whose alpha < 30
					# 这么做对同一张图重复扩边不会使扩边增长
					r = 0
					g = 0
					b = 0
					count = 0
					for x in range(-1, 2):
						i_x = i + x
						if i_x < 0 or i_x >= row:
							continue

						for y in range(-1, 2):
							if x == 0 and y == 0:
								# ignore center point
								continue

							k_y = k + y
							if k_y < 0 or k_y >= col:
								continue

							c2 = origin_data[i_x, k_y]
							if c2[3] < 30:
								continue

							# this color is considerable
							count += 1
							r += c2[0]
							g += c2[1]
							b += c2[2]
					# end 8 directions check

					if count > 0:
						# use average color from neighbors
						# alpha = 3
						origin_data[i, k] = (r // count, g // count, b // count, 3)
						# out = origin_data[i, k]
						# out[0] = r / count
						# out[1] = g / count
						# out[2] = b / count
						# out[3] = 3

						# test code (blue outline) (BRG mode)
						# out[0] = 255
						# out[1] = 0
						# out[2] = 0
						# out[3] = 128

			im.save(output_path)
			new_size = os.path.getsize(output_path)
			print("[DILATOR] After dialtion file size %sK -> %sK" % (old_size / 1000, new_size / 1000))

def main():
	fire.Fire(Dilator)

if __name__ == "__main__":
    main()