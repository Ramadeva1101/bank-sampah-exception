"""Program utama Bank Sampah dengan exception handling."""

from exceptions import (
    BankSampahError,
    DataTidakValidError,
    SaldoTidakCukupError,
    NasabahSudahTerdaftarError,
    SampahTidakTerdaftarError,
)
from models import BankSampah, Nasabah, SampahOrganik, SampahPlastik, SampahLogam


def daftar_nasabah(bank, nama, no_hp):
    try:
        nasabah = Nasabah(nama, no_hp)
        bank.tambah_nasabah(nasabah)
    except DataTidakValidError as e:
        print("  [GAGAL] Data tidak valid:", e)
        return None
    except NasabahSudahTerdaftarError as e:
        print("  [GAGAL]", e)
        return None
    else:
        print(f"  [OK] {nama} terdaftar, kode rekening {nasabah.rekening.kode}")
        return nasabah
    finally:
        print(f"  Selesai memproses pendaftaran {nama}")


def proses_setor(bank, nasabah, sampah, berat):
    try:
        nilai = bank.setor(nasabah, sampah, berat)
    except DataTidakValidError as e:
        print("  [GAGAL] Data tidak valid:", e)
    except SampahTidakTerdaftarError as e:
        print("  [GAGAL]", e)
    else:
        print(f"  [OK] Setor {sampah.nama} {berat} kg = Rp{nilai}")
    finally:
        print(f"  Saldo {nasabah.nama}: Rp{nasabah.rekening.saldo}")


def proses_tarik(bank, nasabah, jumlah):
    try:
        bank.tarik(nasabah, jumlah)
    except SaldoTidakCukupError as e:
        print("  [GAGAL]", e)
    except DataTidakValidError as e:
        print("  [GAGAL] Data tidak valid:", e)
    else:
        print(f"  [OK] Tarik Rp{jumlah}")
    finally:
        print(f"  Saldo {nasabah.nama}: Rp{nasabah.rekening.saldo}")


if __name__ == "__main__":
    try:
        bank = BankSampah("Bank Sampah Sejahtera")
        sayur = SampahOrganik("Sayur Basah", 1000, True)
        botol = SampahPlastik("Botol Plastik", 3000, 5)
        kaleng = SampahLogam("Kaleng", 8000, "Aluminium")
        bank.tambah_sampah(sayur)
        bank.tambah_sampah(botol)
        bank.tambah_sampah(kaleng)

        print("== Membuat jenis sampah dengan harga tidak valid ==")
        try:
            besi = SampahLogam("Besi", -500, "Besi")
        except DataTidakValidError as e:
            print("  [GAGAL]", e)
        else:
            bank.tambah_sampah(besi)
        finally:
            print("  Selesai membuat jenis sampah")

        print("\n== Pendaftaran nasabah ==")
        budi = daftar_nasabah(bank, "Budi", "081234567890")
        sari = daftar_nasabah(bank, "Sari", "085711112222")
        daftar_nasabah(bank, "Budi Palsu", "081234567890")   # No HP duplikat
        daftar_nasabah(bank, "Andi", "12345")                # No HP tidak valid

        print("\n== Setoran sampah ==")
        proses_setor(bank, budi, botol, 5)
        proses_setor(bank, budi, kaleng, 1.5)
        proses_setor(bank, sari, sayur, 3)
        proses_setor(bank, sari, botol, -2)                  # berat negatif
        kardus = SampahOrganik("Kardus", 1500, False)        # tidak didaftarkan ke bank
        proses_setor(bank, sari, kardus, 2)

        print("\n== Penarikan saldo ==")
        proses_tarik(bank, budi, 10000)
        proses_tarik(bank, sari, 5000)                       # saldo tidak cukup
        proses_tarik(bank, budi, -5000)                      # jumlah negatif

        print("\n== Daftar nasabah ==")
        bank.tampil_nasabah()
        print("Riwayat", budi.rekening.kode)
        budi.rekening.tampil_riwayat()
    except BankSampahError as e:
        print("Terjadi kesalahan yang tidak terduga:", e)
    finally:
        print("\nProgram Bank Sampah selesai.")
