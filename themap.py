import random
import sys


class CreateMap:
	def __init__(self, width, height):
		self.map_height = height
		self.map_width = width
		self.map_data = []
		self.usable_pieces = (["   "] * 15) + [" % ", " # ", " $ "]
		self.generate_terrain()

	def generate_terrain(self):
		print("Generating Map Data")
		for y in range(self.map_height):
			for x in range(self.map_width):
				working_cords = {"x": x, "y": y}
				random_piece = random.randint(0, (len(self.usable_pieces) - 1))
				working_cords["piece"] = self.usable_pieces[random_piece]
				if random_piece != '   ':
					working_cords["entity_id"] = "Wall"
				else:
					working_cords['entity_id'] = "Air"
				self.map_data.append(working_cords)
		print("Finished Generating Map Data")

	def print_to_screen(self):
		pos = -1
		for y in range(self.map_width):
			sys.stdout.write("\033[0;0m")
			print('\r')
			for x in range(self.map_height):
				pos += 1
				coordinate = self.map_data[pos]
				sys.stdout.write("\033[0;0m")
				if coordinate['piece'] == " ■ ":
					sys.stdout.write("\033[1;33m")
					sys.stdout.write("" + (coordinate['piece']))
				elif coordinate['piece'] == " F ":
					sys.stdout.write("\033[1;32m")
					sys.stdout.write("" + (coordinate['piece']))
				elif coordinate['piece'] == " E ":
					sys.stdout.write("\033[1;31m")
					sys.stdout.write("" + (coordinate['piece']))
				elif coordinate['piece'] == " I ":
					sys.stdout.write("\033[1;36m")
					sys.stdout.write("" + (coordinate['piece']))
				elif coordinate['piece'] == " # ":
					sys.stdout.write("\033[0;37;47m")
					sys.stdout.write("   ")
				elif coordinate['piece'] == " % ":
					sys.stdout.write("\033[0;37;46m")
					sys.stdout.write("   ")
				elif coordinate['piece'] == " $ ":
					sys.stdout.write("\033[0;37;45m")
					sys.stdout.write("   ")
				else:
					sys.stdout.write("\033[0;0m")
					sys.stdout.write("" + (coordinate['piece']))
				# break
				sys.stdout.write("\033[0;0m")

	def empty_spaces(self):
		available_spots = []
		for coordinate in self.map_data:
			if coordinate['piece'] == "   ":
				available_spots.append(coordinate)
		return available_spots

	def position_not_occupied(self, requested_loc):
		for coordinate in self.map_data:
			if (coordinate['x'] == requested_loc['x']) and (coordinate['y'] == requested_loc['y']):
				if coordinate['piece'] == "   ":
					return 'Air'
				else:
					return coordinate['entity_id']

	def map_update(self, entity_id, empty=False):
		for coordinate in self.map_data:
			if (coordinate['x'] == entity_id.location['x']) and (coordinate['y'] == entity_id.location['y']):
				if empty:
					coordinate['piece'] = "   "
					coordinate['entity_id'] = 'Air'
				else:
					coordinate['piece'] = entity_id.icon
					coordinate['entity_id'] = entity_id
				break

