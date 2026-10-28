class Clipper:
    INSIDE = 0  # 0000
    LEFT = 1    # 0001
    RIGHT = 2   # 0010
    BOTTOM = 4  # 0100
    TOP = 8     # 1000

    @classmethod
    def _compute_outcode(cls, x, y, xmin, ymin, xmax, ymax):
        code = cls.INSIDE
        if x < xmin:
            code |= cls.LEFT
        elif x > xmax:
            code |= cls.RIGHT
        if y < ymin:
            code |= cls.BOTTOM
        elif y > ymax:
            code |= cls.TOP
        return code

    @classmethod
    def clip_line(cls, x1, y1, x2, y2, artboard_rect):
        """Memotong garis (x1,y1)-(x2,y2) berdasarkan batas artboard [xmin, ymin, xmax, ymax]"""
        xmin, ymin, xmax, ymax = artboard_rect
        code1 = cls._compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
        code2 = cls._compute_outcode(x2, y2, xmin, ymin, xmax, ymax)
        accept = False

        while True:
            if (code1 == 0) and (code2 == 0):
                accept = True
                break
            elif (code1 & code2) != 0:
                break
            else:
                x, y = 0.0, 0.0
                outcode_out = code1 if code1 != 0 else code2

                if outcode_out & cls.TOP:
                    x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1) if y2 != y1 else x1
                    y = ymax
                elif outcode_out & cls.BOTTOM:
                    x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1) if y2 != y1 else x1
                    y = ymin
                elif outcode_out & cls.RIGHT:
                    y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1) if x2 != x1 else y1
                    x = xmax
                elif outcode_out & cls.LEFT:
                    y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1) if x2 != x1 else y1
                    x = xmin

                if outcode_out == code1:
                    x1, y1 = x, y
                    code1 = cls._compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
                else:
                    x2, y2 = x, y
                    code2 = cls._compute_outcode(x2, y2, xmin, ymin, xmax, ymax)

        if accept:
            return x1, y1, x2, y2
        return None
