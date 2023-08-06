# Latest-Indonesia-Earthquake
The package will get the latest earthquake from BMKG | Meteorological, Climatological, and Geophysical Agency

## How it Work ?
The package will scrape from [BMKG](https://www.bmkg.go.id) to get latest quake happened in Indonesia
This package will use BeautifulSoup4 and Requests, to produce output in the form of JSON that is ready to be used in web or mobile applications

## How to Use
```
import gempaterkini

if __name__ == '__main__':
    print('Aplikasi utama')
    result = gempaterkini.ekstrasi_data()
    gempaterkini.tampilkan_data(result)
```


# Author
Rizal Mustofa