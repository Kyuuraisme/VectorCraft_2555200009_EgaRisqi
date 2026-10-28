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
*   **`L`** : **Line Tool** — Membuat garis vektor lurus dengan melakukan klik & tahan (*drag*) di kanvas.
*   **`C`** : **Circle Tool** — Membuat lingkaran presisi berbasis radius dengan melakukan *drag* dari titik pusat.
*   **`P`** : **Pen / Bézier Tool** — Klik sekali pada artboard untuk memunculkan struktur kurva Bézier interaktif.

###  Pengaturan Algoritma & Preview
*   **`B`** : Mengubah mesin perentalan garis ke **Algoritma Bresenham** (Default).
*   **`D`** : Mengubah mesin perentalan garis ke **Algoritma DDA**.
*   **`O`** : Mengaktifkan / menonaktifkan mode **Preview Outside** (Bagian garis di luar artboard digambar transparan/abu-abu).

###  Manipulasi Spasial (Saat Objek Terpilih dalam Mode `V`)
*   **`R`** : Memutar (*Rotate*) objek aktif sebesar **+15°** searah jarum jam secara homogen terhadap titik pusat objek (*Center Pivot*).
*   **`S`** : Memiringkan (*Shear*) objek aktif secara linear pada koordinat sumbu X sebesar **+0.1**.
*   **`DELETE` / `BACKSPACE`** : Menghapus objek vektor yang sedang terpilih dari lembar kerja.

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
