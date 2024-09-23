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
plate_height = 3
plate_width = 140
plate_length = 90

parts = []

pts = [
    (0, 8),
    (plate_width, 8),
    (plate_width, plate_length),
    (0, plate_length)
]

# format: ((x, y), height, post dia, hole dia, hole depth) 
posts = (
    ((5, 13), 30, 8, 2.9, 7),
    ((5, 72.5), 30, 8, 2.9, 7),
    ((135, 72.5), 30, 8, 2.9, 7),
    ((135, 13), 30, 8, 2.9, 7)
)

base_plate = (
    cq.Workplane("XY")
    .center(0, 0)
    .polyline(pts).close().extrude(plate_height)
    .fillet(0.5)
    .faces(">Z")
    .workplane()
)

for each_post in posts:
    pos = each_post[0]
    post_height = each_post[1]
    post_dia = each_post[2]
    base_plate = base_plate.moveTo(pos[0], pos[1]).circle(post_dia / 2).extrude(post_height)

base_plate = base_plate.faces(">Z").workplane()

for each_post in posts:
    pos = each_post[0]
    post_hole_dia = each_post[3]
    post_hole_depth = each_post[4]
    base_plate = base_plate.moveTo(pos[0], pos[1]).hole(post_hole_dia)

base_plate = base_plate.faces("<Z").workplane()

posts = posts[3:]

over_hang1 = []
over_hang2 = []

screw_post_cut_len = plate_height * 2 + post_height - 25

for each_post in posts:
    over_hang1.append(cq.Workplane("XY"))
    over_hang2.append(cq.Workplane("XY"))
    screw_head_radius = 5 / 2
    pos = each_post[0]
    post_height = each_post[1]
    post_hole_dia = each_post[3]
    post_hole_depth = each_post[4]
    base_plate = base_plate.moveTo(pos[0], -pos[1]).circle(screw_head_radius).cutBlind(-screw_post_cut_len)
    over_hang1[-1] = over_hang1[-1].moveTo(pos[0], pos[1]).sketch().circle(screw_head_radius).\
        rect(2 * screw_head_radius, post_hole_dia, mode='s').finalize().extrude(-0.16)
    over_hang2[-1] = over_hang2[-1].moveTo(pos[0], pos[1]).sketch().circle(screw_head_radius).\
        rect(post_hole_dia, post_hole_dia, mode='s').finalize().extrude(-0.16)

parts.append(base_plate)


bracket = (
    cq.Workplane("XY").
    polyline(((0, 80), (0, 77), (plate_width, 77), (plate_width, 80))).close().extrude(8 + plate_height).
    faces("<Y").workplane().moveTo(31.5, plate_height + 5).hole(3.5).
    moveTo(108.5, plate_height + 5).hole(3.5)
)

parts.append(bracket)

wings = (
    cq.Workplane("XY").workplane(8 + plate_height).
    polyline(((0, 80), (0, 77), (37, 77), (37, 80))).close().
    polyline(((103, 80), (103, 77), (plate_width, 77), (plate_width, 80))).close().
    extrude(8)
)

parts.append(wings)

result = cq.Workplane("XY")

for each_part in parts:
    result = result.union(each_part)

for each_oh in over_hang1:
    result = result.union(each_oh.translate((0, 0, screw_post_cut_len - 0.16))) 
for each_oh in over_hang2:
    result = result.union(each_oh.translate((0, 0, screw_post_cut_len))) 


# Let's cut a small piece and print it

#box = cq.Workplane("XY").rect(50, 50).extrude(50)

#result = result.intersect(box)

cq.exporters.export(result, stl_file)
