import random

COLOR_BLANK = "\033[0;0m"
# Green
COLOR_WALL_ONE = "\033[0;37;48;2;0;130;76m"
# Brown
COLOR_WALL_TWO = "\033[0;37;48;2;102;51;0m"
# Gray
COLOR_WALL_THREE = "\033[0;37;48;2;75;75;75m"

'''
The map is handled in a cartesian plane with an inverted y for Quadrant IV. To go Right, X + 1; To go Down, Y + 1.
Map is drawn left to right, top to bottom. Each coordinate is stored in a overall map list. Each coordinate is a dict
to store: X position, Y position, current entity in that position, as well as that entities icon and color. 
When drawing the map, each entity type has a unique icon, and color given in the color consts above. To speed up the 
access of position rather than scanning each component of the map data list, each item is presumed to be in order, 
so the method "coord_to_series()" will convert given X, Y coordinates to the items position in the map_data list.
'''


class CreateMap:
	def __init__(self, width, height, air_count):
		self.map_height = height
		self.map_width = width
		self.map_data = [[{} for y in range(self.map_height)] for x in range(self.map_width)]
		self.map_icons = (["   "] * air_count) + [" % ", " # ", " $ "]
		self.generate()

	# TODO Just generate walls with random colors? Essentially eliminate the need for % $ #
	def generate(self):
		for y in range(self.map_height):
			for x in range(self.map_width):
				working_cords = self.map_data[x][y]
				working_cords["icon"] = random.choice(self.map_icons)
				if working_cords['icon'] == '   ':
					working_cords["entity"] = "Air"
					working_cords['icon_color'] = COLOR_BLANK
				elif working_cords['icon'] == ' # ':
					working_cords['icon'] = '   '
					working_cords['entity'] = "Wall"
					working_cords['icon_color'] = COLOR_WALL_ONE
				elif working_cords['icon'] == ' % ':
					working_cords['icon'] = '   '
					working_cords['entity'] = "Wall"
					working_cords['icon_color'] = COLOR_WALL_TWO
				elif working_cords['icon'] == ' $ ':
					working_cords['icon'] = '   '
					working_cords['entity'] = "Wall"
					working_cords['icon_color'] = COLOR_WALL_THREE

	def display(self):
		for y in range(self.map_height):
			display_string = []
			for x in range(self.map_width):
				coordinate = self.map_data[x][y]
				display_string.append(COLOR_BLANK)
				display_string.append(coordinate['icon_color'] + coordinate['icon'])
			display_string.append(COLOR_BLANK)
			print(''.join(display_string))

	def empty_spaces(self):
		available_spots = []
		for y in range(self.map_height):
			for x in range(self.map_width):
				if self.map_data[x][y]['entity'] == "Air":
					available_spots.append({'x': x, 'y': y})
		return available_spots

	def check_position(self, location):
		if (location['x'] >= self.map_width) or (location['x'] < 0) or \
				(location['y'] >= self.map_height) or (location['y'] < 0):
			return 'Wall'
		coordinate = self.map_data[location['x']][location['y']]
		return coordinate['entity']

	# TODO: Add exception if Entity is blank but Empty is True
	def update(self, location, entity=None, empty=False):
		coordinate = self.map_data[location['x']][location['y']]
		if empty:
			coordinate['icon'] = "   "
			coordinate['icon_color'] = COLOR_BLANK
			coordinate['entity'] = 'Air'
		else:
			coordinate['icon'] = entity.icon
			coordinate['icon_color'] = entity.icon_color
			coordinate['entity'] = entity
