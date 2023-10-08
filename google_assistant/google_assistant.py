import math
import cadquery as cq

'''
width = 20
length = 60 
height = 2

d1 = 3.5
h1 = 2.6
d2 = 9.5
h2 = 6.3 - h1

result = (cq.Workplane("front").rect(width, length).center(0, length/2 - 8).rect(8, 3).extrude(height)
        .faces(">Z").workplane().center(0, -(length/2 - 8)*2).circle(d1/2).extrude(h1)
        .faces(">Z").workplane().circle(d2/2).extrude(h2))
'''

y1 = 5
y2 = 20
h1 = 70
w1 = 17
h2 = 3
w2 = 8
d1 = 5.4
th1 = 2

result = (cq.Workplane("front").rect(w1, h1)
        .center(0, h1/2 - y1).rect(w2, h2)
        .center(0, - y2 + y1).circle(d1/2)
        .extrude(th1)
        .edges("|Z").fillet(1.2)
        .edges("|X").fillet(0.9)
        )

e = cq.exporters.export
e(result, 'google_assistant_hook.stl')

