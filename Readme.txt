# VectorCraft 2D Studio

**VectorCraft 2D Studio** adalah aplikasi desktop grafis vektor interaktif yang dibangun menggunakan **Python 3.9+** dan **Pygame-ce / Pygame**. Aplikasi ini dirancang dengan prinsip *algorithmic graphics from-scratch*, di mana seluruh proses rasterisasi (penggambaran piksel), transformasi geometris, dan pemotongan garis (*clipping*) dihitung menggunakan formula matematika murni tanpa menggunakan fungsi gambar bawaan library grafis (*high-level drawing functions*).

---

##  Penjelasan Arsitektur & Struktur Proyek

Proyek ini menerapkan prinsip Berorientasi Objek (OOP) dengan pemisahan yang tegas antara lapisan logika matematis (*Engine*) dan lapisan antarmuka pengguna (*UI/View*).

```text
VectorCraft_2555200009_EgaRisqi/
├── Engine/                  # CORE LOGIKA MATEMATIS (MURNI)
│   ├── rasterizer.py        # Algoritma Rasterisasi Garis (DDA & Bresenham) & Lingkaran (Midpoint)
│   ├── matrix3x3.py         # Matriks Homogen 3x3 (Translasi, Rotasi Pivot, Skala, Shear)
│   ├── clipper.py           # Engine Pemotongan Garis Cohen-Sutherland
│   └── curves.py            # Kalkulasi Kurva Cubic Bezier & Polinomial Bernstein
├── Ui/                      # LAPISAN ANTARMUKA & VIEW COMPONENTS
│   ├── canvas.py            # Area Kerja Artboard & Pengelolahan Pixel Buffer (PixelArray)
│   ├── inspector.py         # Panel Samping untuk Menampilkan Informasi & Status Objek
│   └── toolbar.py           # Menu Pilihan Alat Kerja Aktif & Shortcut info
├── App.py                   # Titik Masuk Utama Aplikasi (Main Entry Point & State Controller)
├── requirements.txt         # Daftar Pustaka Dependensi Proyek
└── README.md                # Dokumentasi Panduan Penggunaan Aplikasi
```

### Detail Lapisan Engine:
1. **`rasterizer.py`**: Mengimplementasikan algoritma **DDA** dan **Bresenham** untuk menggambar garis di segala oktan kemiringan, serta **Midpoint Circle Algorithm** dengan simetri 8-arah untuk lingkaran presisi.
2. **`matrix3x3.py`**: Memanfaatkan `numpy` untuk operasi perkalian matriks linear koordinat homogen $3 \times 3$ guna memproses manipulasi objek secara presisi.
3. **`clipper.py`**: Menggunakan bitwise outcode berbasis algoritma **Cohen-Sutherland Line Clipping** untuk memotong garis yang melewati batas artboard secara *real-time*.
4. **`curves.py`**: Menghitung titik kurva halus berbasis formulasi **Bernstein Polynomials** untuk menghasilkan visualisasi kurva *Cubic Bézier*.

---

##  Panduan Tombol Pintas (Shortcut Keys)

Untuk berpindah mode kerja, pilih menu, atau melakukan manipulasi objek, gunakan tombol keyboard berikut:

###  Mode Alat Kerja (Tools)
*   **`V`** : **Select & Transform Tool** — Mode untuk memilih, menggeser, merotasi, dan mengubah skala objek.
*   **`L`** : **Line Tool** — Klik satu kali untuk titik awal, arahkan kursor untuk melihat preview, lalu klik lagi untuk membuat garis. Tool tetap aktif untuk membuat garis berikutnya. Titik awal dan akhir tetap terlihat sebagai handle biru-merah dan dapat diseret. Pada garis terpilih, R/Q memutar ±15°, S/T melakukan shear X/Y, serta pivot dan handle rotasi dapat diseret.
*   **`C`** : **Circle Tool** — Membuat lingkaran presisi berbasis radius dengan melakukan *drag* dari titik pusat.
*   **`P`** : **Pen / Bézier Tool** — Klik pertama menentukan titik awal, gerakkan kursor untuk melihat preview, lalu klik kedua menentukan titik akhir dan menyimpan kurva Bézier kubik. Tool tetap aktif untuk membuat kurva berikutnya.

###  Pengaturan Algoritma & Preview
*   **`B`** : Mengubah mesin perentalan garis ke **Algoritma Bresenham** (Default).
*   **`D`** : Mengubah mesin perentalan garis ke **Algoritma DDA**.
*   **`O`** : Mengaktifkan / menonaktifkan mode **Preview Outside** (Bagian garis di luar artboard digambar transparan/abu-abu).

