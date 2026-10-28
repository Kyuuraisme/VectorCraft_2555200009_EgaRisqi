import pygame

class InspectorView:
    def __init__(self, font):
        self.font = font

    def draw_status(self, screen, state, y_pos=300):
        # Menampilkan status koordinat objek terpilih atau informasi transformasi aktif
        y = y_pos
        def print_lbl(text):
            nonlocal y
            surf = self.font.render(text, True, (180, 180, 180))
            screen.blit(surf, (15, y))
            y += 22

        print_lbl("INSPEKTOR PROPERTI:")
        print_lbl(f"Preview Luar [O]: {'ON' if state.preview_outside else 'OFF'}")
        
        if state.selected_obj:
            bbox = state.selected_obj.get_bounding_box()
            print_lbl(f"Tipe: {state.selected_obj.type}")
            print_lbl(f"W: {int(bbox[2]-bbox[0])}px | H: {int(bbox[3]-bbox[1])}px")
            print_lbl("[R] Putar +15° Pivot")
            print_lbl("[S] Shear Kanan (+0.1)")
        else:
            print_lbl("Status: Tidak ada objek")
