from typing import List, Optional, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import httpx
import pandas as pd
from itertools import zip_longest


app = FastAPI(
    title="Government API Documentation",
    description="API untuk mengelola data pemerintahan",
    docs_url="/",  # Ubah docs_url menjadi "/"
)

# Endpoint untuk mengakses path root "/"a
@app.get("/")
async def read_root():
    return {'example': 'Kamu telah berhasil masuk ke API Government', "Data":"Successful"}

# schema model untuk data pajak objek wisata
class Pajak(BaseModel):
    id_pajak: str
    status_kepemilikan: str
    jenis_pajak: str
    tarif_pajak: float
    besar_pajak: int
    
# Data dummy untuk tabel pajak_objek_wisata
data_pajak =[
    {'id_pajak': 'PJ001', 'status_kepemilikan': 'Swasta', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': 0.11, 'besar_pajak': 50000000},
    {'id_pajak': 'PJ002', 'status_kepemilikan': 'Swasta', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': 0.11, 'besar_pajak': 100000000},
    {'id_pajak': 'PJ003', 'status_kepemilikan': 'Pemerintah', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': 0, 'besar_pajak': 0},
    {'id_pajak': 'PJ004', 'status_kepemilikan': 'Pemerintah', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': 0.11, 'besar_pajak': 75000000},
    {'id_pajak': 'PJ005', 'status_kepemilikan': 'Campuran', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': 0.11, 'besar_pajak': 65000000}
]

# Endpoint untuk menambahkan data pajak objek wisata
@app.post("/pajak")
async def add_pajak(pajak: Pajak):
    data_pajak.append(pajak.dict())
    return {"message": "Data Pajak Objek Wisata Berhasil Ditambahkan."}

#Endpoint untuk mendapatkan data pajak objek wisata
@app.get("/pajak", response_model=List[Pajak])
async def get_pajak():
    return data_pajak

def get_pajak_index(id_pajak):
    for index, pajak in enumerate(data_pajak):
        if pajak['id_pajak'] == id_pajak:
            return index
    return None

# Endpoint untuk mengambil detail data pajak sesuai dengan input id_pajak
@app.get("/pajak/{id_pajak}", response_model=Optional[Pajak])
def get_pajak_by_id(id_pajak: str):
    for pajak in data_pajak:
        if pajak['id_pajak'] == id_pajak:
            return Pajak(**pajak)
    return None

# Endpoint untuk memperbarui data pajak objek wisata dengan memasukkan id_pajak saja
@app.put("/pajak/{id_pajak}")
def update_pajak_by_id(id_pajak: str, update_pajak: Pajak):
    index = get_pajak_index(id_pajak)
    if index is not None:
        data_pajak[index] = update_pajak.dict()
        return {"message": "Data wisata berhasil diperbarui."}
    else:
        raise HTTPException(status_code=404, detail="Data Pajak Objek Wisata Tidak Ditemukan.")

# Endpoint untuk menghapus data pajak objek wisaya by id_pajak
@app.delete("/pajak/{id_pajak}")
def delete_pajak_by_id(id_pajak: str):
    index = get_pajak_index(id_pajak)
    if index is not None:
        del data_pajak[index]
        return {"message": "Data Pajak Objek Wisata Berhasil Dihapus."}
    else:
        raise HTTPException(status_code=404, detail="Data Pajak Objek Wisata Tidak Berhasil Dihapus.")

# Fungsi untuk mengambil data objek wisata dari website objek wisata
async def get_data_wisata_from_web():
    url = "https://pajakobjekwisata.onrender.com/wisata"  # URL Endpoint API dari Objek Wisata
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data Objek Wisata")

# Schema Model untuk data Objek Wisata
class Wisata(BaseModel):
    id_wisata: str
    nama_objek: str

# Endpoint untuk mendapatkan data objek wisata
@app.get('/wisata', response_model=List[Wisata])
async def get_wisata():
    data_wisata = await get_data_wisata_from_web()
    return data_wisata

# Fungsi untuk mendapatkan indeks objek wisata berdasarkan id_wisata
async def get_wisata_index(id_wisata: str):
    data_wisata = await get_data_wisata_from_web()
    for index, wisata in enumerate(data_wisata):
        if wisata['id_wisata'] == id_wisata:
            return index
    return None

# Endpoint untuk mengambil detail data objek wisata sesuai dengan input id_wisata
@app.get("/wisata/{id_wisata}", response_model=Optional[Wisata])
async def get_wisata_by_id(id_wisata: str):
    data_wisata = await get_data_wisata_from_web()
    for wisata in data_wisata:
        if wisata['id_wisata'] == id_wisata:
            return Wisata(**wisata)
    return None

# untuk penduduk

class Penduduk (BaseModel):
    nik: int
    nama: str
    provinsi: str
    kota: str
    kecamatan: str
    desa: str

# Data Dummy untuk tabel penduduk
data_penduduk =[
    {'nik':101, 'nama':'Ale', 'provinsi': 'Jawa Barat', 'kota': 'Bandung', 'kecamatan': 'Dayeuhkolot', 'desa': 'Bojongsoang'},
    {'nik':102, 'nama':'Leo', 'provinsi': 'Bali', 'kota': 'Gianyar', 'kecamatan': 'Gianyar', 'desa': 'Siangan'},
    {'nik':103, 'nama':'Lea', 'provinsi': 'Jawa Tengah', 'kota': 'Yogyakarta', 'kecamatan': 'Gedongtengen', 'desa': 'Sosromeduran'},
    {'nik':104, 'nama':'Satoru', 'provinsi': 'Jawa Timur', 'kota': 'Surabaya', 'kecamatan': 'Tenggilis Mejoyo', 'desa': 'Kendangsari'},
    {'nik':105, 'nama':'Suguru', 'provinsi': 'DKI Jakarta', 'kota': 'Jakarta Selatan', 'kecamatan': 'Kebayoran Baru', 'desa': 'Senayan'},

    {'nik':106, 'nama':'Ammar', 'provinsi': 'Banten', 'kota': 'Tangeran Selatan', 'kecamatan': 'Serpong', 'desa': 'Rawa Buntu'},
    {'nik':107, 'nama':'Alif', 'provinsi': 'Sumatera Barat', 'kota': 'Padang', 'kecamatan': 'Kuranji', 'desa': 'Ampang'},
    {'nik':108, 'nama':'Malvin', 'provinsi': 'Jawa Barat', 'kota': 'Bogor', 'kecamatan': 'Bogor Selatan', 'desa': 'Cikaret'},
    {'nik':109, 'nama':'Agung', 'provinsi': 'Jawa Timur', 'kota': 'Jember', 'kecamatan': 'Pakusari', 'desa': 'Kertosari'},
    {'nik':110, 'nama':'Fadlan', 'provinsi': 'Banten', 'kota': 'Serang', 'kecamatan': 'Taktakan', 'desa': 'Kalang Anyar'},

    {'nik':111, 'nama':'Chadkowi', 'provinsi': 'Kota Bandung', 'kota': 'Bandung', 'kecamatan': 'Buah Batu', 'desa': 'Margasari'},
    {'nik':112, 'nama':'Prabroro', 'provinsi': 'DKI Jakarta', 'kota': 'Jakarta Timur', 'kecamatan': 'Jatinegara', 'desa': 'Cipinang'},
    {'nik':113, 'nama':'Anisa', 'provinsi': 'DIY', 'kota': 'Sleman', 'kecamatan': 'Sleman', 'desa': 'Triharjo'},
    {'nik':114, 'nama':'Janggar', 'provinsi': 'Bali', 'kota': 'Badung', 'kecamatan': 'Kuta', 'desa': 'Seminyak'},
    {'nik':115, 'nama':'Mahfud DM', 'provinsi': 'Jawa Timur', 'kota': 'Surabaya', 'kecamatan': 'Gayungan', 'desa': 'Gayungan'},
   
    {'nik':116, 'nama':'Ali', 'provinsi': 'Banten', 'kota': 'Tangerang Selatan', 'kecamatan': 'Ciputat Timur', 'desa': 'Bintaro Sektor 3A'},
    {'nik':117, 'nama':'Sandra', 'provinsi': 'Jawa Barat', 'kota': 'Bandung', 'kecamatan': 'Sumur Bandung', 'desa': 'Karanganyar'},
    {'nik':118, 'nama':'Joseph', 'provinsi': 'Jawa Tengah', 'kota': 'Magelang', 'kecamatan': 'Magelang Utara', 'desa': 'Wates'},
    {'nik':119, 'nama':'Lisa', 'provinsi': 'DI Yogyakarta', 'kota': 'Yogyakarta', 'kecamatan': 'Kota Gede', 'desa': 'Purbayan'},
    {'nik':120, 'nama':'Bagus', 'provinsi': 'DKI Jakarta', 'kota': 'Jakarta Barat', 'kecamatan': 'Taman Sari', 'desa': 'Maphar'},
]

    # untuk post data kita ke kelompok lain
@app.post('/penduduk', response_model=Penduduk)
async def post_penduduk(penduduk: Penduduk):
    data_penduduk.append(penduduk.dict())
    return penduduk

# untuk menampilkan data kita sendiri
@app.get('/penduduk', response_model=List[Penduduk])
async def get_penduduk():
    return data_penduduk

# ================================================================================== (RENTAL MOBIL)

class Pendudukrental (BaseModel):
    nik: int
    nama: str
    kota: str

data_Pendudukrental =[
    {'nik':101, 'nama':'Ale', 'kota': 'Bandung'},
    {'nik':102, 'nama':'Leo', 'kota': 'Gianyar'},
    {'nik':103, 'nama':'Lea',  'kota': 'Yogyakarta'},
    {'nik':104, 'nama':'Satoru', 'kota': 'Surabaya'},
    {'nik':105, 'nama':'Suguru','kota': 'Jakarta Selatan',},
]
    # untuk post data kita ke kelompok  rental mobil

@app.post("/pendudukrental")
def tambah_pendudukrental(pendudukrental: Pendudukrental):
    data_Pendudukrental.append(pendudukrental.dict())
    return {"message": "Data Penduduk berhasil ditambahkan."}

# untuk menampilkan data kita sendiri kelompok rental mobil
@app.get('/pendudukrental', response_model=List[Pendudukrental])
async def get_pendudukrental():
    return data_Pendudukrental

def get_pendudukrental_index(nik: str) -> Optional[int]:
    for index, pendudukrental in enumerate(data_Pendudukrental):
        if pendudukrental['nik'] == nik:
            return index
    return None

@app.get("/pendudukrental/{nik}", response_model=Pendudukrental)
def get_pendudukrental_by_nik(nik: int):
    index = get_pendudukrental_index(nik)
    if index is not None:
        return Pendudukrental(**data_Pendudukrental[index])
    raise HTTPException(status_code=404, detail="Data Penduduk tidak ditemukan.")

# ================================================================================== (HOTEL)

class Pendudukhotel (BaseModel):
    nik: int
    nama: str
    kota: str

data_Pendudukhotel =[
    {'nik':101, 'nama':'Ale', 'kota': 'Bandung'},
    {'nik':102, 'nama':'Leo', 'kota': 'Gianyar'},
    {'nik':103, 'nama':'Lea',  'kota': 'Yogyakarta'},
    {'nik':104, 'nama':'Satoru', 'kota': 'Surabaya'},
    {'nik':105, 'nama':'Suguru','kota': 'Jakarta Selatan',},
]
    # untuk post data kita ke kelompok hotel
@app.post('/pendudukhotel', response_model=Pendudukhotel)
async def post_pendudukhotel(pendudukhotel: Pendudukhotel):
    data_Pendudukhotel.append(pendudukhotel.dict())
    return pendudukhotel

# untuk menampilkan data kita sendiri kelompok hotel
@app.get('/pendudukhotel', response_model=List[Pendudukhotel])
async def get_pendudukhotel():
    return data_Pendudukhotel


# ================================================================================== (ASURANSI)

class Pendudukasuransi (BaseModel):
    nik: int
    nama: str
    provinsi: str
    kota: str
    kecamatan: str
    desa : str

data_Pendudukasuransi =[
    {'nik':116, 'nama':'Ali', 'provinsi': 'Banten', 'kota': 'Tangerang Selatan', 'kecamatan': 'Ciputat Timur', 'desa': 'Bintaro Sektor 3A'},
    {'nik':117, 'nama':'Sandra', 'provinsi': 'Jawa Barat', 'kota': 'Bandung', 'kecamatan': 'Sumur Bandung', 'desa': 'Karanganyar'},
    {'nik':118, 'nama':'Joseph', 'provinsi': 'Jawa Tengah', 'kota': 'Magelang', 'kecamatan': 'Magelang Utara', 'desa': 'Wates'},
    {'nik':119, 'nama':'Lisa', 'provinsi': 'DI Yogyakarta', 'kota': 'Yogyakarta', 'kecamatan': 'Kota Gede', 'desa': 'Purbayan'},
    {'nik':120, 'nama':'Bagus', 'provinsi': 'DKI Jakarta', 'kota': 'Jakarta Barat', 'kecamatan': 'Taman Sari', 'desa': 'Maphar'},
]
    # untuk post data kita ke kelompok asuransi
@app.post('/pendudukasuransi', response_model=Pendudukasuransi)
async def post_pendudukasuransi(pendudukasuransi: Pendudukasuransi):
    data_Pendudukasuransi.append(pendudukasuransi.dict())
    return pendudukasuransi

# untuk menampilkan data kita sendiri kelompok asuransi
@app.get('/pendudukasuransi', response_model=List[Pendudukasuransi])
async def get_pendudukasuransi():
    return data_Pendudukasuransi

def get_pendudukasuransi_index(nik: str) -> Optional[int]:
    for index, pendudukasuransi in enumerate(data_Pendudukasuransi):
        if pendudukasuransi['nik'] == nik:
            return index
    return None

@app.get("/pendudukasuransi/{nik}", response_model=Pendudukasuransi)
def get_pendudukasuransi_by_nik(nik: int):
    index = get_pendudukasuransi_index(nik)
    if index is not None:
        return Pendudukasuransi(**data_Pendudukasuransi[index])
    raise HTTPException(status_code=404, detail="Data Penduduk tidak ditemukan.")

# =========================================== (BATAS PENDUDUK ASURANSI)

# ================================================================================== (BANK)

class Pendudukbank (BaseModel):
    nik: int
    nama: str


data_Pendudukbank =[
    {'nik':106, 'nama':'Ammar'},
    {'nik':107, 'nama':'Alif'},
    {'nik':108, 'nama':'Malvin'},
    {'nik':109, 'nama':'Agung'},
    {'nik':110, 'nama':'Fadlan'},

]
    # untuk post data kita ke kelompok asuransi
@app.post('/pendudukbank', response_model=Pendudukbank)
async def post_pendudukbank(pendudukbank: Pendudukbank):
    data_Pendudukbank.append(pendudukbank.dict())
    return pendudukbank

# untuk menampilkan data kita sendiri kelompok hotel
@app.get('/pendudukbank', response_model=List[Pendudukbank])
async def get_pendudukbank():
    return data_Pendudukbank

def get_pendudukbank_index(nik: str) -> Optional[int]:
    for index, pendudukbank in enumerate(data_Pendudukbank):
        if pendudukbank['nik'] == nik:
            return index
    return None

@app.get("/pendudukbank/{nik}", response_model=Pendudukbank)
def get_pendudukbank_by_nik(nik: int):
    index = get_pendudukbank_index(nik)
    if index is not None:
        return Pendudukbank(**data_Pendudukbank[index])
    raise HTTPException(status_code=404, detail="Data Penduduk tidak ditemukan.")

# =========================================== (BATAS PENDUDUK BANK)

# untuk get data sendiri (berdasakan index)
def get_penduduk_index(nik):
    for index, penduduk in enumerate(data_penduduk):
        if penduduk['nik'] == nik:
            return index
    return None

# untuk get data sendiri (berdasarkan NIK)
@app.get("/penduduk/{nik}", response_model=Optional[Penduduk])
def get_penduduk_by_id(nik: int):
    for penduduk in data_penduduk:
        if penduduk['nik'] == nik:
            return Penduduk(**penduduk)
    return None

# untuk update data sendiri 
@app.put("/penduduk/{nik}")
def update_penduduk_by_id(nik: int, update_penduduk: Penduduk):
    index = get_penduduk_index(nik)
    if index is not None:
        data_penduduk[index] = update_penduduk.dict()
        return {"message": "Data Penduduk berhasil diperbarui."}
    else:
        raise HTTPException(status_code=404, detail="Data Penduduk Tidak Ditemukan.")
    
# untuk menghapus data
@app.delete("/penduduk/{nik}")
def delete_penduduk_by_id(nik: int):
    index = get_penduduk_index(nik)
    if index is not None:
        del data_penduduk[index]
        return {"message": "Data (nama datanya) Berhasil Dihapus."}
    else:
        raise HTTPException(status_code=404, detail="Data Penduduk Tidak Berhasil Dihapus.")
    


# untuk get data dari kelompok asuransi menggunakan url web hosting
async def get_asuransi_from_web():
    url = "https://eai-fastapi.onrender.com/penduduk"  #endpoint kelompok asuransi
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail = "Gagal mengambil Penduduk.")

# untuk get data dari kelompok bank menggunakan url web hosting (bank)
async def get_bank_from_web():
    url = "https://jumantaradev.my.id/"  #endpoint kelompok bank
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail = "Gagal mengambil Penduduk.")

# untuk get data dari kelompok hotel menggunakan url web hosting (hotel)
async def get_hotel_from_web():
    url = "https://hotelbaru.onrender.com"  #endpoint kelompok hotel
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail = "Gagal mengambil Penduduk.")
    
# untuk get data dari kelompok bank menggunakan url web hosting (rental mobil)
async def get_rental_from_web():
    url = "https://rental-mobil-api.onrender.com/pelanggan"  #endpoint kelompok rental mobil
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail = "Gagal mengambil Penduduk.")
    
# untuk get data dari kelompok tour guide menggunakan url web hosting (Tour Guide)
async def get_guide_from_web():
    url = "https://tour-guide-ks4n.onrender.com/tourguide"  #endpoint kelompok tour guide
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail = "Gagal mengambil Tour Guide.") 

