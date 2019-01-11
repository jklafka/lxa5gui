import svgwrite
import sys
import gui_crab_nebula
import subprocess
import math
import numpy as np

BASE_SIZE = 12


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
		'''
		Adds an additional inner_box under data_box paired with how
		many inner boxes were added previously. 
		'''
		self._num_inner += 1
		self.inner_boxes.append([inner_box, self._num_inner])
		return 


	def sort(self, crit, reverse_tf = False):
		'''
		[Currently not in use] Sort the inner_boxes according to criterion 
		crit, in reverse if reverse_tf is True. 
		'''
		if self.my_type == "stack" and self.text is None: #is outer_box
			if crit == "suffixes":
				self.inner_boxes.sort(lambda x: x[0].text[1], reverse = reverse_tf)
			elif crit == "stems":
				self.inner_boxes.sort(lambda x: x[0].text[0], reverse = reverse_tf)
			elif crit == "robustness":
				self.inner_boxes.sort(lambda x: x[0].text[2], reverse = reverse_tf)
		return 


	def filter(self, crit, level):
		'''
		Filter the inner_boxes according to criterion crit and condition level.
		'''
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
					((upper_left[0] + BASE_SIZE) + (box_size[0] /  num_inner) * i, \
						upper_left[1] + BASE_SIZE), \
					((box_size[0] / num_inner) -  2 * BASE_SIZE, box_size[1] -  2 * BASE_SIZE)))
				i += 1
		else:
			words_list = []
			for num in np.random.randint(0, len(self.data_box.text), \
					min(5, len(self.data_box.text) - 1)):
				words_list.append(self.data_box.text[num])
			self.add_text(self._svg, words_list, \
				(upper_left[0] + 2 * BASE_SIZE, upper_left[1] + box_size[1] / 2)) 


	def draw_box(self, svg, upper_left, box_size): 
		'''
		Draw box of size box_size in pixels with upper left corner located
		at coordinates upper_left in pixels on canvas svg. 
		'''
		svg.add(svg.rect(insert = upper_left,
                                   size = box_size,
                                   stroke_width = "5",
                                   stroke = "black",
                                   fill = "rgb(128,0,0)"))


	def add_text(self, svg, text, location):
		'''
		Draw text at location in pixels on canvas svg. 
		'''
		svg.add(svg.text(text, insert = location))


def get_robustness(stem_box, suffix_box, num_stems, num_suffixes):
	'''
	Compute the robustness of a signature data_box with stems in stem_box, 
	suffixes in suffix_box, number of stems num_stems and number of suffixes
	num_suffixes. 
	'''
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


def make_sig_box(suffixes, stems):
	'''
	Given a tuple of stems and a tuple of suffixes, 
	create a data_box with a data_box containing the stems
	and a data_box containing the suffixes as inner_boxes. 
	'''
	sig_box = data_box("row", None)
	stem_box = data_box("stack", list(stems))
	suffix_box = data_box("stack", list(suffixes))
	num_stems = len(stem_box.text)
	num_suffixes = len(suffix_box.text)
	sig_box.include_box(stem_box)
	sig_box.include_box(suffix_box)
	sig_box.text = [num_stems, num_suffixes, get_robustness(stem_box, \
		suffix_box, num_stems, num_suffixes)]
	return sig_box


def main(signatures_filename, sort_crit=None, filter_crit=None, zoom=100):
	'''
	Construct the data_boxes and their graphical graphics_box representations. 
	Then draw the graphics_boxes on an SVG image.
	'''
	zoom = float(zoom/100)
	signatures = gui_crab_nebula.main(signatures_filename) # dict maps suffixes to stems
	outer_box = data_box("stack", None)
	outer_box.text = 0
	for key, val in signatures.items():
		outer_box.include_box(make_sig_box(key, val))
		outer_box.text += 1

	if filter_crit is not "None":
		filter_list = filter_crit.split('=')

	if sort_crit is not None: 
		if sort_crit == "robustness":
			outer_box.inner_boxes.sort(lambda x : x[0].text[2])
		elif sort_crit == "stems":
			outer_box.inner_boxes.sort(lambda x : x[0].text[0])
		elif sort_crit == "suffixes":
			outer_box.inner_boxes.sort(lambda x : x[0].text[1])		

	svg_document = svgwrite.Drawing(filename = "crab_nebula.svg",
                            size = (1000 * zoom, \
                            (outer_box.text * (100 + BASE_SIZE) - 300) * zoom),
                            style="font-size:{}".format(16 * zoom))
	box_param = 100 #math.ceil(1000/outer_box.text)
	for box in outer_box.inner_boxes:
		graphics_box(box[0], svg_document, \
			(100 * zoom, zoom * (box[1] * box_param)), \
			(800 * zoom, zoom * (box_param - BASE_SIZE)))
	svg_document.save()


if __name__ == "__main__":
	if len(sys.argv) > 2:
		main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	else:
		main(sys.argv[1])