###  Manipulasi Spasial (Saat Objek Terpilih dalam Mode `V`)
*   **`R`** : Memutar (*Rotate*) objek aktif sebesar **+15°** searah jarum jam secara homogen terhadap titik pusat objek (*Center Pivot*).
*   **`S`** : Memiringkan (*Shear*) objek aktif secara linear pada koordinat sumbu X sebesar **+0.1**.
*   **`DELETE` / `BACKSPACE`** : Menghapus objek vektor yang sedang terpilih dari lembar kerja.
*   **`Ctrl + DELETE` / `Ctrl + BACKSPACE` / `Ctrl + R`** : Menghapus dan mereset seluruh objek dari kanvas.
*   **`ESC`** : Membatalkan gambar garis atau poligon yang sedang aktif.
*   **`G`** : Mode Polygon/Pesawat; arahkan kursor lalu klik sekali untuk memunculkan siluet vector pesawat. Pesawat dapat dipilih dan diputar, di-shear, serta diskalakan dengan gizmo dan shortcut transformasi.
*   **`Panah` / `Shift+Panah`** : Menggeser objek 1 px / 10 px.
*   **`R` / `Q`** : Rotasi objek terhadap pivot sebesar +15° / -15°.
*   **`S` / `T`** : Shear pada sumbu X / Y sebesar +0.1.
*   **`H` / `J`** : Flip/refleksi horizontal / vertikal terhadap pivot.
*   **`[` / `]`** : Perbesar/kurangi skala objek 10% terhadap pivot.
*   **`F`** : Mengembalikan pivot ke pusat bounding box objek.

---

## Penjelasan Implementasi Fitur Utama

### Alur State dan Kontrol Aplikasi

`App.py` bertindak sebagai pengatur alur utama aplikasi. State aplikasi disimpan oleh `AppStateManager`, terutama:

- `tool`: menyimpan alat aktif, misalnya `SELECT`, `LINE`, `BEZIER`, `CIRCLE`, atau `POLYGON`.
- `drawing`: menandakan proses membuat objek baru sedang aktif.
- `temp_points`: menyimpan titik sementara yang digunakan saat preview mouse.
- `objects`: menyimpan objek vektor yang telah dibuat.
- `selected_obj`: menyimpan objek yang sedang dipilih.
- `algo`: menyimpan algoritma aktif, yaitu `DDA` atau `Bresenham`.
- `drag_mode` dan `active_handle_idx`: mengatur operasi drag, transformasi, dan pemindahan handle.

Kode pada `handle_events()` membedakan tiga jenis event:

1. `KEYDOWN` untuk shortcut alat dan transformasi.
2. `MOUSEBUTTONDOWN` untuk memulai klik, seleksi, atau membuat objek.
3. `MOUSEMOTION` dan `MOUSEBUTTONUP` untuk mengubah preview, memindahkan handle, atau menyelesaikan proses drag.

Objek bergambar direpresentasikan oleh `VectorShape` di `App.py`. Setiap objek menyimpan `type`, daftar `points`, dan `pivot`. Karena titik-titik disimpan sebagai koordinat vektor, objek dapat dipindahkan, diputar, dipantulkan, di-shear, dan diskalakan tanpa menggambar ulang dari bitmap.

### Select dan Transform Tool

Saat tombol **V** ditekan, `state.tool` berubah menjadi `SELECT`. Pada klik mouse, aplikasi memeriksa objek terakhir ke objek pertama menggunakan `obj.is_hit(mx, my)`. Jika objek ditemukan, objek disimpan sebagai `selected_obj`.

`VectorShape.get_pivot()` mengembalikan pivot khusus jika sudah diatur, atau mengambil pusat bounding box. Transformasi dilakukan dengan matriks 3x3 pada `Engine/Matrix3x3.py`.

Contoh transformasi yang digunakan:

- Translasi dengan `Matrix3x3.translation(dx, dy)`.
- Rotasi terhadap pivot dengan `Matrix3x3.pivot_transform(...)`.
- Shear dengan `Matrix3x3.shear(...)`.
- Scaling dengan `Matrix3x3.scaling(...)`.
- Refleksi dengan `Matrix3x3.reflection(...)`.

Gizmo pada canvas menampilkan:

- Kotak pembatas merah sebagai bounding box.
- Kotak hijau sebagai handle scaling.
- Lingkaran kuning sebagai pivot.
- Handle biru sebagai arah rotasi.

### Line Tool

Line Tool menggunakan pola dua klik pada bagian `elif self.state.tool == "LINE"` di `App.py`.

