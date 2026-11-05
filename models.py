"""Kelas domain Bank Sampah (versi UTS + exception handling)."""

from exceptions import (
    DataTidakValidError,
    SaldoTidakCukupError,
    NasabahSudahTerdaftarError,
    SampahTidakTerdaftarError,
)


class PencatatTransaksi:
    def __init__(self):
        self._riwayat = []

    def catat(self, pesan):
        self._riwayat.append(pesan)

    def tampil_riwayat(self):
        for baris in self._riwayat:
            print(" ", baris)


class Sampah:
    def __init__(self, nama, harga_per_kg):
        self.nama = nama
        self.harga_per_kg = harga_per_kg

    @property
    def harga_per_kg(self):
        return self.__harga_per_kg

    @harga_per_kg.setter
    def harga_per_kg(self, nilai):
        # Aturan bisnis 1: harga per kg harus angka dan lebih dari 0
        if not isinstance(nilai, (int, float)) or nilai <= 0:
            raise DataTidakValidError(f"Harga per kg harus lebih dari 0, diterima: {nilai}")
        self.__harga_per_kg = nilai

    def hitung_nilai(self, berat):
        return berat * self.harga_per_kg

    def __str__(self):
        return f"{self.nama} Rp{self.harga_per_kg}/kg"


class SampahOrganik(Sampah):
    def __init__(self, nama, harga_per_kg, basah):
        super().__init__(nama, harga_per_kg)
        self.basah = basah

    def hitung_nilai(self, berat):
        nilai = super().hitung_nilai(berat)
        if self.basah:
            nilai = nilai * 80 / 100
        return nilai


class SampahPlastik(Sampah):
    def __init__(self, nama, harga_per_kg, berat_bonus):
        super().__init__(nama, harga_per_kg)
        self.berat_bonus = berat_bonus

    def hitung_nilai(self, berat):
        nilai = super().hitung_nilai(berat)
        if berat >= self.berat_bonus:
            nilai = nilai * 110 / 100
        return nilai


class SampahLogam(Sampah):
    def __init__(self, nama, harga_per_kg, jenis_logam):
        super().__init__(nama, harga_per_kg)
        self.jenis_logam = jenis_logam

    def __str__(self):
        return super().__str__() + f" ({self.jenis_logam})"


class Rekening(PencatatTransaksi):
    jumlah_rekening = 0

    def __init__(self, nama_pemilik):
        super().__init__()
        Rekening.jumlah_rekening += 1
        huruf = nama_pemilik.upper()[:3]
        self.__kode = f"{huruf}{Rekening.jumlah_rekening:03d}"
        self.__saldo = 0

    @property
    def kode(self):
        return self.__kode

    @property
    def saldo(self):
        return self.__saldo

    def setor(self, jumlah, keterangan):
        self.__saldo += jumlah
        self.catat(f"{keterangan} +Rp{jumlah}")

    def tarik(self, jumlah):
        # Aturan bisnis 4: jumlah penarikan harus lebih dari 0
        if not isinstance(jumlah, (int, float)) or jumlah <= 0:
            raise DataTidakValidError(f"Jumlah penarikan harus lebih dari 0, diterima: {jumlah}")
        # Aturan bisnis 5: penarikan tidak boleh melebihi saldo
        if jumlah > self.__saldo:
            raise SaldoTidakCukupError(self.__saldo, jumlah)
        self.__saldo -= jumlah
        self.catat(f"Tarik -Rp{jumlah}")


class Nasabah:
    def __init__(self, nama, no_hp):
        self.nama = nama
        self.no_hp = no_hp
        self.__rekening = Rekening(nama)

    @property
    def rekening(self):
        return self.__rekening

    @property
    def no_hp(self):
        return self.__no_hp

    @no_hp.setter
    def no_hp(self, nilai):
        # Aturan bisnis 2: No HP hanya angka dan diawali "08"
        if not Nasabah.validasi_hp(nilai):
            raise DataTidakValidError(f"No HP tidak valid: {nilai}")
        self.__no_hp = nilai

    @staticmethod
    def validasi_hp(no_hp):
        return isinstance(no_hp, str) and no_hp.isdigit() and no_hp.startswith("08")

    @classmethod
    def dari_teks(cls, teks):
        if teks.count(";") != 1:
            raise DataTidakValidError(f"Format teks harus 'nama;no_hp', diterima: {teks}")
        nama, no_hp = teks.split(";")
        return cls(nama, no_hp)

    def __str__(self):
        return f"{self.nama} | {self.rekening.kode} | Saldo Rp{self.rekening.saldo}"

    def __eq__(self, other):
        return isinstance(other, Nasabah) and self.no_hp == other.no_hp


class BankSampah:
    def __init__(self, nama):
        self.nama = nama
        self.__daftar_sampah = []
        self.__daftar_nasabah = []

    def tambah_sampah(self, sampah):
        self.__daftar_sampah.append(sampah)

    def tambah_nasabah(self, nasabah):
        # Aturan bisnis 6: satu No HP hanya boleh terdaftar satu kali
        if nasabah in self.__daftar_nasabah:
            raise NasabahSudahTerdaftarError(nasabah.no_hp)
        self.__daftar_nasabah.append(nasabah)

    def setor(self, nasabah, sampah, berat):
        # Aturan bisnis 3: berat setoran harus lebih dari 0
        if not isinstance(berat, (int, float)) or berat <= 0:
            raise DataTidakValidError(f"Berat setoran harus lebih dari 0, diterima: {berat}")
        # Aturan bisnis 7: sampah harus terdaftar di bank
        if sampah not in self.__daftar_sampah:
            raise SampahTidakTerdaftarError(sampah.nama)
        nilai = round(sampah.hitung_nilai(berat))
        nasabah.rekening.setor(nilai, f"Setor {sampah.nama} {berat} kg")
        return nilai

    def tarik(self, nasabah, jumlah):
        nasabah.rekening.tarik(jumlah)

    def tampil_nasabah(self):
        for n in self.__daftar_nasabah:
            print(n)
