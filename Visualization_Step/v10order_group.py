	#Travelling salesman implementation for connecting the wireframe points
#Use closest point method

import math

#DOES NOT NEED ANY CHANGES

point_list = []
ordered_point_list = []
ordered_coords = []

class Point:
	def __init__(self, x_val, y_val):
		global point_list
		global ordered_point_list
		self.x_val = x_val
		self.y_val = y_val
		self.coords = [x_val, y_val]

		point_list.append(self)
		ordered_point_list.append(self)

	def swap(self, index2, chosen_list):
		index1 = chosen_list.index(self)
		chosen_list[index1], chosen_list[index2] = chosen_list[index2], chosen_list[index1]

	def distance_from_point(self, other):	
		return(math.dist(self.coords, other.coords))

	def next_closest_point(self, chosen_list):
		start_index = chosen_list.index(self) + 1

		current_closest_point_distance = [chosen_list[start_index], Point.distance_from_point(self, chosen_list[start_index])]

		for point in chosen_list[start_index:]:
			cur_distance = Point.distance_from_point(self, point)
			if  cur_distance < current_closest_point_distance[1]:
				current_closest_point_distance = [point, cur_distance]
		return(current_closest_point_distance[0])



def evaluate_route():
	distance_traveled = 0
	for i in range(len(ordered_point_list) - 1):
		distance_traveled += Point.distance_from_point(ordered_point_list[i], ordered_point_list[i+1])
	return(distance_traveled)



def strategy_closest_point():
	global ordered_point_list
	for point_index in range (len(point_list) - 1):
		cur_point = ordered_point_list[point_index]
		Point.swap(Point.next_closest_point(cur_point, ordered_point_list), point_index + 1, ordered_point_list)
	print("Route Length: ", evaluate_route())
	



def main(group):
	global ordered_point_list
	global point_list
	global ordered_coords
	ordered_point_list, point_list, ordered_coords = [], [], []
	
	for coords in group:
		Point(coords[0], coords[1])
	strategy_closest_point()
	for point in ordered_point_list:
		ordered_coords.append(point.coords)
	
	return(ordered_coords)
	
