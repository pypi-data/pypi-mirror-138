import requests
from bs4 import BeautifulSoup


def data_extraction():
    """
    Date: 11 Februari 2022
    Time: 21:25:16 WIB
    Magnitude: 5.2
    Depth: 10 km
    Location: Lat=5.77 LU Lon=124.43 BT
    Description: 267 km BaratLaut TAHUNA-KEP.SANGIHE-SULUT
    Impact: tidak berpotensi TSUNAMI
    :return:
    """
    try:
        content = requests.get('https://www.bmkg.go.id/')
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')
        date_time = soup.find('span', {'class':'waktu'})
        date_time = date_time.text.split(', ')
        date = date_time[0]
        time = date_time[1]

        data = soup.find('div', {'class':'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        data = data.findChildren('li')
        i = 0
        magnitude = None
        depth = None
        lat = None
        long = None
        description = None
        impact = None

        for dat in data:
            if i == 1:
                magnitude = dat.text
            elif i == 2:
                depth = dat.text
            elif i == 3:
                location = dat.text.split(' - ')
                lat = location[0]
                long = location[1]
            elif i == 4:
                description = dat.text
            elif i == 5:
                impact = dat.text
            i += 1

        res = dict()
        res["date"] = date
        res["time"] = time
        res["magnitude"] = magnitude
        res["depth"] = depth
        res["location"] = {"lat": lat,
                           "lon": long}
        res["description"] = description
        res["impact"] = impact
        return res
    else:
        return None


def show_data(result):
    if result is None:
        print("Unable to find latest data")
        return
    print("Last Indonesia earth quake")
    print(f"Date {result['date']}")
    print(f"Time {result['time']}")
    print(f"Magnitude {result['magnitude']}")
    print(f"Depth {result['depth']}")
    print(f"Location: Lat = {result['location']['lat']}, Lon = {result['location']['lon']}")
    print(f"Description {result['description']}")
    print(f"Impact {result['impact']}")

if __name__ == '__main__':
    result = data_extraction()
    show_data(result)
