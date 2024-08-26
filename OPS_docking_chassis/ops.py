from common import ChassisType, ChassisBuilder

box = ChassisBuilder(ChassisType.TOP_ONLY)

box.width = 140
box.length = 200
box.height = 80

box.holes = (
    (30, 189, 3),
    (110, 189, 3),
    (15, 70, 5),
    (125, 70, 5),
    (70, 20, 5)
)

box.posts = (
    (15, 70, 8, 15, 4, 5),
    (125, 70, 8, 15, 4, 5),
    (70, 20, 8, 15, 4, 5)
)

model = box.build_sketch()

model = box.extrude()
