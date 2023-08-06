from bs4 import BeautifulSoup
import requests


def data():
    test = requests.get('https://www.bmkg.go.id/')
    soup = BeautifulSoup(test.text, 'html.parser')

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

    return datt


def show(i):
    print("last earthquake report by BMKG:")
    print(f"date {i['date'][0]}")
    print(f"time {i['date'][1]}")
    print(f"magnitude {i['magnitude']}")
    print(f"depth {i['depth']}")
    print(f"Geo {i['geo'][0]} & {i['geo'][1]}")
    print(f"epicenter {i['loc']}")
    print(f"felt {i['felt']}")


if __name__ == '__main__':
    show(data())
