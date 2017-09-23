import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import string

def make_soup(url):
    page = urlopen(url)
    soupdata = BeautifulSoup(page, 'html.parser')
    return soupdata
base_url = 'http://www.rlpgta.ca/our-realtors%C2%AE?pageFilter='
l = []
for num in string.ascii_uppercase:
    soup = make_soup(base_url+str(num))
    for i in soup.find_all('div',attrs={'class':'agentInfo'}):
         link = i.find('a').get('href')
         newlink = str(link).replace('®','%C2%AE')
         l.append(newlink)
print(len(l))
contact_list = []
for url in l:
    contact_info = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    for i in soup.find_all("div", attrs={"class":"agentName"}):
        if i.text is None or i.text == "":
            contact_info.append('None')
        else:
            name = i.text.split('\n')[1]
            contact_info.append(name)
    for n in soup.find_all("a", attrs={"class":"whiteLink agentInfo__email"}):
        if n.text is None or n.text == "":
            contact_info.append('None')
        else:
            contact_info.append(n.text)
    for u in soup.find_all("span", attrs={"class":"agentInfo__contactInfo"}):
        if u.text is None or u.text == "":
            contact_info.append('None')
        else:
            contact_info.append(u.text)
    contact_list.append(contact_info)
with open("output.csv", "w") as f:
    writer = csv.writer(f, delimiter=',',lineterminator='\n' )
    writer.writerows(contact_list)