1. Klik pertama membuat `drawing = True`.
2. Titik awal disimpan pada `temp_points[0]`.
3. Pergerakan mouse memperbarui `temp_points[1]` sebagai titik akhir preview.
4. Klik kedua memvalidasi jarak titik menggunakan `math.hypot()`.
5. Jika jaraknya lebih dari 4 piksel, objek baru bertipe `LINE` ditambahkan ke `objects`.
6. Mode LINE tetap aktif sehingga pengguna dapat menggambar garis berikutnya.

Contoh pembentukan objek:

```python
nob = VectorShape("LINE")
nob.points = [list(self.state.temp_points[0]), end_point]
```

Garis kemudian dirasterisasi oleh `_draw_object()` di `Ui/Canvas.py`. Pertama, garis dipotong menggunakan `Clipper.clip_line()` berdasarkan batas artboard. Dengan opsi preview luar aktif, bagian garis yang berada di luar artboard digambar dengan warna abu-abu.

### Pen / Bézier Tool

Pen Tool juga menggunakan pola dua klik, sehingga perilakunya mirip Line Tool tetapi menghasilkan kurva Bézier kubik.

Pada klik pertama:

```python
self.state.drawing = True
self.state.temp_points = [
    [mx, my],
    [mx + 40, my - 60],
    [mx + 80, my - 60],
    [mx + 120, my]
]
```

Saat mouse bergerak, `App.py` memperbarui titik berdasarkan posisi kursor:

```python
dx = mx - start[0]
dy = my - start[1]
self.state.temp_points[1] = [start[0] + dx / 3, start[1] + dy / 3]
self.state.temp_points[2] = [start[0] + 2 * dx / 3, start[1] + 2 * dy / 3]
self.state.temp_points[3] = [mx, my]
```

Pada klik kedua:

1. Posisi klik menjadi titik akhir `P3`.
2. Titik awal dan akhir harus berjarak lebih dari 4 piksel.
3. Control point `P1` dibuat pada sepertiga jarak dari titik awal.
4. Control point `P2` dibuat pada dua pertiga jarak dari titik awal.
5. Empat titik disimpan ke objek bertipe `BEZIER`.
6. Tool tetap aktif dalam mode Pen/Bezier.

Empat titik pada kurva adalah:

- `P0`: titik awal atau titik jangkar.
- `P1`: control point pertama.
- `P2`: control point kedua.
- `P3`: titik akhir atau titik jangkar.

Fungsi kurva berada di `Engine/Curves.py` dan dihitung memakai rumus Bernstein:

\[
B(t)=(1-t)^3P_0+3(1-t)^2tP_1+3(1-t)t^2P_2+t^3P_3
\]

Nilai `t` berjalan dari `0` sampai `1`. Aplikasi membagi kurva menjadi 40 segmen, menghitung koordinat setiap segmen, lalu menghubungkan titik-titik tersebut menggunakan rasterisasi garis. Pengguna masih dapat menyeret keempat handle kurva saat objek dipilih.

### Circle Tool

Circle Tool menyimpan titik pusat dan titik pada radius menggunakan `temp_points`. Saat mouse di-drag, titik kedua diperbarui oleh jarak kursor dari titik awal. Setelah mouse dilepas, radius dihitung dengan:

```python
r = math.hypot(obj.points[1][0] - xc, obj.points[1][1] - yc)
```

Lingkaran digambar memakai Midpoint Circle Algorithm dengan simetri oktan pada `Engine/Rasterizer.py`.

### Polygon dan Pesawat

Polygon Tool dapat menerima titik-titik melalui `polygon_points`. Tombol **Enter** menyimpan poligon jika terdapat minimal tiga titik. Jika kurang dari tiga, aplikasi membuat objek pesawat sebagai contoh bentuk vektor.

Objek pesawat dibuat melalui `create_airplane_points()`. Titik template relatif terhadap posisi mouse sehingga seluruh siluet dapat ditransformasi sebagai satu objek vektor.

### Preview dan Gizmo Handle

`Ui/Canvas.py` bertanggung jawab menggambar area kerja dan elemen visual. Preview dibuat memakai objek dummy selama proses `drawing`.

Handle yang ditampilkan meliputi:

- Lingkaran titik awal saat Line atau Bezier sedang dibuat.
- Handle titik kurva saat objek Bezier dipilih.
- Pivot kuning.
- Handle rotasi biru.
- Handle scaling hijau.
- Garis bounding box merah.

Pada `MOUSEMOTION`, jika `drag_mode == "DRAG_HANDLE"`, koordinat titik yang dipilih langsung diperbarui. Perubahan ini akan muncul pada kurva atau garis saat frame berikutnya dirender.

