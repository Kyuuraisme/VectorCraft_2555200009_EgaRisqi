from Engine.Rasterizer import Rasterizer

class CurveEngine:
    @staticmethod
    def get_cubic_bezier_point(p0, p1, p2, p3, t):
        """Kalkulasi titik Kurva Bezier Kubik menggunakan Polinomial Bernstein."""
        mt = 1 - t
        w0 = mt ** 3
        w1 = 3 * (mt ** 2) * t
        w2 = 3 * mt * (t ** 2)
        w3 = t ** 3
        
        rx = w0 * p0[0] + w1 * p1[0] + w2 * p2[0] + w3 * p3[0]
        ry = w0 * p0[1] + w1 * p1[1] + w2 * p2[1] + w3 * p3[1]
        return rx, ry

    @staticmethod
    def draw_bezier(px_array, p0, p1, p2, p3, color, algo, scr_w, scr_h, segments=40):
        prev_x, prev_y = p0[0], p0[1]
        for i in range(1, segments + 1):
            t = i / segments
            cx, cy = CurveEngine.get_cubic_bezier_point(p0, p1, p2, p3, t)
            if algo == "DDA":
                Rasterizer.draw_line_dda(px_array, prev_x, prev_y, cx, cy, color, scr_w, scr_h)
            else:
                Rasterizer.draw_line_bresenham(px_array, prev_x, prev_y, cx, cy, color, scr_w, scr_h)
            prev_x, prev_y = cx, cy
