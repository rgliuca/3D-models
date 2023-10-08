import math
import cadquery as cq

diameter = 85
mesh_width = 2
mesh_spacing = 2
height = 0.6 


result = cq.Workplane("front").circle(diameter/2)  # current point is the center of the circle, at (0, 0)
for y in range(0, diameter//2, mesh_width + mesh_spacing):
    x_len = int(((diameter//2) ** 2 - y ** 2) ** 0.5) * 2
    n_squares = x_len // (mesh_width + mesh_spacing) 
    start_offset = (x_len - n_squares * mesh_width - (n_squares - 1) * mesh_spacing) / 2
    print(f"{n_squares=}, {start_offset=}")
    if n_squares >= 1:
        for n in range(n_squares):
            x = int(-x_len/2 + start_offset + mesh_width/2 + n * (mesh_width + mesh_spacing)) 
            result.center(x, y).rect(mesh_width, mesh_width)

for y in range(-mesh_width - mesh_spacing, -diameter//2, -mesh_width - mesh_spacing):
    x_len = int(((diameter//2) ** 2 - y ** 2) ** 0.5) * 2
    n_squares = x_len // (mesh_width + mesh_spacing) 
    start_offset = (x_len - n_squares * mesh_width - (n_squares - 1) * mesh_spacing) / 2
    print(f"{n_squares=}, {start_offset=}")
    if n_squares >= 1:
        for n in range(n_squares):
            x = int(-x_len/2 + start_offset + mesh_width/2 + n * (mesh_width + mesh_spacing)) 
            result.center(x, y).rect(mesh_width, mesh_width)
#result = result.center(0, 0).rect(mesh_width, mesh_width)  # new work center is (1.5, 0.0)

#result = result.center(-1.5, 1.5).circle(0.25)  # new )work center is (0.0, 1.5).
# The new center is specified relative to the previous center, not global coordinates!

result = result.extrude(height)

#result = result.center(0, 0).rect(2, 2).extrude(5)

e = cq.exporters.export
e(result, 'out.stl')

