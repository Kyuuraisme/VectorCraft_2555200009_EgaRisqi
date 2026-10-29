import pygame

class ToolbarView:
    def __init__(self, font, font_bold):
        self.font = font
        self.font_bold = font_bold

    def draw_sidebar(self, screen, state, y_start=20):
        pygame.draw.rect(screen, (45, 45, 48), (0, 0, 190, 768))
        pygame.draw.line(screen, (100, 100, 100), (190, 0), (190, 768), 2)
        
        y = y_start
        def render_txt(text, active=False, is_header=False):
            nonlocal y
            color = (0, 120, 215) if active else ((240,240,240) if not is_header else (150, 150, 150))
            f = self.font_bold if is_header or active else self.font
            surf = f.render(text, True, color)
            screen.blit(surf, (15, y))
            y += 25

        render_txt("VECTORCRAFT 2D", is_header=True)
        y += 10
        render_txt("ALAT KERJA [Key]:", is_header=True)
        render_txt("- [V] Select Tool", state.tool == "SELECT")
        render_txt("- [L] Line Tool", state.tool == "LINE")
        render_txt("- [C] Circle Tool", state.tool == "CIRCLE")
        render_txt("- [P] Pen/Bezier Tool", state.tool == "BEZIER")
        render_txt("- [G] Polygon Tool", state.tool == "POLYGON")
        y += 8
        render_txt("LINE TRANSFORM:", is_header=True)
        render_txt("R/Q Rotasi ±15°")
        render_txt("S/T Shear X/Y")
        render_txt("Seret titik/pivot/rotasi")
        y += 8
        render_txt("PENGHAPUSAN:", is_header=True)
        render_txt("Delete: Hapus objek terpilih")
        render_txt("Ctrl+Delete/Ctrl+R: Reset semua")
        render_txt("Esc: Batalkan gambar aktif")
        
        y += 15
        render_txt("ALGORITMA:", is_header=True)
        render_txt("- [B] Bresenham", state.algo == "Bresenham")
        render_txt("- [D] DDA", state.algo == "DDA")
        return y
