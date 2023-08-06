from bs4 import BeautifulSoup
import requests

content = 'https://www.bmkg.go.id/'
req = requests.get(content)
soup = BeautifulSoup(req.text, 'html.parser')


def test():
    try:
        if req.status_code == 200:
            print('web accessable')
            print(soup.find('title').string)
    except Exception:
        print('server down')


def earthquake():
    date = soup.find('span', {'class': 'waktu'}).string.split(', ')

    nondate = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
    nondate = nondate.findChildren('li')

    i = 0
    for j in nondate:
        if i == 1:
            magnitude = j.text
        elif i == 2:
            depth = j.text
        elif i == 3:
            geo = j.text
        elif i == 4:
            loc = j.text
        elif i == 5:
            felt = j.text
        i = i + 1

    datt = dict()
    datt['date'] = date
    datt['magnitude'] = magnitude
    datt['depth'] = depth
    datt['geo'] = geo.split(' - ')
    datt['loc'] = loc.replace('Pusat gempa ', '')
    datt['felt'] = felt.replace('Dirasakan ', '')

    print("last earthquake report by BMKG:")
    print(f"date {datt['date'][0]}")
    print(f"time {datt['date'][1]}")
    print(f"magnitude {datt['magnitude']}")
    print(f"depth {datt['depth']}")
    print(f"Geo {datt['geo'][0]} & {datt['geo'][1]}")
    print(f"epicenter {datt['loc']}")
    print(f"felt {datt['felt']}")


def article():
    main = soup.find('div', {'class': 'col-md-4 artikel-pengumuman-home md-margin-bottom-20'})

    dat = []
    news = main.findChildren('h3')
    for i in news:
        dat.append(i.text)

    datt = []
    date = main.findChildren('li')
    for j in date:
        datt.append(j.text)

    print('This is the last article on BMKG:')
    print(f"{dat[0]}, published on {datt[0]}")
    print(f"{dat[1]}, published on {datt[1]}")
    print(f"{dat[2]}, published on {datt[2]}")
    print(f"{dat[3]}, published on {datt[3]}")

