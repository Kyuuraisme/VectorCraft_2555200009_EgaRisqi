import pygame
import math
from Engine.Rasterizer import Rasterizer
from Engine.Clipper import Clipper
from Engine.Curves import CurveEngine

class CanvasView:
    def __init__(self, app_state):
        self.state = app_state # Mengambil referensi dari Main Context

    def render(self, screen, width, height):
        # 1. Menggambar Latar Artboard dasar
        ab = self.state.artboard
        ab_w, ab_h = ab[2] - ab[0], ab[3] - ab[1]
        pygame.draw.rect(screen, (255, 255, 255), (ab[0], ab[1], ab_w, ab_h))
        
        # 2. Pemrosesan Pixel Array / Buffer secara Mandiri
        px_array = pygame.PixelArray(screen)
        
        # Gambar Semua Objek Terdaftar
        for obj in self.state.objects:
            self._draw_object(px_array, obj, width, height)
            
        # Gambar Objek Sementara Saat Ditarik Kursor Mouse
        if self.state.drawing and self.state.temp_points:
            # MEMPERBAIKI EROR: Membuat objek tiruan anonim (Muck Object) tanpa import eksternal
            class DummyShape:
                def __init__(self, type_str, points):
                    self.type = type_str
                    self.points = points
            
            dummy = DummyShape(self.state.tool, self.state.temp_points)
            self._draw_object(px_array, dummy, width, height, force_color=(0, 180, 0))

        del px_array # Selalu bebaskan array lock
        
        # 3. Menggambar UI Transform Gizmo & Batas Batas Artboard di atas pixel layer
        self._render_gizmos(screen)


    def _draw_object(self, px_array, obj, scr_w, scr_h, force_color=None):
        color = force_color if force_color else (0, 0, 0)
        color_outside = (210, 210, 210)
        algo = self.state.algo

        if obj.type == "LINE":
            p0, p1 = obj.points[0], obj.points[1]
            clipped = Clipper.clip_line(p0[0], p0[1], p1[0], p1[1], self.state.artboard)
            if self.state.preview_outside and not force_color:
                Rasterizer.draw_line(px_array, p0[0], p0[1], p1[0], p1[1], color_outside, algo, scr_w, scr_h)
            if clipped:
                Rasterizer.draw_line(px_array, clipped[0], clipped[1], clipped[2], clipped[3], color, algo, scr_w, scr_h)

        elif obj.type == "CIRCLE":
            xc, yc = obj.points[0][0], obj.points[0][1]
            r = math.hypot(obj.points[1][0] - xc, obj.points[1][1] - yc)
            # Karena lingkaran berbasis simetri oktan, area luar diabaikan lewat pembatas set_pixel internal.
            Rasterizer.draw_circle_midpoint(px_array, xc, yc, r, color, scr_w, scr_h)

        elif obj.type == "BEZIER":
            if self.state.preview_outside and not force_color:
                CurveEngine.draw_bezier(px_array, obj.points[0], obj.points[1], obj.points[2], obj.points[3], color_outside, algo, scr_w, scr_h)
            CurveEngine.draw_bezier(px_array, obj.points[0], obj.points[1], obj.points[2], obj.points[3], color, algo, scr_w, scr_h)

        elif obj.type in ["POLYGON", "AIRPLANE"] and len(obj.points) >= 2:
            segment_count = len(obj.points) if not force_color else len(obj.points) - 1
            for i in range(segment_count):
                p0 = obj.points[i]
                p1 = obj.points[(i + 1) % len(obj.points)]
                Rasterizer.draw_line(px_array, p0[0], p0[1], p1[0], p1[1], color, algo, scr_w, scr_h)

    def _render_gizmos(self, screen):
        # Frame Artboard
        ab = self.state.artboard
        pygame.draw.rect(screen, (0, 120, 215), (ab[0], ab[1], ab[2]-ab[0], ab[3]-ab[1]), 2)
        pygame.draw.circle(screen, (0, 120, 215), (int(ab[2]), int(ab[3])), 6) # Artboard Resizer
        
        # Titik dan garis sementara saat membuat poligon
        if self.state.tool == "POLYGON" and self.state.polygon_points:
            points = [(int(p[0]), int(p[1])) for p in self.state.polygon_points]
            for index in range(1, len(points)):
                pygame.draw.line(screen, (0, 180, 0), points[index - 1], points[index], 2)
            for point in points:
                pygame.draw.circle(screen, (255, 255, 255), point, 6)
                pygame.draw.circle(screen, (0, 180, 0), point, 6, 2)
                pygame.draw.circle(screen, (255, 50, 50), point, 2)
            if len(points) > 0:
                pygame.draw.line(screen, (100, 180, 100), points[-1], pygame.mouse.get_pos(), 1)

        # Preview pesawat saat Polygon Tool aktif
        if self.state.tool == "POLYGON" and not self.state.polygon_points:
            mx, my = pygame.mouse.get_pos()
            template = [
                (90, 0), (20, -18), (5, -55), (-10, -55),
                (0, -20), (-55, -15), (-75, -35), (-85, -35),
                (-75, -10), (-55, -5), (-55, 5), (-75, 10),
                (-85, 35), (-75, 35), (-55, 15), (0, 20),
                (-10, 55), (5, 55), (20, 18)
            ]
            preview_points = [(int(mx + x), int(my + y)) for x, y in template]
            for i, point in enumerate(preview_points):
                next_point = preview_points[(i + 1) % len(preview_points)]
                pygame.draw.line(screen, (90, 180, 90), point, next_point, 1)

        # Titik awal/akhir dan garis preview fitur LINE berbasis dua klik
        if self.state.tool == "LINE":
            if self.state.selected_obj and self.state.selected_obj.type == "LINE" and not self.state.drawing:
                for point in self.state.selected_obj.points:
                    point = (int(point[0]), int(point[1]))
                    pygame.draw.circle(screen, (255, 255, 255), point, 7)
                    pygame.draw.circle(screen, (0, 180, 215), point, 7, 2)
                    pygame.draw.circle(screen, (255, 50, 50), point, 2)
            if self.state.drawing and self.state.temp_points:
                start = (int(self.state.temp_points[0][0]), int(self.state.temp_points[0][1]))
                pygame.draw.circle(screen, (255, 255, 255), start, 7)
                pygame.draw.circle(screen, (255, 180, 0), start, 7, 2)
                pygame.draw.circle(screen, (255, 50, 50), start, 2)

        # Pen Tool mengikuti pola dua klik LINE, sambil mempertahankan 4 titik Bezier
        if self.state.tool == "BEZIER":
            if self.state.drawing and self.state.temp_points:
                start = (int(self.state.temp_points[0][0]), int(self.state.temp_points[0][1]))
                pygame.draw.circle(screen, (255, 255, 255), start, 7)
                pygame.draw.circle(screen, (255, 180, 0), start, 7, 2)
            elif self.state.selected_obj and self.state.selected_obj.type == "BEZIER":
                for point in self.state.selected_obj.points:
                    point = (int(point[0]), int(point[1]))
                    pygame.draw.circle(screen, (255, 255, 255), point, 7)
                    pygame.draw.circle(screen, (0, 180, 215), point, 7, 2)
                    pygame.draw.circle(screen, (255, 50, 50), point, 2)

        # Transform Gizmo Objek Aktif
        if self.state.tool in ["SELECT", "LINE", "BEZIER"] and self.state.selected_obj:
            bbox = self.state.selected_obj.get_bounding_box()
            pygame.draw.rect(screen, (255, 50, 50), (bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]), 1)
            pygame.draw.rect(screen, (0, 255, 0), (bbox[2]-4, bbox[3]-4, 8, 8)) # Scale Anchor

            px, py = self.state.selected_obj.get_pivot()
            pygame.draw.line(screen, (0, 120, 215), (int(px), int(py)), (int(px), int(py - 55)), 1)
            pygame.draw.circle(screen, (255, 180, 0), (int(px), int(py)), 7, 2)
            pygame.draw.circle(screen, (255, 255, 255), (int(px), int(py)), 2)
            pygame.draw.circle(screen, (0, 120, 215), (int(px), int(py - 55)), 8, 2)
            
            if self.state.selected_obj.type == "BEZIER":
                pts = self.state.selected_obj.points
                pygame.draw.line(screen, (150, 150, 150), pts[0], pts[1], 1)
                pygame.draw.line(screen, (150, 150, 150), pts[2], pts[3], 1)
                for p in pts:
                    pygame.draw.circle(screen, (255, 50, 50), (int(p[0]), int(p[1])), 4)
