import numpy as np

class Rasterizer:
    @staticmethod
    def set_pixel(px_array, x, y, color, width, height):
        """Memastikan piksel berada di dalam dimensi layar sebelum di-plot."""
        if 0 <= x < width and 0 <= y < height:
            px_array[x, y] = color

    @staticmethod
    def draw_line_dda(px_array, x1, y1, x2, y2, color, scr_w, scr_h):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            Rasterizer.set_pixel(px_array, int(x1), int(y1), color, scr_w, scr_h)
            return
        x_inc = dx / steps
        y_inc = dy / steps
        x, y = x1, y1
        for _ in range(int(steps) + 1):
            Rasterizer.set_pixel(px_array, int(round(x)), int(round(y)), color, scr_w, scr_h)
            x += x_inc
            y += y_inc

    @staticmethod
    def draw_line_bresenham(px_array, x1, y1, x2, y2, color, scr_w, scr_h):
        x1, y1, x2, y2 = int(round(x1)), int(round(y1)), int(round(x2)), int(round(y2))
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while True:
            Rasterizer.set_pixel(px_array, x1, y1, color, scr_w, scr_h)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    @staticmethod
    def draw_circle_midpoint(px_array, xc, yc, r, color, scr_w, scr_h):
        xc, yc, r = int(round(xc)), int(round(yc)), int(round(r))
        if r < 0: return
        x = 0
        y = r
        d = 1 - r
        
        def plot_8_way(cx, cy, px, py):
            Rasterizer.set_pixel(px_array, cx + px, cy + py, color, scr_w, scr_h)
            Rasterizer.set_pixel(px_array, cx - px, cy + py, color, scr_w, scr_h)
            Rasterizer.set_pixel(px_array, cx + px, cy - py, color, scr_w, scr_h)
            Rasterizer.set_pixel(px_array, cx - px, cy - py, color, scr_w, scr_h)
            Rasterizer.set_pixel(px_array, cx + py, cy + px, color, scr_w, scr_h)
            Rasterizer.set_pixel(px_array, cx - py, cy + px, color, scr_w, scr_h)
            Rasterizer.set_pixel(px_array, cx + py, cy - px, color, scr_w, scr_h)
            Rasterizer.set_pixel(px_array, cx - py, cy - px, color, scr_w, scr_h)

        plot_8_way(xc, yc, x, y)
        while x < y:
            x += 1
            if d < 0:
                d += 2 * x + 1
            else:
                y -= 1
                d += 2 * (x - y) + 1
            plot_8_way(xc, yc, x, y)
