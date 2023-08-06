import requests
from bs4 import BeautifulSoup

import gempaterkini


def ekstrasi_data():
    """
    Tanggal: 04 Februari 2022
    Waktu: 17:10:45 WIB
    Magnitudo: 5.5
    Kedalaman: 10 km
    Lokasi: LS=7.48 LS - BT=105.92 BT
    Pusat gempa: Pusat gempa berada di laut 71 Km Barat Daya Bayah
    Dirasakan: Dirasakan (Skala MMI): IV Pelabuhan Ratu, III Malingping, III Bayah, III Cihara, III Panggarangan
    :return:
    """
    try:
        content = requests.get('https://bmkg.go.id')
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        result = soup.find('span', {'class': 'waktu'})
        result = result.text.split(', ')
        waktu = result[1]
        tanggal = result[0]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')
        i = 0
        magnitudo = None
        kedalaman = None
        ls = None
        bt = None
        lokasi = None
        keterangan = None

        for res in result:
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text.split(' - ')
                ls = koordinat [0]
                bt = koordinat [1]
            elif i == 4:
                lokasi = res.text
            elif i == 5:
                keterangan = res.text
            i = i + 1

        hasil = dict()
        hasil['tanggal'] = tanggal
        hasil['waktu'] = waktu
        hasil['magnitudo'] = magnitudo
        hasil['kedalaman'] = kedalaman
        hasil['koordinat'] = {'ls': ls, 'bt': bt }
        hasil['lokasi'] = lokasi
        hasil['keterangan'] = keterangan
        return hasil
    else:
        return None


def tampilkan_data(result):
    if result is None:
        print("Tidak bisa menemukan data gempa terkini")
        return

    print('Gempa terakhir berdasarkan BMKG')
    print(f"Tanggal {result['tanggal']}")
    print(f"Waktu {result['waktu']}")
    print(f"Magnitudo: {result['magnitudo']}")
    print(f"Kedalaman: {result['kedalaman']}")
    print(f"Koordinat: LS={result['koordinat']['ls']}, BT={result['koordinat']['bt']}")
    print(f"Lokasi: {result['lokasi']}")
    print(f"Keterangan: {result['keterangan']}")

if __name__ == '__main__':
    result = ekstrasi_data()
    tampilkan_data(result)