class Asuransi(BaseModel):
    nik: int
    nama: str

class Bank(BaseModel):
    nik: int
    nama: str

class Hotel(BaseModel):
    nik: int
    nama: str
    kabupaten: str

class Rental(BaseModel):
    nomor_telepon:str
    email:str

class Guide(BaseModel):
    id_guider: str
    nama_guider: str
    
# untuk mendapatkan hasil dari kelompok lain (asuransi)
@app.get('/penduduk/asuransi', response_model=List[Asuransi])
async def get_asuransi():
    data_asuransi = get_bank_from_web()
    return data_asuransi

# untuk mendapatkan hasil dari kelompok lain (bank)
@app.get('/penduduk/bank', response_model=List[Bank])
async def get_bank():
    data_bank = get_bank_from_web()
    return data_bank

# untuk mendapatkan hasil dari kelompok lain (hotel)
@app.get('/penduduk/hotel', response_model=List[Hotel])
async def get_hotel():
    data_hotel = get_hotel_from_web()
    return data_hotel

# untuk mendapatkan hasil dari kelompok lain (rental mobil)
@app.get('/pelanggan', response_model=List[Rental])
async def get_pelanggan():
    data_pelanggan = await get_rental_from_web()
    return data_pelanggan

# untuk mendapatkan hasil dari kelompok lain (Tour Guide)
# untuk mendapatkan hasil dari kelompok lain (Tour Guide)
@app.get('/tourguide', response_model=List[Guide])
async def get_tourguide():
    data_tourguide = await get_guide_from_web()
    return data_tourguide

