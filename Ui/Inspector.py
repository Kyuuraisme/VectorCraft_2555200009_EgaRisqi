import pygame

class InspectorView:
    def __init__(self, font):
        self.font = font

    def draw_status(self, screen, state, y_pos=300):
        # Menampilkan status koordinat objek terpilih atau informasi transformasi aktif
        y = y_pos
        max_width = 160

        def print_lbl(text):
            nonlocal y
            words = text.split(" ")
            lines = []
            current = ""
            for word in words:
                candidate = word if not current else current + " " + word
                if self.font.size(candidate)[0] <= max_width:
                    current = candidate
                else:
                    if current:
                        lines.append(current)
                    current = word
            if current:
                lines.append(current)

            for line in lines:
                surf = self.font.render(line, True, (180, 180, 180))
                screen.blit(surf, (15, y))
                y += 20

        print_lbl("INSPEKTOR PROPERTI:")
        print_lbl(f"Preview Luar [O]: {'ON' if state.preview_outside else 'OFF'}")
        
        if state.selected_obj:
            bbox = state.selected_obj.get_bounding_box()
            print_lbl(f"Tipe: {state.selected_obj.type}")
            print_lbl(f"W: {int(bbox[2]-bbox[0])}px | H: {int(bbox[3]-bbox[1])}px")
            px, py = state.selected_obj.get_pivot()
            print_lbl(f"Pivot: {int(px)}, {int(py)}")
            print_lbl("Panah: Geser | Shift: 10px")
            print_lbl("R/Q: Rotasi +/-15° | S/T: Shear")
            if state.tool == "LINE":
                print_lbl("Titik biru: seret titik garis")
                print_lbl("Handle biru: rotasi | kuning: pivot")
            if state.selected_obj.type == "AIRPLANE":
                print_lbl("Vector pesawat: klik, rotasi, shear, skalakan")
            print_lbl("H/J: Flip X/Y | [/] Skalakan")
            print_lbl("F: Reset Pivot | Seret poros")
        else:
            print_lbl("Status: Tidak ada objek terpilih")
            print_lbl("Delete: hapus objek terpilih")
            print_lbl("Ctrl+Delete / Ctrl+R: reset semua")
            print_lbl("Esc: batalkan proses gambar")
