import math


class CohenSutherland:
    """
    Cohen–Sutherland clipping algorithm clips a line from P0 = (x0, y0) to P1 = (x1, y1) against a rectangle with
    diagonal from (xmin, ymin) to (xmax, ymax).
    Adapted from code at: http://en.wikipedia.org/wiki/Cohen%E2%80%93Sutherland
    """
    INSIDE = 0   # 0000
    LEFT = 1     # 0001
    RIGHT = 2    # 0010
    BOTTOM = 4   # 0100
    TOP = 8      # 1000

    def compute_outcode(self, x, y, xmin, xmax, ymin, ymax):
        # Compute the bit code for a point (x, y) using the clip
        # bounded diagonally by (xmin, ymin), and (xmax, ymax)
        # ASSUME THAT xmax, xmin, ymax and ymin are global constants

        code = self.INSIDE  # initialised as being inside of [[clip window]]
        if x < xmin:
            code |= self.LEFT  # to the left of clip window
        elif x > xmax:
            code |= self.RIGHT  # to the right of clip window
        if y < ymin:
            code |= self.BOTTOM  # below the clip window
        elif y > ymax:
            code |= self.TOP  # above the clip window

        return code

    def __call__(self, matrix, resolution):
        px = matrix[0]
        py = matrix[1]
        centroidx = matrix[2]
        centroidy = matrix[3]
        p1x = matrix[4]
        p1y = matrix[5]

        # args: centroidx, centroidy, resolution, px, py, p1x, p1y
        # determine coordinates of grid cell
        xmin = centroidx - resolution / 2
        xmax = centroidx + resolution / 2
        ymin = centroidy - resolution / 2
        ymax = centroidy + resolution / 2

        # compute outcodes for P0, P1, and whatever point lies outside the clip rectangle
        outcode0 = self.compute_outcode(px, py, xmin, xmax, ymin, ymax)
        outcode1 = self.compute_outcode(p1x, p1y, xmin, xmax, ymin, ymax)
        accept = False
        intersection = 0

        while True:
            if (outcode0 / outcode1) == 0:
                # Bitwise OR is 0: both points inside window; trivially accept and exit loop
                accept = True
                break
            elif outcode0 & outcode1:
                # Bitwise AND is not 0: both points share an outside zone (LEFT, RIGHT, TOP
                # or BOTTOM), so both must be outside window; exit loop (accept is false)
                break
            else:
                # failed both tests, so calculate the line segment to clip
                # from an outside point to an intersection with clip edge
                x, y = 0, 0

                # at least one endpoint is outside the clip rectangle; pick it.
                outcodeout = outcode1 if outcode1 > outcode0 else outcode0

                # Now find the intersection point;
                # use formulas:
                #   slope = (y1 - y0) / (x1 - x0)
                #   x = x0 + (1 / slope) * (ym - y0), where ym is ymin or ymax
                # 	y = y0 + slope * (xm - x0), where xm is xmin or xmax
                # No need to worry about divide-by-zero because, in each case, the
                # outcode bit being tested guarantees the denominator is non-zero
                if outcodeout & self.TOP:
                    # point is above the clip window
                    x = px + (p1x - px) * (ymax - py) / (p1y - py)
                    y = ymax
                elif outcodeout & self.BOTTOM:
                    # point is below the clip window
                    x = px + (p1x - px) * (ymin - py) / (p1y - py)
                    y = ymin
                elif outcodeout & self.RIGHT:
                    # point is to the right of clip rectangle
                    y = py + (p1y - py) * (xmax - px) / (p1x - px)
                    x = xmax
                elif outcodeout & self.LEFT:
                    # point is to the left of clip rectangle
                    y = py + (p1y - py) * (xmin - px) / (p1x - px)
                    x = xmin

                # Now we move outside point to intersection point to clip
                # and get ready for next pass.
                if outcodeout == outcode0:
                    px = x
                    py = y
                    outcode0 = self.compute_outcode(px, py, xmin, xmax, ymin, ymax)
                else:
                    p1x = x
                    p1y = y
                    outcode1 = self.compute_outcode(p1x, p1y, xmin, xmax, ymin, ymax)

        if accept:
            intersection = math.sqrt(math.pow((p1x - px), 2) + math.pow((p1y - py), 2))
        return intersection
