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

stl_file = "ops_chassis_bottom.stl"
plate_height = 4
plate_width = 140
plate_length = 200

parts = []

pts = [
    (0, 0),
    (plate_width, 0),
    (plate_width, plate_length),
    (0, plate_length)
]

holes = [
    ((30, 189), 3),
    ((110, 189), 3),
    ((15, 70), 5),
    ((125, 70), 5),
    ((70, 20), 10)
]

base_plate = (cq.Workplane("XY")
    .center(0, 0)
    .polyline(pts).close().extrude(plate_height)
    .fillet(1)
    .faces(">Z")
    .workplane()
)

for each_hole in holes:
    pos = each_hole[0]
    dia = each_hole[1]
    base_plate = base_plate.moveTo(pos[0], pos[1]).hole(dia)


parts.append(base_plate)

result = cq.Workplane("XY")

for each_part in parts:
    result = result.union(each_part)

cq.exporters.export(result, stl_file)

show_object(result)
