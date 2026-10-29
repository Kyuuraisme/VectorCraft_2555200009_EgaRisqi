import pygame
import sys
import math
import numpy as np

# Impor Komponen Logika & UI Terpisah
from Ui.Canvas import CanvasView
from Ui.Toolbar import ToolbarView
from Ui.Inspector import InspectorView
from Engine.Matrix3x3 import Matrix3x3

# Overwrite helper wrapper agar modul rasterizer memiliki fungsi pemanggil dinamis
from Engine import Rasterizer
Rasterizer.Rasterizer.draw_line = lambda arr, x1, y1, x2, y2, col, algo, w, h: \
    Rasterizer.Rasterizer.draw_line_dda(arr, x1, y1, x2, y2, col, w, h) if algo == "DDA" else \
    Rasterizer.Rasterizer.draw_line_bresenham(arr, x1, y1, x2, y2, col, w, h)

# Representasi Struktur Objek Selaras 
from Ui.Canvas import CurveEngine
class VectorShape:
    def __init__(self, type_str):
        self.type = type_str
        self.points = []
        self.pivot = None
    def get_pivot(self):
        if self.pivot is not None:
            return tuple(self.pivot)
        bbox = self.get_bounding_box()
        return ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
    def set_pivot(self, x, y):
        self.pivot = [float(x), float(y)]
    def reset_pivot(self):
        self.pivot = None
    def get_bounding_box(self):
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        return [min(xs), min(ys), max(xs), max(ys)]
    def apply_transform(self, matrix):
        for i in range(len(self.points)):
            nx, ny = Matrix3x3.transform_point(matrix, self.points[i][0], self.points[i][1])
            self.points[i] = [nx, ny]
        if self.pivot is not None:
            px, py = Matrix3x3.transform_point(matrix, self.pivot[0], self.pivot[1])
            self.pivot = [px, py]
    def is_hit(self, px, py, threshold=8):
        for p in self.points:
            if math.hypot(p[0] - px, p[1] - py) <= threshold: return True
        bbox = self.get_bounding_box()
        return bbox[0] <= px <= bbox[2] and bbox[1] <= py <= bbox[3]

class AppStateManager:
    """Mengelola state internal sistem secara terpusat (Model-Controller Context)"""
    def __init__(self):
        self.artboard = [250, 100, 850, 550] # [x1, y1, x2, y2]
        self.tool = "SELECT"
        self.algo = "Bresenham"
        self.preview_outside = True
        self.objects = []
        self.selected_obj = None
        self.drawing = False
        self.drag_mode = None
        self.drag_start = (0, 0)
        self.active_handle_idx = -1
        self.temp_points = []
        self.scale_anchor = (0, 0)
        self.rotation_angle_start = 0.0
        self.polygon_points = []