# chema model untuk data SETORAN PAJAK OBJEK WISATA UNTUK BANK
class Setoran(BaseModel):
    id_setoran:int
    id_pajak: str
    tanggal_jatuh_tempo: str
    tanggal_setoran: str
    status_setoran: str
    denda: float
    besar_pajak_setelah_denda: int
    
# Data dummy untuk tabel pajak_objek_wisata
data_setoran = [
    {'id_setoran': 1, 'id_pajak': 'PJ001', 'tanggal_jatuh_tempo': '30-11-2023', 'tanggal_setoran': '30-11-2023', 'status_setoran': 'tepat waktu', 'denda': 0, 'besar_pajak_setelah_denda': 0},
    {'id_setoran': 2, 'id_pajak': 'PJ002', 'tanggal_jatuh_tempo': '30-11-2023', 'tanggal_setoran': '30-11-2023', 'status_setoran': 'terlambat', 'denda': 0.02, 'besar_pajak_setelah_denda': 100000000},
    {'id_setoran': 3, 'id_pajak': 'PJ003', 'tanggal_jatuh_tempo': '30-11-2023', 'tanggal_setoran': '30-11-2023', 'status_setoran': 'tepat waktu', 'denda': 0, 'besar_pajak_setelah_denda': 0},
    {'id_setoran': 4, 'id_pajak': 'PJ004', 'tanggal_jatuh_tempo': '30-11-2023', 'tanggal_setoran': '30-11-2023', 'status_setoran': 'terlambat', 'denda': 0.02, 'besar_pajak_setelah_denda': 75000000},
    {'id_setoran': 5, 'id_pajak': 'PJ005', 'tanggal_jatuh_tempo': '30-11-2023', 'tanggal_setoran': '30-11-2023', 'status_setoran': 'tepat waktu', 'denda': 0, 'besar_pajak_setelah_denda': 0}
]

