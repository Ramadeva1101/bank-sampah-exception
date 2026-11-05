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
        if nilai <= 0:
            raise ValueError("Harga harus lebih dari 0")
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
        if jumlah > self.__saldo:
            raise ValueError("Saldo tidak cukup")
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
        if not Nasabah.validasi_hp(nilai):
            raise ValueError("No HP tidak valid")
        self.__no_hp = nilai

    @staticmethod
    def validasi_hp(no_hp):
        return no_hp.isdigit() and no_hp.startswith("08")

    @classmethod
    def dari_teks(cls, teks):
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
        self.__daftar_nasabah.append(nasabah)

    def setor(self, nasabah, sampah, berat):
        nilai = round(sampah.hitung_nilai(berat))
        nasabah.rekening.setor(nilai, f"Setor {sampah.nama} {berat} kg")
        return nilai

    def tarik(self, nasabah, jumlah):
        nasabah.rekening.tarik(jumlah)

    def tampil_nasabah(self):
        for n in self.__daftar_nasabah:
            print(n)


if __name__ == "__main__":
    bank = BankSampah("Bank Sampah Sejahtera")
    sayur = SampahOrganik("Sayur Basah", 1000, True)
    botol = SampahPlastik("Botol Plastik", 3000, 5)
    kaleng = SampahLogam("Kaleng", 8000, "Aluminium")
    bank.tambah_sampah(sayur)
    bank.tambah_sampah(botol)
    bank.tambah_sampah(kaleng)
    print(kaleng)

    budi = Nasabah("Budi", "081234567890")
    sari = Nasabah.dari_teks("Sari;085711112222")
    bank.tambah_nasabah(budi)
    bank.tambah_nasabah(sari)
    print("budi == sari :", budi == sari)
    print("budi == budi2:", budi == Nasabah("Budi", "081234567890"))

    print("Setor botol  :", bank.setor(budi, botol, 5))
    print("Setor kaleng :", bank.setor(budi, kaleng, 1.5))
    print("Setor sayur  :", bank.setor(sari, sayur, 3))
    bank.tarik(budi, 10000)

    try:
        botol.harga_per_kg = -500
    except ValueError as e:
        print("Gagal:", e)
    try:
        bank.tarik(sari, 5000)
    except ValueError as e:
        print("Gagal:", e)

    bank.tampil_nasabah()
    print("Riwayat", budi.rekening.kode)
    budi.rekening.tampil_riwayat()
