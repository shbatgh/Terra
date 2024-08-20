import math
import colorsys
import random

def generate_unique_colors(coordinates):
    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def rgb_distance(c1, c2):
        return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)

    def find_furthest_color(existing_colors):
        best_color = None
        max_distance = -1
        for r in range(0, 256, 64):  # Sample RGB space
            for g in range(0, 256, 64):
                for b in range(0, 256, 64):
                    color = (r, g, b)
                    min_dist = min(rgb_distance(color, c) for c in existing_colors)
                    if min_dist > max_distance:
                        max_distance = min_dist
                        best_color = color
        return best_color

    num_colors = len(coordinates)
    sorted_coords = sorted(coordinates, key=lambda p: min(distance(p, q) for q in coordinates if p != q))

    # Start with an arbitrary color
    colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))]
    colors = [(255, 0, 0)]

    max_image_distance = math.sqrt((max(p[0] for p in coordinates) - min(p[0] for p in coordinates))**2 +
                                   (max(p[1] for p in coordinates) - min(p[1] for p in coordinates))**2)

    # Assign the most contrasting color to each subsequent point
    for i in range(1, num_colors):
        nearest_colors = []
        current_distance = 100
        while current_distance <= max_image_distance:
            for c in sorted_coords:
                if distance(c, sorted_coords[i]) <= current_distance:
                    if sorted_coords.index(c) < len(colors):
                        nearest_colors.append(colors[sorted_coords.index(c)])
            if nearest_colors:
                break
            current_distance += 50
        if not nearest_colors:
            nearest_colors = colors
        new_color = find_furthest_color(nearest_colors)
        while new_color in colors:  # Check if the new color already exists
            new_color = (new_color[0] + 1, new_color[1], new_color[2])  # Add 1 to the first value of the color tuple
        colors.append(new_color)

    # Pair coordinates with colors
    color_coord_map = {}
    for coord, color in zip(sorted_coords[:num_colors], colors):
        color_coord_map[color] = coord
    return color_coord_map
