import cadquery as cq


def copy(obj):
    return obj.translate((0, 0, 0))

# intersection = sphere.intersect(box)  # doesn't work


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

holes = (
    ((30, 189), 3),
    ((110, 189), 3),
)

# format: ((x, y), height, hole dia, hole depth) 
posts = (
    ((15, 70), 6, 7, 3),
    ((125, 70), 6, 7, 3),
    ((70, 20), 6, 7, 2.5),
    ((6, 8), 20, 8, 2.5),
    ((6, 70), 20, 8, 2.5),
    ((134, 70), 20, 8, 2.5),
    ((134, 8), 20, 8, 2.5)
)

base_plate = (
    cq.Workplane("XY")
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

for each_post in posts:
    pos = each_post[0]
    post_height = each_post[1]
    post_hole_dia = each_post[2]
    post_hole_depth = each_post[3]
    base_plate = base_plate.moveTo(pos[0], pos[1]).circle(post_hole_dia / 2).extrude(post_height)

base_plate = base_plate.faces(">Z").workplane()

for each_post in posts:
    pos = each_post[0]
    post_height = each_post[1]
    post_hole_dia = each_post[2]
    post_hole_depth = each_post[3]
    base_plate = base_plate.moveTo(pos[0], pos[1]).hole(post_hole_dia / 2)

parts.append(base_plate)

bracket = (
    cq.Workplane("XY").
    polyline(((22, 80), (22, 77), (118, 77), (118, 80))).close().extrude(8 + plate_height).
    faces("<Y").workplane().moveTo(33, plate_height + 4).hole(3).
    moveTo(107, plate_height + 4).hole(3)
     
)

parts.append(bracket)

result = cq.Workplane("XY")

for each_part in parts:
    result = result.union(each_part)

cq.exporters.export(result, stl_file)

# show_object(result)