# Endpoint untuk menambahkan data pajak objek wisata
@app.post("/setoranpajak")
async def add_setoran(setoranpajak: Setoran):
    data_setoran.append(setoranpajak.dict())
    return {"message": "Data Setoran Pajak Objek Wisata Berhasil Ditambahkan."}

#Endpoint untuk mendapatkan data pajak objek wisata
@app.get("/setoranpajak", response_model=List[Setoran])
async def get_setoran():
    return data_setoran

def get_setoran_index(id_setoran):
    for index, pajak in enumerate(data_setoran):
        if pajak['id_setoran'] == id_setoran:
            return index
    return None

# @app.get("/setoranpajak/{status_setoran}", response_model=Optional[Setoran])
# def get_setoran_by_status(status_setoran: str):
#     for pajaksetoran in data_setoran:
#         if pajaksetoran['status_setoran'] == status_setoran:
#             return Setoran(**pajaksetoran)
#     raise HTTPException(status_code=404, detail="Setoran not found")
class NotFoundResponse(BaseModel):
    status_setoran: str
    detail: str

@app.get("/setoranpajak/{status_setoran}", response_model=Union[Setoran, NotFoundResponse])
def get_setoran_by_status(status_setoran: str):
    for pajaksetoran in data_setoran:
        if pajaksetoran['status_setoran'] == status_setoran:
            return Setoran(**pajaksetoran)
    return NotFoundResponse(status_setoran=status_setoran, detail=f"Setoran pajak dengan status '{status_setoran}' tidak ditemukan")



