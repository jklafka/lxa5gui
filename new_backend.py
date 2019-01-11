import svgwrite
import sys
import gui_crab_nebula
import subprocess
import math
import numpy as np

FONT_SIZE = 12


class data_box(object):
	'''
	Abstract representation of each box. The boxes represent any 
	organizing unit within the final output of the program, from 
	the largest box containing everything else to the boxes containing 
	groups of stems or suffixes. 
	'''
	def __init__(self, my_type, text):
		self.my_type = my_type # "row" or "stack" 
		self.inner_boxes = [] # list of data_box objects
		self._num_inner = 0
		self.text = text # can be empty, or list of stems/suffixes


	def include_box(self, inner_box):
		self._num_inner += 1
		self.inner_boxes.append([inner_box, self._num_inner])
		return 


	def sort(self, crit, reverse_tf = False):
		if self.my_type == "stack" and self.text is None: #is outer_box
			if crit == "suffixes":
				self.inner_boxes.sort(lambda x: x[0].text[1], reverse = reverse_tf)
			elif crit == "stems":
				self.inner_boxes.sort(lambda x: x[0].text[0], reverse = reverse_tf)
			elif crit == "robustness":
				self.inner_boxes.sort(lambda x: x[0].text[2], reverse = reverse_tf)
		return 


	def filter(self, crit, level):
		if self.my_type == "stack" and self.text is None: #is outer_box
			if crit == "suffixes":
				self.inner_boxes = [box for box in self.inner_boxes \
					if box[0].text[1] >= level]
			elif crit == "stems":
				self.inner_boxes = [box for box in self.inner_boxes \
					if box[0].text[0] >= level]
			elif crit == "robustness":
				self.inner_boxes = [box for box in self.inner_boxes \
					if box[0].text[2] >= level]
			elif crit == "certain suffixes":
				self.inner_boxes = [box for box in self.inner_boxes \
					if suffix in box[0].inner_boxes[1][0] for suffix in level]
		return

		## filter by whether the signature contains certain suffixes

"""
	def delete_inner_box(self, box_name):
		'''
		Given the name of an inner box (a box that lives inside the data_box, 
		deletes that box from the list of inner_boxes.
		'''
		self._inner_boxes = [item for item in self._inner_boxes \
			if item[0].name != box_name]
		return
"""

class graphics_box(object):
	"""
	The actual graphical representation of a group of suffixes, a group of
	stems or a group of smaller boxes. 
	"""
	def __init__(self, data_box, svg, upper_left, box_size):
		#graphics_box.LAYER_NUM += 1
		#self.layer_num = graphics_box.LAYER_NUM
		self._inner_boxes = []
		self._svg = svg
		self.data_box = data_box
		self.draw_box(self._svg, upper_left, box_size)
		if self.data_box.inner_boxes != []:
			i = 0
			num_inner = len(data_box.inner_boxes)
			for inner_box in data_box.inner_boxes:
				self._inner_boxes.append(graphics_box(inner_box[0], svg, \
					((upper_left[0] + FONT_SIZE) + (box_size[0] /  num_inner) * i, upper_left[1] + FONT_SIZE), \
					((box_size[0] / num_inner) -  2 *FONT_SIZE, box_size[1] -  2 * FONT_SIZE)))
				i += 1
		else:
			words_list = []
			for num in np.random.randint(0, len(self.data_box.text), 5):
				words_list.append(self.data_box.text[num])

			self.add_text(words_list, \
				(upper_left[0] + 2 * FONT_SIZE, upper_left[1] + box_size[1] / 2)) 


	def draw_box(self, svg, upper_left, box_size): ##make sure the syntax is right for this
		svg.add(svg.rect(insert = upper_left,
                                   size = box_size,
                                   stroke_width = "5",
                                   stroke = "black",
                                   fill = "rgb(128,0,0)"))


	def add_text(self, text, location):
		self._svg.add(self._svg.text(text, \
	                                   insert = location))
		## add code to check whether the text will overfill the box

	#def zoom(self, percentage):
	## still have to implement

def get_robustness(stem_box, suffix_box, num_stems, num_suffixes):
	n0 = 0
	n1 = 0
	num_letters = 0
	for item in stem_box.text:
		n0 += len(item)
	num_letters += n0
	n0 *= num_suffixes
	for item in suffix_box.text:
		n1 += len(item)
	num_letters += n1
	n1 *= num_stems
	n2 = n1 + n0
	return n2 - num_letters


def make_sig_box(key, val):
	sig_box = data_box("row", None)
	stem_box = data_box("stack", list(val))
	suffix_box = data_box("stack", list(key))
	num_stems = len(stem_box.text)
	num_suffixes = len(suffix_box.text)
	sig_box.include_box(stem_box)
	sig_box.include_box(suffix_box)
	sig_box.text = [num_stems, num_suffixes, get_robustness(stem_box, \
		suffix_box, num_stems, num_suffixes)]
	return sig_box


def main(signatures_filename):
	signatures = gui_crab_nebula.main(signatures_filename) # dict maps suffixes to stems
	outer_box = data_box("stack", None)
	outer_box.text = 0
	for key, val in signatures.items():
		outer_box.include_box(make_sig_box(key, val))
		outer_box.text += 1
#	for box_pair in outer_box.inner_boxes:
#		box_pair[1] = box_pair[0].text
	svg_document = svgwrite.Drawing(filename = "crab_nebula.svg",
                            size = (1000, outer_box.text * (100 + FONT_SIZE) - 300))
	box_param = 100 #math.ceil(1000/outer_box.text)
	for box in outer_box.inner_boxes:
		graphics_box(box[0], svg_document, \
			(100, box[1] * box_param), (800, box_param - FONT_SIZE))
	svg_document.save()

if __name__ == "__main__":
	main(sys.argv[1])