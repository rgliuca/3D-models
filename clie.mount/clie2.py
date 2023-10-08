import cadquery as cq
from math import *

# w is the 1/2 width of the mount base
w = 30 / 2

# h1 is the height of the straight support/mount leg
h1 = 8

# h2 is the slant lenght of the angled support/mount
h2 = 15

# th1 is the thickness of the support/mount
th1 = 2

# theta is the angle of the support slant
theta = 32

# base_width is the thickness of the base
base_width = 1.5

# mount_width is the height of the support/mount
mount_width = 30

parts = []

base_pts = [(0, 0), (w + th1, 0), (w + th1, h1),
        (w + th1 + h2 * sin(theta/360 * pi * 2), h1 + h2 * cos(theta/360 * pi * 2)),
        (w + th1 + h2 * sin(theta/360 * pi * 2) - th1 * cos(theta/360 * pi * 2),
            h1 + h2 * cos(theta/360 * pi * 2) + th1 * sin(theta/360 * pi *2)),
        (0, h1 + h2 * cos(theta/360 * pi * 2) + th1 * sin(theta/360 * pi *2)),
        (0, 0)
        ]

mirror_pts = []

for each_pt in base_pts:
    mirror_pts.append((each_pt[0] * -1, each_pt[1]))

left_mount_pts = [_ for _ in base_pts]
left_mount_pts.pop()
left_mount_pts.pop()
left_mount_pts.append((w, h1 + th1 * sin(theta/360 * pi * 2)))
left_mount_pts.append((w, 0))

right_mount_pts = [(_[0] * -1 , _[1]) for _ in left_mount_pts]

#mount = cq.Workplane("XY").polyline(pts).close().extrude(mount_width).faces("<Z[1]").fillet(1)
left_base = cq.Workplane("XY").polyline(base_pts).close().extrude(base_width)
right_base = cq.Workplane("XY").polyline(mirror_pts).close().extrude(base_width)
parts.append(left_base)
parts.append(right_base)

left_mount = cq.Workplane("XY").polyline(left_mount_pts).close().extrude(mount_width).edges().fillet(th1 / 2 - .001)
parts.append(left_mount)

right_mount = cq.Workplane("XY").polyline(right_mount_pts).close().extrude(mount_width).edges().fillet(th1 / 2 - .001)
parts.append(right_mount)

'''
edges = mount.edges().all()

for each_edge in edges:
    each_edge.fillet(1)
'''

result = cq.Workplane("XY")

for each_part in parts:
    result = result.union(each_part)

cq.exporters.export(result,'clie2_rack.stl')
