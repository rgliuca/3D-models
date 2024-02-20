import cadquery as cq

def copy(obj):
    return obj.translate((0, 0, 0))

#intersection = sphere.intersect(box)  # doesn't work

def intersect(wp1, wp2):
    """
    Return geometric intersection between 2 cadquery.Workplane instances by
    exploiting.
    A n B = (A u B) - ((A - B) u (B - A))
    """
    neg1 = copy(wp1).cut(wp2)
    neg2 = copy(wp2).cut(wp1)
    negative = neg1.union(neg2)
    return copy(wp1).union(wp2).cut(negative)

plate_height = 4
plate_width = 58
plate_length = 76 

m1 = 30

hook_width = 25

t1 = 30
t2 = 20

b1 = 5
b2 = 8

parts = []

'''
wall_plate = cq.Workplane("XY").\
    center(0, 0).box(plate_width, plate_length, plate_height)
'''

pts = [
    (0, 0),
    (plate_height, 0),
    (plate_height, plate_length),
    (0, plate_length)
    ]

wall_plate = cq.Workplane("XY").\
    center(0, 0).\
    polyline(pts).close().extrude(plate_width).\
    fillet(1)


parts.append(wall_plate)

pts = [
    (0, 0),
    (t2, 0),
    (0, t1)
    ]

hook = cq.Workplane("XY").\
    workplane(offset = (plate_width - hook_width) / 2).\
    center(0, m1).\
    polyline(pts).close().extrude(hook_width).\
    edges("|Z").fillet(1)

pts = [
    (0, 0),
    (b2, 0),
    (b2, b1),
    (0, b1)
    ]

hook = hook.polyline(pts).close().cutThruAll()
    
parts.append(hook)

result = cq.Workplane("XY")

for each_part in parts:
    result = result.union(each_part)

cq.exporters.export(result,'wall_hook.stl')

exit()