# Function to check for penalties and calculate fine
# def calculate_fine(setoran, current_date, fine_rate=0.02):
#     due_date = setoran['tanggal_jatuh_tempo']
#     if due_date < current_date:
#         # Calculate the number of days overdue
#         overdue_days = (current_date - due_date).days
#         # Calculate the fine as a percentage of the 'besar_pajak'
#         fine_amount = setoran['besar_pajak'] * fine_rate * (overdue_days / 30)  # Assuming fine is per month
#         setoran['denda'] = fine_amount
#     else:
#         setoran['denda'] = 0



# # menyatukan data pajak dan wisata ke dalam satu tabel
# async def combine_pajak_wisata():
#     pajak_data = get_pajak()
#     wisata_data = get_wisata()

#     combined_data = []
#     for pajak in pajak_data:
#         for wisata in wisata_data:
#             combined_obj = {
#                 "id_pajak": pajak['id_pajak'],
#                 "wisata": wisata
#             }
#             combined_data.append(combined_obj)
#     return combined_data  

# class PajakWisata(BaseModel):
#     id_pajak: str
#     wisata : Wisata

# @app.get("/pajakwisata", response_model=List[PajakWisata])
# def get_combined_data():
#     combined_data = combine_pajak_wisata()
#     return combined_data
# Schema model untuk data gabungan


