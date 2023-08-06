# Copyright 2011-2019 Rob Gilton
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from . import pcons
from functools import singledispatch
from .pcons import Pad
import numpy as np
import sys

def mm(v, places=None):
    """Stringify the given value and suffix with mm

    Limit the number of decimal places to the number given
    if it is specified."""
    if places is None:
        return f"{v}mm"

    f = f"{{:.{places}f}}mm"
    return f.format(v)


def output_pad( x1, y1, x2, y2, thickness, clearance, mask, name, square, paste, f = sys.stdout, opposite_side = False ):
    flags = []
    if square:
        flags.append("square")
    if not paste:
        flags.append("nopaste")
    if opposite_side:
        flags.append("onsolder")

    print("\tPad[",
          *[mm(x, 6) for x in (x1,y1,x2,y2,
                               thickness*2, clearance*2,
                               mask+thickness*2)],
          f'"{name}"',
          f'"{name}"',
          f"\"{','.join(flags)}\"]",
          file=f)


@singledispatch
def render_item(obj, f=sys.stdout):
    raise TypeError("No renderer for object:", obj)


def render_square_pad( pad, f = sys.stdout ):
    "pcb doesn't support square pads - so hack it with two rectangles"
    d = pad.tr.x.val - pad.bl.x.val
    assert d == (pad.bl.y.val - pad.tl.y.val)

    thickness = d / 4

    p1 = ( ( pad.tl.x.val + thickness, pad.tl.y.val + thickness ),
           ( pad.tr.x.val - thickness, pad.tl.y.val + thickness ) )

    p2 = ( ( pad.bl.x.val + thickness, pad.bl.y.val - thickness ),
           ( pad.br.x.val - thickness, pad.bl.y.val - thickness ) )

    for p in (p1, p2):
        output_pad( p[0][0], p[0][1], p[1][0], p[1][1],
                    thickness = thickness,
                    clearance = pad.clearance,
                    mask = pad.mask_clearance,
                    name = pad.name,
                    square = pad.square,
                    paste = pad.paste,
                    f = f,
                    opposite_side = pad.opposite_side)


@render_item.register(pcons.Pad)
def _( pad, f = sys.stdout ):
    # Need to work out the longest dimension
    dims = ( pad.tr.x.val - pad.bl.x.val,
             pad.bl.y.val - pad.tl.y.val )

    if dims[0] > dims[1]:
        "Draw the pad in the x-direction"
        thickness = dims[1] / 2

        r1 = ( pad.bl.x.val + thickness,
               pad.bl.y.val - thickness )

        r2 = ( pad.br.x.val - thickness,
               pad.bl.y.val - thickness )

    elif dims[0] < dims[1]:
        "Draw the pad in the y-direction"
        thickness = dims[0] / 2

        r1 = ( pad.bl.x.val + thickness,
               pad.bl.y.val - thickness )

        r2 = ( pad.bl.x.val + thickness,
               pad.tr.y.val + thickness )
    else:
        render_square_pad(pad, f)
        return

    output_pad( r1[0], r1[1], r2[0], r2[1],
                thickness = thickness,
                clearance = pad.clearance,
                mask = pad.mask_clearance,
                name = pad.name,
                square = pad.square,
                paste = pad.paste,
                f = f,
                opposite_side = pad.opposite_side )


@render_item.register(pcons.Attribute)
def _(attr, f=sys.stdout):
    print(f'\tAttribute("{attr.name}" "{attr.value}")',
          file=f)


@render_item.register(pcons.CircularPad)
def _(pad, f=sys.stdout):
    output_pad( pad.centre.x.val, pad.centre.y.val,
                pad.centre.x.val, pad.centre.y.val,
                thickness = pad.diam/2,
                clearance = pad.clearance,
                mask = pad.mask_clearance,
                name = pad.name,
                square = False,
                paste = pad.paste,
                f = f,
                opposite_side = pad.opposite_side )


@render_item.register(pcons.Hole)
def _(hole, f=sys.stdout):
    print("\tPin[",
          *[mm(x) for x in (hole.pos.x.val,
                            hole.pos.y.val,
                            hole.diameter,
                            hole.clearance * 2,
                            hole.mask_clearance + hole.diameter,
                            hole.diameter + 0)],
          '""', '""',
          '"hole"]',
          file=f)


@render_item.register(pcons.Pin)
def _(pin, f=sys.stdout):
    print("\tPin[",
          *[mm(x) for x in (pin.centre.x.val,
                            pin.centre.y.val,
                            pin.pad_diameter,
                            pin.clearance * 2,
                            pin.mask_clearance + pin.pad_diameter,
                            pin.hole_diameter)],
          f'"{pin.name}"',
          f'"{pin.number}"',
          '"square"]' if pin.square else '""]',
          file=f)


@render_item.register(pcons.SilkLine)
def _(line, f=sys.stdout):
    print("\tElementLine[",
          *[mm(x) for x in (line.start.x.val,
                            line.start.y.val,
                            line.end.x.val,
                            line.end.y.val,
                            line.thickness)],
          "]", file=f)


@render_item.register(pcons.SilkCircle)
def render_silk_circle( c, f = sys.stdout ):
    print("\tElementArc[",
          *[mm(x) for x in (c.pos.x.val,
                            c.pos.y.val,
                            c.diameter/2,
                            c.diameter/2)],
          0,
          360,
          mm(c.thickness), "]",
          file=f)


@render_item.register(pcons.UnconstrainedPad)
def _(pad, stream):
    A = np.array([pad.tl.x.val, pad.tl.y.val])
    B = np.array([pad.tr.x.val, pad.tr.y.val])
    C = np.array([pad.br.x.val, pad.br.y.val])
    D = np.array([pad.bl.x.val, pad.bl.y.val])

    width = np.linalg.norm(D-A)
    length = np.linalg.norm(B-A)
    rects = []

    if width < length:
        rects.append([A,B,C,D])
    elif width > length:
        # The width needs to be smaller than the length
        # Rotate our perception of the pad by 90 degrees
        rects.append([B,C,D,A])
    else:
        # The pad is square.  PCB can't handle square pads,
        # so split it into two rectangular pads next to each other

        # Create two new points X and Y halfway along the edge of the pad
        X = A + (D-A)/2
        Y = B + (C-B)/2

        rects.append([A,B,Y,X])
        rects.append([X,Y,C,D])

    for A, B, C, D in rects:
        # Find unit vectors defining axes of the pad
        u = B-A
        u /= np.linalg.norm(u)

        v = D-A
        v /= np.linalg.norm(v)

        if np.dot(u,v) != 0:
            raise Exception("Only rectangular pads are supported at the moment")

        thickness = np.linalg.norm(D-A)/2

        start = A + u * thickness + v * thickness
        end = B - u * thickness + v * thickness

        output_pad( start[0], start[1],
                    end[0], end[1],
                    thickness=thickness,
                    clearance=pad.clearance,
                    mask=pad.mask_clearance,
                    name=pad.name,
                    square=pad.square,
                    paste=pad.paste,
                    f=stream )


@render_item.register(pcons.SilkRect)
def _(_, f=sys.stdout):
    "This has no rendererable elements"
    pass


def render( des, f = sys.stdout ):
    print(f'Element[0x00 "{des.desc}" "" "" 0 0 0 0 0 100 0x00000000]',
          file=f)
    print ("(", file=f)

    for obj in des.ents:
        if hasattr(obj, "render"):
            obj.render(f)
        else:
            render_item(obj, f)

    print (")", file=f)



