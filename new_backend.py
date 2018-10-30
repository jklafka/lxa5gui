import svgwrite
import sys
import crab_nebula_klafka
import subprocess

class data_box(object):
	'''
	Abstract representation of each box. The boxes represent any 
	organizing unit within the final output of the program, from 
	the largest box containing everything else	to the boxes containing 
	groups of stems or suffixes. 
	'''
	def __init__(self, name, my_type, text):
		self.name = name
		self.my_type = my_type # "row" or "stack" 
		self._inner_boxes = [] # list of data_box objects
		self._num_inner = 0
		self.text = text # can be empty, or stems or suffixes

	def include_box(self, inner_box):
		self._num_inner += 1
		self._inner_boxes.append([inner_box, self._num_inner])
		return 

	def sort(self, criterion, type):
		## sort by number of suffixes
		## sort by number of stems
		## sort by robustness


	def filter(self, criterion, type):
		## filter by number of suffixes
		## filter by whether the signature contains certain suffixes


	def get_inner_boxes(self):
		'''
		Returns a list of the names of the boxes in self._inner_boxes
		'''
		return [item[0] for item in self._inner_boxes]

	def delete_inner_box(self, box_name):
		'''
		Given the name of an inner box (a box that lives inside the data_box, 
		deletes that box from the list of inner_boxes.
		'''
		self._inner_boxes = [item for item in self._inner_boxes \
			if item[0].name != box_name]
		return


class graphics_box(object):
	"""
	The actual graphical representation of a group of suffixes, a group of
	stems or a group of smaller boxes. 
	"""
	def __init__(self, data_box, svg, drawn):
		self._inner_boxes = []
		self._draw_box(data_box.text, upper_left, box_size, svg)

		for inner_box in data_box.get_inner_boxes():
			self._inner_boxes.append(graphics_box(inner_box[0], svg, drawn))

	def _draw_box(self, text, upper_left, box_size, svg):
		svg.add(svg_document.rect(insert = upper_left,
                                   size = box_size,
                                   stroke_width = "5",
                                   stroke = "black",
                                   fill = "rgb(128,0,0)"))

	#def zoom(self, percentage):
	## still have to implement


def main(signatures_filename, font_size):
	signatures = crab_nebula_klafka.main(signatures_filename) # dict maps suffixes to stems
	suff_dict = {}
	stem_dict = {}
	stem_str = ""
	iden = 0
	for suffixes, stems in signatures.items():
		suff_dict[suffixes] = iden
		for stem in stems: 
			stem_dict[stem] = iden
			stem_str += stem
			stem_str += " "
		iden += 1
	file = open("stems.txt", 'w')
	file.write(stem_str)
	file.close()
	stem_sigs = crab_nebula_klafka.main("stems.txt")
	#subprocess.call(["rm", "stems.txt"])


	svg_document = svgwrite.Drawing(filename = "test-svgwrite.svg",
                            size = ("1000px", "1000px"))

if __name__ = "__main__":
	main(sys.argv[1], sys.argv[2])