class Pajakwisata(BaseModel):
    id_pajak: str
    status_kepemilikan: str
    jenis_pajak: str
    tarif_pajak: float
    besar_pajak: int
    id_wisata : str
    nama_objek : str

# @app.get('/pajakwisata', response_model=List[Pajakwisata])
# async def get_pajakwisata():
#     try:
#         # Debugging: Print data yang diambil dari endpoint eksternal
#         data_wisata = await get_data_wisata_from_web()
        
#         # Debugging: Print data yang diambil dari endpoint eksternal
#         print("Data Wisata dari Web:", data_wisata)
        
#         # Konversi data pajak dan wisata ke DataFrame pandas
#         df_pajak = pd.DataFrame(data_pajak)
#         df_wisata = pd.DataFrame(data_wisata)
        
#         # Debugging: Print data yang diambil dari dataset lokal
#         print("Data Pajak Lokal:", df_pajak)
        
#         # Pastikan kolom yang diperlukan ada di kedua data
#         if 'id_pajak' not in df_pajak.columns:
#             raise ValueError("Kolom 'id_pajak' tidak ditemukan pada data pajak lokal")
#         if 'id_wisata' not in df_wisata.columns:
#             raise ValueError("Kolom 'id_wisata' tidak ditemukan pada data wisata eksternal")
        
