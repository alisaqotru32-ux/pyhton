#!/usr/bin/env python3
# word_counter.py
# Penghitung kata sederhana tanpa modul eksternal

def normalize_word(w):
    """
    Hilangkan tanda baca di awal/akhir kata dan ubah ke huruf kecil.
    (Tidak menghapus tanda baca di tengah kata, contoh: "don't" tetap "don't")
    """
    punct = ".,;:!\"'()[]{}<>?\\/|@#$%^&*-_+=~`"
    start = 0
    end = len(w)
    while start < end and w[start] in punct:
        start += 1
    while end > start and w[end - 1] in punct:
        end -= 1
    return w[start:end].lower()

def count_words_from_text(text):
    """
    Mengembalikan (total_words, freq_dict)
    total_words: int jumlah kata (setelah normalisasi, non-empty)
    freq_dict: dict kata -> frekuensi
    """
    freq = {}
    total = 0
    # split berdasarkan whitespace standar (spasi, newline, tab)
    parts = text.split()
    for part in parts:
        w = normalize_word(part)
        if w:  # abaikan string kosong setelah normalisasi
            total += 1
            freq[w] = freq.get(w, 0) + 1
    return total, freq

def print_report(total, freq, top_n=10):
    print("\n--- Laporan ---")
    print("Total kata         :", total)
    print("Kata unik          :", len(freq))
    if total == 0:
        print("Tidak ada kata untuk ditampilkan.")
        return
    # urutkan kata berdasarkan frekuensi turun, jika tie urut alfabet
    items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    print(f"\nTop {min(top_n, len(items))} kata terbanyak:")
    for i, (word, count) in enumerate(items[:top_n], start=1):
        print(f"{i:2}. {word!r:20} {count} kali")

def read_file_safe(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("Error: file tidak ditemukan:", path)
    except PermissionError:
        print("Error: tidak punya izin membaca file:", path)
    except UnicodeDecodeError:
        # coba baca dengan fallback pembacaan byte-to-text sederhana
        try:
            with open(path, 'rb') as f:
                data = f.read()
            # ganti byte yang tidak bisa didecode menjadi replacement char
            text = ''.join(chr(b) for b in data)
            return text
        except Exception as e:
            print("Error membaca file (unicode):", e)
    except Exception as e:
        print("Error saat membaca file:", e)
    return None

def main():
    print("Aplikasi Penghitung Kata Sederhana")
    print("Pilih mode:")
    print("1) Ketik/Tempel teks langsung")
    print("2) Baca dari file (path)")
    print("3) Keluar")
    try:
        choice = input("Masukkan pilihan (1/2/3): ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nDibatalkan. Keluar.")
        return

    if choice == "1":
        print("\nMasukkan teks Anda. Akhiri dengan baris kosong (tekan Enter dua kali).")
        lines = []
        try:
            while True:
                line = input()
                # berhenti jika baris kosong dan sudah ada input sebelumnya
                if line == "" and lines:
                    break
                lines.append(line)
        except (KeyboardInterrupt, EOFError):
            # terima saja apa yang sudah diketik
            pass
        text = "\n".join(lines)
        total, freq = count_words_from_text(text)
        print_report(total, freq)

    elif choice == "2":
        path = input("Masukkan path file: ").strip()
        text = read_file_safe(path)
        if text is None:
            print("Gagal membaca file. Tidak ada perhitungan.")
            return
        total, freq = count_words_from_text(text)
        print_report(total, freq)

    elif choice == "3":
        print("Keluar. Sampai jumpa!")
        return

    else:
        print("Pilihan tidak dikenali. Jalankan ulang dan pilih 1, 2, atau 3.")

if __name__ == "__main__":
    main()
