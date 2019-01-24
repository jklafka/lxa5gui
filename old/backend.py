import svgwrite
import sys
import gui_crab_nebula

## rectangle class

def main(font_size, input_file):
	signatures = gui_crab_nebula.main(input_file)
	point_dict = {} #maps each signature to a pair of points representing upper right and lower left
	
	location_counter = 0
	for key, val in signatures.items():
		box_vertical = font_size * (len(key) + 2)
		point_dict[key] = [(100, location_counter + font_size), (800, box_vertical)]
		location_counter += box_vertical 
		location_counter += font_size
	big_box = [(0, 0), None]
	location_counter += font_size
	big_box[1] = (1000, location_counter) #size of outermost box

	svg_document = svgwrite.Drawing(filename = "test-svgwrite.svg",
                                size = ("1000px", str(big_box[1][1]) + "px"))

	#add main rectangle
	svg_document.add(svg_document.rect(insert = (0, 0),
                                   size = ("1000px", str(big_box[1][1]) + "px"),
                                   stroke_width = "5",
                                   stroke = "black",
                                   fill = "rgb(128,0,0)"))

	#add rectangles for each signature
	for key, val in point_dict.items():
		#insert completions
		svg_document.add(svg_document.rect(insert = (700, val[0][1]),
	                                   size = ("200px",  str(val[1][1])+ "px"),
	                                   stroke_width = "1",
	                                   stroke = "black",
	                                   fill = "rgb(211,211,211)"))
		key_string = ""
		for word in key: 
			key_string += "'"
			key_string += word
			key_string += "'" 
			if word != key[-1]:
				key_string += ", "
		svg_document.add(svg_document.text(str(key_string),
	                                   insert = (700 + font_size, val[0][1] + 2 * font_size)))

		#insert stems
		svg_document.add(svg_document.rect(insert = val[0],
	                                   size = ("500px",  str(val[1][1])+ "px"),
	                                   stroke_width = "1",
	                                   stroke = "black",
	                                   fill = "rgb(211,211,211)"))

		stems_list = list(signatures[key])
		m = min([len(key), len(stems_list)])
		stem_string = ""
		for word in stems_list[:m]: 
			stem_string += "'"
			stem_string += word
			stem_string += "'" 
			if word != stems_list[m-1]:
				stem_string += ", "
		svg_document.add(svg_document.text(stem_string + "\n and {} more"\
			.format(len(stems_list) -m),
	                                   insert = (100 + font_size, val[0][1] + 2 * font_size)))


	svg_document.save()


if __name__ == "__main__":
	main(int(sys.argv[1]), sys.argv[2])