#         # Lakukan join (disini asumsikan join berdasarkan beberapa aturan logika, bisa disesuaikan)
#         df_pajakwisata = pd.merge(df_pajak, df_wisata, left_on='id_pajak', right_on='id_wisata')

#         # Debugging: Print data setelah join
#         print("Data Gabungan:", df_pajakwisata)

#         # Konversi hasil join ke list of dict
#         data_pajakwisata = df_pajakwisata.to_dict(orient='records')

#         return data_pajakwisata
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# Endpoint untuk mendapatkan data gabungan pajak dan objek wisata
@app.get('/pajakwisata', response_model=List[Pajakwisata])
async def get_pajak_wisata():
    data_wisata = await get_data_wisata_from_web()

    # Menggunakan zip_longest untuk menggabungkan data pajak dan data wisata
    gabungan_data = []
    for pajak, wisata in zip_longest(data_pajak, data_wisata, fillvalue={}):
        gabungan_data.append(Pajakwisata(
            id_pajak=pajak.get('id_pajak', None),
            status_kepemilikan=pajak.get('status_kepemilikan', None),
            jenis_pajak=pajak.get('jenis_pajak', None),
            tarif_pajak=pajak.get('tarif_pajak', None),
            besar_pajak=pajak.get('besar_pajak', None),
            id_wisata=wisata.get('id_wisata', None),
            nama_objek=wisata.get('nama_objek', None)
        ))

    return gabungan_data