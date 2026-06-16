

import math

def vector_to_coord(vector):
    if vector[0] == 0:
        return 0, 0
    if vector[1] == 0 or vector[1] == 360: return vector[0], 0
    if vector[1] == 90: return 0, vector[0]
    if vector[1] == 180: return -vector[0], 0
    if vector[1] == 270: return 0, -vector[0]
    return vector[0] * math.cos(math.radians(vector[1])), vector[0]*math.sin(math.radians(vector[1]))
def coord_to_vector(coord):
    magnitude = math.sqrt((coord[0]) ** 2 + (coord[1]) ** 2)
    if coord[0] == 0:
        if coord[1] > 0:
            direction = 90
        else:
            direction = 270
    else:
        direction = math.degrees(math.atan((abs(coord[1])) / (abs(coord[0]))))
        if coord[0] < 0:
            if coord[1] > 0:
                direction = 180 - direction
            else:
                direction += 180
        elif coord[1] < 0:
            direction = 360 - direction
    return magnitude, direction
# print(vector_to_coord((33, 136)))
# for degree in range(360):
#     result_coord = vector_to_coord((1, degree))
#     result_degree = coord_to_vector(result_coord)[1]
#     if result_degree > degree + 1 or result_degree < degree - 1:
#         print(str(degree) + " : " + str(result_degree) + " : " + str(result_coord))