## Penjelasan Algoritma DDA dan Bresenham

Kedua algoritma digunakan untuk menentukan piksel mana yang harus diaktifkan agar sebuah garis tampak lurus pada layar raster.

### Algoritma DDA

DDA (*Digital Differential Analyzer*) menghitung kemiringan garis menggunakan operasi penambahan desimal:

```python
steps = max(abs(dx), abs(dy))
x_inc = dx / steps
y_inc = dy / steps
```

Selanjutnya koordinat `x` dan `y` ditambah setiap iterasi. `round()` digunakan untuk memilih piksel terdekat.

Karakteristik DDA:

- Mudah dipahami dan diimplementasikan.
- Menggunakan nilai desimal atau floating-point.
- Memerlukan pembagian dan operasi tambahan per langkah.
- Ada kemungkinan akumulasi kesalahan pembulatan.
- Umumnya lebih lambat dibanding Bresenham pada rendering besar.

### Algoritma Bresenham

Bresenham menentukan piksel berikutnya menggunakan variabel kesalahan *integer* dan keputusan incremental:

```python
err = dx - dy
e2 = 2 * err
```

Nilai `e2` menentukan apakah koordinat `x`, koordinat `y`, atau keduanya harus bertambah.

Karakteristik Bresenham:

- Menggunakan operasi integer sebagai inti algoritma.
- Tidak memerlukan pembagian desimal pada proses utama.
- Lebih efisien untuk rendering real-time.
- Lebih stabil karena keputusan mengikuti nilai error kumulatif.
- Lebih cepat dan umum digunakan pada grafis raster.

### Tabel Perbandingan

| Aspek | DDA | Bresenham |
|---|---|---|
| Dasar perhitungan | Penambahan koordinat desimal | Nilai error integer |
| Operasi matematika | Pembagian dan floating-point | Penjumlahan, pengurangan, dan perkalian integer |
| Kecepatan | Lebih lambat | Lebih cepat |
| Kemudahan pembelajaran | Lebih mudah | Sedikit lebih kompleks |
| Akurasi pembulatan | Tergantung pembulatan koordinat desimal | Lebih konsisten pada keputusan piksel |
| Penggunaan memori | Tidak besar | Tidak besar |
| Cocok untuk | Pembelajaran konsep rasterisasi | Rendering real-time |

### Penggunaan pada Aplikasi

Tombol **B** mengatur `state.algo` menjadi `Bresenham`, sedangkan tombol **D** mengubahnya menjadi `DDA`. Pilihan ini digunakan oleh `_draw_object()` saat menggambar garis atau segmen kurva.

Untuk kurva Bézier, urutannya adalah:

1. `CurveEngine.get_cubic_bezier_point()` menghasilkan titik kontinu Bezier.
2. Kurva dibagi menjadi 40 segmen.
3. Dua titik berurutan segmen dihubungkan sebagai garis.
4. Garis segmen dirasterisasi memakai DDA atau Bresenham sesuai pilihan algoritma.

Dengan demikian, memilih DDA atau Bresenham tidak mengubah bentuk matematika kurva Bézier. Pilihan tersebut hanya mengubah cara pixel garis pada segmen-segmen kurva dihitung dan digambar.

---

##  Cara Menjalankan Aplikasi

1.  **Ekstrak Berkas ZIP**: Pastikan struktur folder tidak berubah setelah diekstrak.
2.  **Instalasi Dependensi**: Buka Terminal / Command Prompt pada direktori utama proyek, lalu jalankan:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Eksekusi Program**: Jalankan perintah berikut untuk membuka aplikasi:
    ```bash
    python App.py
    ```

---

##  Panduan Interaksi Mouse (Gizmo UI)
*   **Menggeser Objek**: Pada mode **Select (V)**, klik dan tahan di dalam area kotak pembatas (*bounding box*) merah objek, lalu gerakkan mouse untuk memindahkan objek.
*   **Mengubah Skala (*Scaling*)**: Klik objek hingga muncul kotak pembatas merah, lalu klik dan tarik **kotak hijau kecil** di pojok kanan bawah objek.
*   **Memanipulasi Lengkungan Kurva**: Pada objek kurva Bézier yang terpilih, klik dan tarik titik jangkar lingkaran merah (*Control Points*) untuk mengubah bentuk kelengkungan secara interaktif.
*   **Mengubah Ukuran Lembar Kerja**: Arahkan kursor mouse ke **bulatan biru** di pojok kanan bawah Artboard putih, lalu klik dan tarik untuk memperbesar atau memperkecil area batas pemotongan (*clipping bounds*) secara dinamis.
