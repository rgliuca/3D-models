from enum import Enum, auto
from typing import Self

import cadquery as cq


class ChassisType(Enum):
    TOP_ONLY = auto()
    BOTTOM_ONLY = auto()
    BOTH = auto()


class PostType(Enum):
    SQUARE = auto()
    ROUND = auto()


class ChassisBuilder:
    WALL_THICKNESS = 2
    BASE_THICKNESS = 2
    MODEL_OFFSET_X = 10
    MODEL_OFFSET_Y = 0

    def __init__(self: Self, chassis_t) -> None:
        # x dim
        self._width = 0
        # y dim
        self._length = 0
        # z dim
        self._height = 0

        self._model_offset_x = ChassisBuilder.MODEL_OFFSET_X + self._width
        self._model_offset_y = ChassisBuilder.MODEL_OFFSET_Y
        self._base_thickness = ChassisBuilder.BASE_THICKNESS
        self._wall_thickness = ChassisBuilder.WALL_THICKNESS
        self._chassis_type = chassis_t
        self._top = None
        self._bottom = None

        '''
        If this property is still None at build phase, then it's assumed
        to be default: posts in all 4 corners of the chassis and always
        square & the width will be determined by the _mounting_post_dim
        If this list is empty (not None), then no posts are needed:
        (x_center_pos, y_center_pos, height) height is optional, if not
        specified, then it's assumed to be flush against the top cover
        '''
        self._mounting_posts = None

        '''
        Mounting post hole dimension is a tuple: (diameter, depth)
        '''
        self._mounting_post_dim = None

        '''
        Sanity check will be done at build phase if this value is 0
        This property will specify the diameter of the screw hole on the
        top cover.
        This property corresponds to the center location of the
        _mounting_posts list
        TODO: define countersink holes
        '''
        self._mount_screw_dia = 0

        '''
        list of tuples of posts (x_center_pos, y_center_pos, height, dia/
        width, screw_dia, depth) posts can be square or round with a
        mounting screw hole in the middle some sanity check is done to make
        sure the posts are within the box's width and len dim Initialzed as
        None, if not specified, then automatically assumed four corner will
        have square posts
        '''
        self._other_posts = None

        '''
        list of tuples of round holes for the top lid
        TODO: define countersink holes
        '''
        self._other_holes = None

    @property
    def width(self: Self) -> float:
        return self._width

    @width.setter
    def width(self: Self, value):
        self._width = value
        self._model_offset_x = ChassisBuilder.MODEL_OFFSET_X + self._width

    @property
    def length(self: Self) -> float:
        return self._length

    @length.setter
    def length(self: Self, value):
        self._length = value

    @property
    def height(self: Self) -> float:
        return self._height

    @height.setter
    def height(self: Self, value):
        self._height = value

    @property
    def base_thickness(self: Self) -> float:
        return self._base_thickness

    @base_thickness.setter
    def base_thickness(self: Self, value):
        self._base_thickness = value

    @property
    def wall_thickness(self: Self) -> float:
        return self._wall_thick_ness

    @wall_thickness.setter
    def wall_thickness(self: Self, value):
        self._wall_thickness = value

    @property
    def holes(self: Self) -> list:
        return self._other_holes

    @holes.setter
    def holes(self: Self, value: list) -> list:
        self._other_holes = value

    @property
    def posts(self: Self) -> list:
        return self._other_posts

    @posts.setter
    def posts(self: Self, value: list) -> list:
        self._other_posts = value

    # This method should input all the required parameters to get a model
    # setup
    def build_sketch(self: Self) -> cq.Workplane:
        '''
        - sanity check for the mounting posts: make sure the location is valid
        and the screw dia is within the bounds of the width and length

        -  sanity check for the other posts and other holes

        - sketch the cover and base
        - sketch the posts
        '''

        self._top = cq.Workplane("XY")
        self._bottom = cq.Workplane("XY")

        # build the top cover first
        if self._chassis_type is ChassisType.TOP_ONLY or ChassisType.BOTH:
            self._top.polyline((
                (0, 0),
                (self._width, 0),
                (self._width, self._length),
                (0, self._length)
            )).close()

        # build the bottom cover
        if self._chassis_type is ChassisType.BOTTOM_ONLY or ChassisType.BOTH:
            self._bottom.polyline((
                (self._model_offset_x, self._model_offset_y),
                (self._model_offset_x + self._width, self._model_offset_y),
                (self._model_offset_x + self._width, self._model_offset_y +
                    self._length),
                (self._model_offset_x, self._model_offset_y + self._length)
            )).close()

        if self._mounting_posts is not None:
            # anywhere there's a mounting post, will puch a hole on the
            # chassis
            for each_post in self._mounting_posts:
                ...

    def extrude(self: Self) -> cq.Workplane:
        '''
        - sanity check to make sure the mounting hole height, etc are not
        out of bounds
        '''
        # punch the holes on the top cover
        self._top = self._top.extrude(self._base_thickness).faces(">Z").\
            workplane()

        if self._other_holes is not None:
            for each_hole in self._other_holes:
                x = each_hole[0]
                y = each_hole[1]
                dia = each_hole[2]
                self._top = self._top.moveTo(x, y).hole(dia)

        self._bottom = self._bottom.extrude(self._base_thickness)

        # extrude other posts
        post_models = []
        if self._other_posts is not None:
            ox = self._model_offset_x
            oy = self._model_offset_y
            for ep in self._other_posts:
                post_models.append(
                    self._bottom.faces(">Z").workplane().
                    moveTo(ox + ep[0], oy + ep[1]).
                    circle(ep[2] / 2).extrude(ep[3]).faces(">Z").
                    workplane().moveTo(ox + ep[0], oy + ep[1]).
                    circle(ep[4] / 2).extrude(-ep[5], combine='cut')
                 )

        final_model = self._bottom.union(self._top)

        for pm in post_models:
            final_model = final_model.union(pm)

        return final_model
