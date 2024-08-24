from enum import Enum

import numbers

import cadquery as cq

class ChassisBuilder:
    class ChassisType(Enum):
        TOP_ONLY = auto()
        BOTTOM_ONLY = auto()
        BOTH = auto()

    class PostType(Enum):
        SQUARE = auto()
        ROUND = auto()

    def __init__(self: Self) -> None:
        # x dim
        self._width = 0
        # y dim
        self._length = 0
        # z dim
        self._height = 0

        '''
        If this property is still None at build phase, then it's assumed
        to be default: posts in all 4 corners of the chassis and always
        square the width will be determined by the _mounting_post_dim
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
    def _width(self: Self) -> numbers.Real:
        return self._width

    @property
    def _length(self: Self) -> numbers.Real:
        return self._length

    @property
    def _height(self: Self) -> numbers.Real:
        return self._height

    @property
    def _mounting_posts(self: Self) -> list:
        return self._mounting_posts

    @property
    def _mounting_post_dim(self: Self) -> list:
        return self._mounting_post_dim

    @property
    def _mount_screw_dia(self: Self) -> numbers.Real:
        return self._mount_screw_dia

    @property
    def _posts(self: Self) -> list:
        return self._posts

    @property
    def _holes(self: Self) -> list:
        return self._holes

    def build_sketch(self: Self) -> cq.Workplane:
        '''
        - sanity check for the mounting posts: make sure the location is valid
        and the screw dia is within the bounds of the width and length

        -  sanity check for the other posts and other holes

        - sketch the cover and base
        - sketch the posts
        '''

        ...

    def extrude(self: Self, box_height: number.Real) -> cq.Workplane:
        '''
        - sanity check to make sure the mounting hole height, etc are not
        out of bounds
        '''
        ...





