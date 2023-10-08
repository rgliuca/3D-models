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

dist_hole_to_base_support = 46
dist_front_to_hole = 23
dist_hole_to_hole = 51
hole_dia = 6.6
hole_screw_dia = 2
hole_height = 3.5

cut_out_width = 25
cut_out_length = 58
dist_cut_out_to_hole = 18

base_length = 160
base_width = 72
base_thickness = 0.5

base_support_length = 3
base_support_width = 29
base_support_height = 3.5

base_support_dim_x = 29
base_support_dim_y = 83

parts = []

dist_base_support_offset = base_length / 2 - (dist_hole_to_base_support + dist_front_to_hole)

screw_mounts = cq.Workplane("XY").\
    center(-base_length / 2 + dist_front_to_hole, - (base_width - dist_hole_to_hole) / 2).circle(hole_dia / 2).\
    center(0, - dist_hole_to_hole).circle(hole_dia / 2).\
    extrude(hole_height).\
    faces(">Z").hole(hole_screw_dia)

parts.append(screw_mounts)

pts = [
    (0, 0),
    (0, cut_out_width),
    (cut_out_length, cut_out_width),
    (cut_out_length, 0)]

#    hole(hole_screw_dia).center(0, -dist_hole_to_hole).\
#    hole(hole_screw_dia).center(-dist_cut_out_to_hole, dist_hole_to_hole / 2 - cut_out_width / 2).\
base_plate = cq.Workplane("XZ").\
    center(0, -base_thickness/2).rect(base_length, base_thickness).\
    extrude(base_width).faces(">Z").workplane().\
    center(-base_length / 2 + dist_front_to_hole, -(base_width - dist_hole_to_hole) / 2).\
    hole(hole_screw_dia).center(0, -dist_hole_to_hole).\
    hole(hole_screw_dia).center(-dist_cut_out_to_hole, dist_hole_to_hole / 2 - cut_out_width / 2).\
    workplane().polyline(pts).close().cutThruAll()


parts.append(base_plate)

pts = [
        (0, 0),
        (0, base_support_height),
        (base_support_length, base_support_height),
        (base_support_length, 0)]

#    center(-dist_base_support_offset - base_support_length, base_support_height / 2).\
#    rect(base_support_length, base_support_height).extrude(base_support_dim_x).\
base_support = cq.Workplane("XZ").\
    workplane(offset = (base_width - base_support_width) / 2).\
    center(-dist_base_support_offset, 0).\
    polyline(pts).close().extrude(base_support_dim_x).\
    edges("|Y" and ">Z").fillet(0.75)

parts.append(base_support)

#    center(base_support_dim_y - base_support_length, 0).\
#    rect(base_support_length, base_support_height).extrude(base_support_dim_x)

pts = [
       (0, 0),
       (0, base_support_height + 3),
       (base_support_length + 4, base_support_height + 3),
       (base_support_length + 4, base_support_height)
       ]

#    center(base_support_dim_y / 2 - base_support_length - dist_base_support_offset, 0).\
base_clip = cq.Workplane("XZ").\
    workplane(offset = (base_width - base_support_width) / 2).\
    center(-dist_base_support_offset + base_support_dim_y - base_support_length, 0).\
    polyline(pts).\
    threePointArc((base_support_length + 1, base_support_height - 1), (base_support_length, 0)).\
    close().extrude(base_support_dim_x).\
    edges("|Y" and ">Z").fillet(1)

parts.append(base_clip)

result = cq.Workplane("XY")

for each_part in parts:
    result = result.union(each_part)

'''
partial = cq.Workplane("XZ").workplane(offset = 30).center(-30, -5).polyline([(0,0),(0, 100), (120, 100),(120, 0)]).close().extrude(10)

intersection = intersect(result, partial)
result = intersection
'''

cq.exporters.export(result,'jigsaw.sled.stl')
