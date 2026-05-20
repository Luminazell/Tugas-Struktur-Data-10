# ⚡ Advanced Sorter & Expression-Driven In-Place HeapSorter

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/)

Implementasi solusi komprehensif untuk analisis struktur data, algoritma pengurutan tingkat lanjut (*sorting*), pohon biner (*binary tree*), dan mekanisme *heap*. Seluruh modul dibangun menggunakan murni **Python 3** tanpa dependensi *library* eksternal, dirancang khusus untuk memenuhi batasan memori ketat ($O(1)$ *auxiliary space*) serta menjaga stabilitas data pada sistem *embedded*.

---

## 📌 Fitur Utama Modul

### 🔹 1. Advanced Sorter
* **Array Merge Sort (Virtual Sublists):** Memanfaatkan teknik indeksasi sublist virtual dan hanya mengalokasikan **satu** `tmpArray` berukuran $n$ di awal proses. Mengurangi overhead memori secara masif menjadi $O(1)$ ruang tambahan di luar array input. Operasi dijamin stabil (*stable*).
* **Linked List Merge Sort:** Menggunakan strategi *Fast-Slow Pointer* untuk mendeteksi titik tengah *Singly Linked List* dalam satu kali jalan ($O(n)$) tanpa menghitung total node terlebih dahulu. Proses penyambungan kembali (*merging*) dibantu oleh *Dummy Node* dan *Tail Reference* sehingga bebas dari alokasi objek node baru.
* **Quick Sort dengan Fallback Limiter:** Dilengkapi pemilihan pivot berbasis *Median-of-Three* (awal, tengah, akhir) guna menghindari degradasi performa $O(n^2)$ pada pola data terbalik (*descending*). Jika kedalaman rekursi menembus batas aman $2 \times \log_2(n)$, sistem otomatis dialihkan (*fallback*) ke Merge Sort.

### 🔹 2. Expression-Driven HeapSorter
* **Expression Tree Builder & Evaluator:** Mem-parse ekspresi aritmetika terparentheses penuh (contoh: `((8*5)+(9/(7-4)))`) secara rekursif menggunakan antrian token (`collections.deque`). Evaluasi diproses menggunakan traversal **Postorder** untuk mengekstrak urutan kalkulasi intermediet secara otomatis.
* **In-Place Max-Heap Construction:** Mengonversi list hasil evaluasi menjadi struktur *Max-Heap* secara langsung pada memori yang sama menggunakan skema *Bottom-Up Sift-Down* dengan pemetaan indeks anak kiri ($2i + 1$) dan anak kanan ($2i + 2$).
* **In-Place Heapsort:** Mengurutkan array secara meningkat (*ascending*) dengan menukar elemen akar maksimum ke ujung belakang array dan melakukan *sift-down* berulang pada porsi heap yang tersisa.
* **Complete Tree Validator:** Melakukan pengujian berbasis matematika indeks untuk memastikan representasi array tidak memiliki "lubang" kosong (*missing intermediate nodes*), membuktikan kepatuhan terhadap properti *Complete Binary Tree*.

---

## 📐 Representasi Struktur Pohon

Sebagai contoh, ekspresi aritmetika `((8*5)+(9/(7-4)))` secara internal diuraikan oleh modul menjadi struktur pohon biner berikut:

```text
          [ + ]   <-- Root Utama
         /     \
     [ * ]     [ / ]
     /   \     /   \
   [8]   [5] [9]   [ - ]
                   /   \
                 [7]   [4]

Evaluasi dilakukan secara Postorder (Kiri -> Kanan -> Akar), menghasilkan deretan nilai kalkulasi intermediet sebelum akhirnya diurutkan menggunakan Heapsort secara in-place.

🛠️ Struktur Repositori
Disarankan untuk menata berkas di dalam repositori Anda dengan struktur minimalis seperti berikut:
📦 advanced-sorter-heap
 ┣ 📜 README.md          # Dokumentasi proyek (File ini)
 ┗ 📜 main.py             # Kode implementasi Python & script pengujian

🚀 Panduan Memulai
Prasyarat
Pastikan komputer Anda sudah terpasang Python versi 3.8 atau yang lebih baru.
python --version

Eksekusi Program
Cloning repositori ini atau unduh kodenya, kemudian jalankan berkas pengujian utama melalui terminal:
python main.py

Contoh Hasil Keluaran Kontrol
--- [TESTING MODUL 1: AdvancedSorter] ---
Awal Array : [38, 27, 43, 3, 9, 82, 10]
Hasil Sort : [3, 9, 10, 27, 38, 43, 82]

Awal Linked List: 4 -> 2 -> 1 -> 3
Hasil Linked List: 1 -> 2 -> 3 -> 4 

--- [TESTING MODUL 2: ExprHeapSorter] ---
Ekspresi Arismatika: ((8*5)+(9/(7-4)))
Hasil Evaluasi (Postorder List Intermediet): [8, 5, 40, 9, 7, 4, 3, 3, 43]
Array Gabungan Tambahan (Sebelum Heapsort): [8, 5, 40, 9, 7, 4, 3, 3, 43, 15, 40, 2, 7]
Array Setelah Di-Heapsort (Ascending)     : [2, 3, 3, 4, 5, 7, 7, 8, 9, 15, 40, 40, 43]
Apakah Valid Melambangkan Complete Tree?   : True