class VectorCraftApp:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1024, 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("VectorCraft 2D Studio - OOP Framework")
        self.clock = pygame.time.Clock()
        
        # Inisialisasi Model & UI Layer
        self.state = AppStateManager()
        font = pygame.font.SysFont("Segoe UI", 13)
        font_bold = pygame.font.SysFont("Segoe UI", 15, bold=True)
        
        self.canvas_view = CanvasView(self.state)
        self.toolbar_view = ToolbarView(font, font_bold)
        self.inspector_view = InspectorView(font)

    def run(self):
        while True:
            self.handle_events()
            # Render Base Canvas
            self.screen.fill((30, 30, 30))
            
            # Panggil sub-tampilan komponen
            self.canvas_view.render(self.screen, self.width, self.height)
            toolbar_bottom = self.toolbar_view.draw_sidebar(self.screen, self.state)
            inspector_y = min(toolbar_bottom + 15, 650)
            self.inspector_view.draw_status(self.screen, self.state, y_pos=inspector_y)
            
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v: self.state.tool = "SELECT"
                elif event.key == pygame.K_l: self.state.tool = "LINE"
                elif event.key == pygame.K_c: self.state.tool = "CIRCLE"
                elif event.key == pygame.K_p: self.state.tool = "BEZIER"
                elif event.key == pygame.K_g:
                    self.state.tool = "POLYGON"
                    self.state.polygon_points = []
                    self.state.drawing = False
                elif event.key == pygame.K_b: self.state.algo = "Bresenham"
                elif event.key == pygame.K_d: self.state.algo = "DDA"
                elif event.key == pygame.K_o: self.state.preview_outside = not self.state.preview_outside
                elif (event.key in [pygame.K_DELETE, pygame.K_BACKSPACE]
                      and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_META)):
                    self.state.objects = []
                    self.state.selected_obj = None
                    self.state.drawing = False
                    self.state.temp_points = []
                    self.state.polygon_points = []
                    self.state.drag_mode = None
                    self.state.tool = "SELECT"
                elif event.key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
                    if self.state.selected_obj:
                        if self.state.selected_obj in self.state.objects:
                            self.state.objects.remove(self.state.selected_obj)
                        self.state.selected_obj = None
                elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.state.objects = []
                    self.state.selected_obj = None
                    self.state.drawing = False
                    self.state.temp_points = []
                    self.state.polygon_points = []
                    self.state.drag_mode = None
                    self.state.tool = "SELECT"
                elif event.key == pygame.K_RETURN and self.state.tool == "POLYGON" and len(self.state.polygon_points) >= 3:
                    nob = VectorShape("POLYGON")
                    nob.points = [list(p) for p in self.state.polygon_points]
                    self.state.objects.append(nob)
                    self.state.selected_obj = nob
                    self.state.polygon_points = []
                    self.state.tool = "SELECT"
                elif event.key == pygame.K_ESCAPE:
                    self.state.polygon_points = []
                    self.state.temp_points = []
                    self.state.drawing = False
                    self.state.drag_mode = None
                    self.state.tool = "SELECT"

                elif self.state.selected_obj and self.state.tool in ["SELECT", "LINE"]:
                    px, py = self.state.selected_obj.get_pivot()
                    step = 10 if pygame.key.get_mods() & pygame.KMOD_SHIFT else 1
                    if event.key == pygame.K_LEFT:
                        self.state.selected_obj.apply_transform(Matrix3x3.translation(-step, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.state.selected_obj.apply_transform(Matrix3x3.translation(step, 0))
                    elif event.key == pygame.K_UP:
                        self.state.selected_obj.apply_transform(Matrix3x3.translation(0, -step))
                    elif event.key == pygame.K_DOWN:
                        self.state.selected_obj.apply_transform(Matrix3x3.translation(0, step))
                    elif event.key == pygame.K_r:
                        net = Matrix3x3.pivot_transform(Matrix3x3.rotation(math.radians(15)), px, py)
                        self.state.selected_obj.apply_transform(net)
                    elif event.key == pygame.K_q:
                        net = Matrix3x3.pivot_transform(Matrix3x3.rotation(math.radians(-15)), px, py)
                        self.state.selected_obj.apply_transform(net)
                    elif event.key == pygame.K_s:
                        net = Matrix3x3.pivot_transform(Matrix3x3.shear(0.1, 0.0), px, py)
                        self.state.selected_obj.apply_transform(net)
                    elif event.key == pygame.K_t:
                        net = Matrix3x3.pivot_transform(Matrix3x3.shear(0.0, 0.1), px, py)
                        self.state.selected_obj.apply_transform(net)
                    elif event.key == pygame.K_h:
                        self.state.selected_obj.apply_transform(Matrix3x3.pivot_transform(Matrix3x3.reflection(True, False), px, py))
                    elif event.key == pygame.K_j:
                        self.state.selected_obj.apply_transform(Matrix3x3.pivot_transform(Matrix3x3.reflection(False, True), px, py))
                    elif event.key == pygame.K_f:
                        self.state.selected_obj.reset_pivot()
                    elif event.key == pygame.K_LEFTBRACKET:
                        self.state.selected_obj.apply_transform(Matrix3x3.pivot_transform(Matrix3x3.scaling(0.9, 0.9), px, py))
                    elif event.key == pygame.K_RIGHTBRACKET:
                        self.state.selected_obj.apply_transform(Matrix3x3.pivot_transform(Matrix3x3.scaling(1.1, 1.1), px, py))

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 1. Deteksi Handle Artboard Resize
                if math.hypot(mx - self.state.artboard[2], my - self.state.artboard[3]) <= 12:
                    self.state.drag_mode = "RESIZE_ARTBOARD"
                    continue

                # Gizmo khusus untuk garis terpilih saat tool LINE aktif
                if self.state.tool == "LINE" and not self.state.drawing and self.state.selected_obj and self.state.selected_obj.type == "LINE":
                    px, py = self.state.selected_obj.get_pivot()
                    if math.hypot(mx - px, my - py) <= 10:
                        self.state.drag_mode = "MOVE_PIVOT"
                        continue
                    rx, ry = px, py - 55
                    if math.hypot(mx - rx, my - ry) <= 10:
                        self.state.drag_mode = "ROTATE_OBJ"
                        self.state.rotation_angle_start = math.atan2(my - py, mx - px)
                        continue
                    bbox = self.state.selected_obj.get_bounding_box()
                    if math.hypot(mx - bbox[2], my - bbox[3]) <= 10:
                        self.state.drag_mode = "SCALE_OBJ"
                        self.state.drag_start = (mx, my)
                        self.state.scale_anchor = (px, py)
                        continue
                    hit_line_handle = False
                    for idx, point in enumerate(self.state.selected_obj.points):
                        if math.hypot(mx - point[0], my - point[1]) <= 10:
                            self.state.drag_mode = "DRAG_HANDLE"
                            self.state.active_handle_idx = idx
                            hit_line_handle = True
                            break
                    if hit_line_handle:
                        continue
                
                # 2. Mode Seleksi Objek & Gizmo Handle
                if self.state.tool == "SELECT":
                    if self.state.selected_obj:
                        px, py = self.state.selected_obj.get_pivot()
                        if math.hypot(mx - px, my - py) <= 10:
                            self.state.drag_mode = "MOVE_PIVOT"
                            continue
                        rx, ry = px, py - 55
                        if math.hypot(mx - rx, my - ry) <= 10:
                            self.state.drag_mode = "ROTATE_OBJ"
                            self.state.rotation_angle_start = math.atan2(my - py, mx - px)
                            continue
                        bbox = self.state.selected_obj.get_bounding_box()
                        if math.hypot(mx - bbox[2], my - bbox[3]) <= 8:
                            self.state.drag_mode = "SCALE_OBJ"
                            self.state.drag_start = (mx, my)
                            self.state.scale_anchor = (px, py)
                            continue
                        
                        if self.state.selected_obj.type == "BEZIER":
                            hit_h = False
                            for idx, p in enumerate(self.state.selected_obj.points):
                                if math.hypot(mx - p[0], my - p[1]) <= 8:
                                    self.state.drag_mode = "DRAG_HANDLE"
                                    self.state.active_handle_idx = idx
                                    hit_h = True; break
                            if hit_h: continue

                    hit_any = False
                    for obj in reversed(self.state.objects):
                        if obj.is_hit(mx, my):
                            self.state.selected_obj = obj
                            self.state.drag_mode = "MOVE_OBJ"
                            self.state.drag_start = (mx, my)
                            hit_any = True; break
                    if not hit_any: self.state.selected_obj = None

                # 3. Mode Mulai Menggambar
                elif self.state.tool == "LINE":
                    if not self.state.drawing:
                        self.state.drawing = True
                        self.state.temp_points = [[mx, my], [mx, my]]
                    else:
                        end_point = [mx, my]
                        if math.hypot(end_point[0] - self.state.temp_points[0][0], end_point[1] - self.state.temp_points[0][1]) > 4:
                            nob = VectorShape("LINE")
                            nob.points = [list(self.state.temp_points[0]), end_point]
                            self.state.objects.append(nob)
                            self.state.selected_obj = nob
                            self.state.temp_points = []
                        self.state.drawing = False
                        # Tetap berada di mode LINE untuk membuat garis berikutnya.
                        self.state.tool = "LINE"
                elif self.state.tool == "CIRCLE":
                    self.state.drawing = True
                    self.state.temp_points = [[mx, my], [mx, my]]
                elif self.state.tool == "BEZIER":
                    if not self.state.drawing:
                        self.state.drawing = True
                        self.state.temp_points = [[mx, my], [mx+40, my-60], [mx+80, my-60], [mx+120, my]]
                    else:
                        nob = VectorShape("BEZIER")
                        nob.points = [list(p) for p in self.state.temp_points]
                        self.state.objects.append(nob)
                        self.state.drawing = False
                        self.state.selected_obj = nob
                        self.state.tool = "SELECT"
                elif self.state.tool == "POLYGON":
                    if len(self.state.polygon_points) < 2 or math.hypot(mx - self.state.polygon_points[-1][0], my - self.state.polygon_points[-1][1]) > 4:
                        self.state.polygon_points.append([mx, my])
                        self.state.drawing = True
                        self.state.temp_points = self.state.polygon_points

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.state.drawing and self.state.tool == "CIRCLE":
                    nob = VectorShape(self.state.tool)
                    nob.points = [list(p) for p in self.state.temp_points]
                    self.state.objects.append(nob)
                    self.state.selected_obj = nob
                    self.state.drawing = False
                    self.state.tool = "SELECT"
                self.state.drag_mode = None

            elif event.type == pygame.MOUSEMOTION:
                if self.state.drag_mode == "RESIZE_ARTBOARD":
                    self.state.artboard[2] = max(self.state.artboard[0] + 150, mx)
                    self.state.artboard[3] = max(self.state.artboard[1] + 150, my)
                
                elif self.state.drag_mode == "MOVE_OBJ" and self.state.selected_obj:
                    dx, dy = mx - self.state.drag_start[0], my - self.state.drag_start[1]
                    mat = Matrix3x3.translation(dx, dy)
                    self.state.selected_obj.apply_transform(mat)
                    self.state.drag_start = (mx, my)

                elif self.state.drag_mode == "MOVE_PIVOT" and self.state.selected_obj:
                    self.state.selected_obj.set_pivot(mx, my)

                elif self.state.drag_mode == "ROTATE_OBJ" and self.state.selected_obj:
                    px, py = self.state.selected_obj.get_pivot()
                    angle = math.atan2(my - py, mx - px)
                    delta = angle - self.state.rotation_angle_start
                    if abs(delta) > 0.0001:
                        net = Matrix3x3.pivot_transform(Matrix3x3.rotation(delta), px, py)
                        self.state.selected_obj.apply_transform(net)
                    self.state.rotation_angle_start = angle
                    
                elif self.state.drag_mode == "DRAG_HANDLE" and self.state.selected_obj:
                    self.state.selected_obj.points[self.state.active_handle_idx] = [mx, my]
                    
                elif self.state.drag_mode == "SCALE_OBJ" and self.state.selected_obj:
                    px, py = self.state.scale_anchor
                    old_x, old_y = self.state.drag_start
                    sx = max(0.1, abs(mx - px) / max(1.0, abs(old_x - px)))
                    sy = max(0.1, abs(my - py) / max(1.0, abs(old_y - py)))
                    net_matrix = Matrix3x3.pivot_transform(Matrix3x3.scaling(sx, sy), px, py)
                    self.state.selected_obj.apply_transform(net_matrix)
                    self.state.drag_start = (mx, my)

                elif self.state.drawing and self.state.tool in ["LINE", "CIRCLE"]:
                    self.state.temp_points[1] = [mx, my]

                elif self.state.drawing and self.state.tool == "BEZIER":
                    dx = mx - self.state.temp_points[0][0]
                    dy = my - self.state.temp_points[0][1]
                    self.state.temp_points[1] = [self.state.temp_points[0][0] + dx * 0.3, self.state.temp_points[0][1] + dy]
                    self.state.temp_points[2] = [self.state.temp_points[0][0] + dx * 0.7, self.state.temp_points[0][1]]
                    self.state.temp_points[3] = [mx, my]

# --- MAIN ENTRY POINT ---
if __name__ == "__main__":
    app = VectorCraftApp()
    app.run()