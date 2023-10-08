import cadquery as cq

mount_width = 15
mount_length = 25
mount_height = 3

hook_radius = 35 / 2

parts = []

pts = [(0, 0), (0, mount_length), (mount_height, mount_length), (mount_height, 0)]


#mount = cq.Workplane("XY").polyline(pts).close().extrude(mount_width).faces("<Z[1]").fillet(1)
mount = cq.Workplane("XY").polyline(pts).close().extrude(mount_width)
'''
edges = mount.edges().all()

for each_edge in edges:
    each_edge.fillet(1)
'''

#parts.append(edges)
parts.append(mount)

hook = cq.Workplane("XY").threePointArc((hook_radius, -hook_radius), (hook_radius * 2, 0)).\
    lineTo(hook_radius * 2 - mount_height, 0).\
    threePointArc((hook_radius, -hook_radius + mount_height), (mount_height, 0)).\
    close().extrude(mount_width).faces("|Z").fillet(1)
parts.append(hook)

result = cq.Workplane("XY")

for each_part in parts:
    result = result.union(each_part)

cq.exporters.export(result,'braun_hook.stl')
