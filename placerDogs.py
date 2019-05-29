import requests
from bs4 import BeautifulSoup
import re
import json
import datetime
from dateutil.parser import parse

def main():
    dog_entry = []
    placerSpca(dog_entry)
    placerAuburn(dog_entry)
    sacSPCA(dog_entry)
    sacShelter(dog_entry)
    #yoloSPCA(dog_entry) #foster based organization + application
    print json.dumps(dog_entry)

def handleDate(unformatted_date):
    dt = parse(unformatted_date)
    date = "{:%Y-%m-%d}".format(dt)
    #print date
    return date

def placerSpca(dog_entry):
    placer_dogs = 'http://placerspca.org/adopt-home/dogs/#RosevilleDogs'

    page = requests.get(placer_dogs)

    soup = BeautifulSoup(page.text, 'html.parser')

    iframe= soup.find('iframe')
    #print iframe
    iframe_src = (iframe.attrs['src'])
    #print iframe_src

    dog_page = requests.get(iframe_src)
    dog_soup = BeautifulSoup(dog_page.text, 'html.parser')

    dog_td = dog_soup.findAll('td', attrs = {'class': 'list-item'})

    for dog_block in dog_td:
        dog_specific_url = "http://ws.petango.com/webservices/adoptablesearch/" + (dog_block.find('a')).get('href')
        dog_specific_page = requests.get(dog_specific_url)
        dog_specific_soup = BeautifulSoup(dog_specific_page.text, 'html.parser')
        #print dog_specific_url
        dog_image = dog_specific_soup.find('img', attrs = {'id': 'imgAnimalPhoto'})
        dog_image = dog_image.attrs['src']
        dog_image = dog_image.strip('//')
        #print dog_image

        #store dog info to return to javascript
        table_log = {'doggo': dog_image}

        # info
        dog_info_block = dog_block.find('div', attrs = {'class': 'list-animal-info-block'})
        regex = re.compile('list-anima.*')
        dog_infos = dog_info_block.findAll('div', attrs = {'class': regex})
        for dog_info in dog_infos:
            #print dog_info['class']
            info_type = dog_info['class'][0].split('-')[-1]
            #print info_type
            info = dog_info.get_text()
            #print info
            table_log[info_type] = info
            #print table_log
        dog_intake = (dog_specific_soup.find('span', {'id' : 'lblIntakeDate'})).text
        dog_intake = handleDate(dog_intake)
        table_log["intake"] = dog_intake
        table_log["dogLink"] = dog_specific_url
        table_log["shelter"] = "Roseville Placer SPCA"
        dog_entry.append(table_log)

def placerAuburn(dog_entry):

    placer_dogs = 'https://www.placer.ca.gov/1912/Adoptable-Dogs'

    page = requests.get(placer_dogs)
    soup = BeautifulSoup(page.text, 'html.parser')

    iframe= soup.find('iframe')
    #print iframe
    iframe_src = (iframe.attrs['src'])
    #print iframe_src

    dog_page = requests.get(iframe_src)
    dog_soup = BeautifulSoup(dog_page.text, 'html.parser')

    dog_frames = dog_soup.findAll('div', attrs = {'class': 'gridResult'})
    #print dog_frames

    for dog_block in dog_frames:
        dog_item = dog_block.find('a')
        dog_item = dog_item.get('href')
        #print dog_item
        dog_item = "https://petharbor.com/" + dog_item
        item_page = requests.get(dog_item)
        item_soup = BeautifulSoup(item_page.text, 'html.parser')
        item_block = item_soup.find('table', attrs = {'class': 'DetailTable'})
        #print item_block
        unform_date = (item_block.find('td', attrs = {'class' : 'DetailDesc'})).text
        unform_date = re.findall(r"\w+\s\d{1,2},\s\d{4}",unform_date)
        #print unform_date[0]
        dog_intake = handleDate(unform_date[0])
        item_img = "petharbor.com/" + (item_block.find('img')).attrs['src']
        #print item_img
        table_log = {'doggo': item_img}

        dog_text = dog_block.findAll('div', attrs = {'class': 'gridText'})
        #print dog_text
        #for text in dog_text:
            #print(text.get_text())
        dog_name = dog_text[0].get_text()
        table_log["name"] = dog_name
        #print dog_name
        dog_sex = dog_text[1].get_text()
        table_log["sexSN"] = dog_sex
        dog_breed = dog_text[2].get_text()
        table_log["breed"] = dog_breed
        dog_age = dog_text[3].get_text()
        table_log["age"] = dog_age
        #dog_intake = (dog_text[-1].get_text())[3:]
        table_log["intake"] = dog_intake
        table_log["dogLink"] = dog_item
        table_log["shelter"] = "Auburn Placer"
        dog_entry.append(table_log)

def sacSPCA(dog_entry):

    spca_dogs = 'https://www.sspca.org/dogs'

    page = requests.get(spca_dogs)
    soup = BeautifulSoup(page.text, 'html.parser')

    iframe= soup.find('iframe')
    #print iframe
    iframe_src = (iframe.attrs['src'])
    #print iframe_src

    dog_page = requests.get(iframe_src)
    dog_soup = BeautifulSoup(dog_page.text, 'html.parser')

    dog_frames = dog_soup.findAll('td', attrs = {'class': 'list-item'})
    #print dog_frames

    for dog_frame in dog_frames:
        dog_url = (dog_frame.find('a')).get('href')
        dog_url = "https://ws.petango.com/webservices/adoptablesearch/" + (dog_url.split('\'')[1])
        #print dog_url
        dog_item = requests.get(dog_url)
        dog_block = BeautifulSoup(dog_item.text, 'html.parser')
        dog_img = (dog_block.find('img', attrs = {'id' : 'imgAnimalPhoto'})).attrs['src']
        #print dog_img
        table_log = {'doggo': dog_img}
        dog_name = (dog_block.find('span', attrs = {'id' : 'lbName'})).text
        #print dog_name
        table_log["name"] = dog_name
        dog_breed = (dog_block.find('span', attrs = {'id' : 'lbBreed'})).text
        #print dog_breed
        table_log["breed"] = dog_breed
        dog_gender = (dog_block.find('span', attrs = {'id' : 'lbSex'})).text
        #print dog_gender
        table_log["sexSN"] = dog_gender
        dog_age = (dog_block.find('span', attrs = {'id' : 'lbAge'})).text
        #print dog_age
        table_log["age"] = dog_age
        dog_intake = (dog_block.find('span', attrs = {'id' : 'lblIntakeDate'})).text
        dog_intake = handleDate(dog_intake)
        table_log["intake"] = dog_intake
        table_log["dogLink"] = dog_url
        table_log["shelter"] = "Sacramento SPCA"
        #print dog_intake
        dog_entry.append(table_log)

def sacShelter(dog_entry):
    #http://www.cityofsacramento.org/Community-Development/Animal-Care/Adoptions

    shelter_dogs = 'http://petharbor.com/results.asp?searchtype=ADOPT&start=4&nopod=1&grid=1&friends=0&samaritans=1&nosuccess=1&orderby=Intake%20Date&rows=96&imght=120&imgres=detail&tWidth=400&view=sysadm.v_scrm_adopt_shelter&nobreedreq=1&nocustom=1&bgcolor=192845&text=ffffff&link=ffffff&alink=ffffff&vlink=ffffff&fontface=arial&fontsize=13&col_bg=4994d0&miles=20&shelterlist=%27scrm%27&atype=&where=type_DOG&PAGE=1'

    page = requests.get(shelter_dogs)
    soup = BeautifulSoup(page.text, 'html.parser')

    dog_grids = soup.findAll('div', attrs = {'class' : 'gridResult'})

    for dog_grid in dog_grids:
        dog_link = 'https://petharbor.com/' + (dog_grid.find('a')).get('href')
        #print dog_page
        dog_page = requests.get(dog_link)
        dog_soup = BeautifulSoup(dog_page.text, 'html.parser')
        #print dog_soup
        dog_table = dog_soup.find('table', {'class' : 'DetailTable'})
        dog_img = 'petharbor.com/' + (dog_table.find('img')).attrs['src']
        #print dog_img
        table_log = {'doggo': dog_img}
        dog_name = (dog_table.find('font', {'class' : 'Title'})).text
        #print dog_name
        dog_info = (dog_table.find('td', attrs = {'class' : 'DetailDesc'})).text
        #print dog_info
        dog_intake = handleDate((re.findall(r"\w+\s\d{1,2},\s\d{4}",dog_info))[0])
        #print intake_date
        table_log["name"] = dog_name
        table_log["intake"] = dog_intake
        table_log["dogLink"] = dog_link
        table_log["shelter"] = "Sacramento Front Street Animal Shelter"
        dog_entry.append(table_log)

def yoloSPCA(dog_entry):
    yoloSPCA = "http://yolospca.org/adopt/view-adoptable-animals"

    page = requests.get(yoloSPCA)
    soup = BeautifulSoup(page.text, 'html.parser')

    iframe = soup.find('iframe')
    iframe_src = iframe.attrs["src"] + "Dog"
    #print iframe_src

    dog_page = requests.get(iframe_src)
    dog_soup = BeautifulSoup(dog_page.text, 'html.parser')

    dog_frames = dog_soup.findAll('td', attrs = {'class': 'searchResultsCell'})

    for dog_frame in dog_frames:
        dog_url = "https://toolkit.rescuegroups.org/iframe/fb/v1.0/" + (dog_frame.find('a')).get('href')
        #print dog_url
        dog_block = requests.get(dog_url)
        dog_info = BeautifulSoup(dog_block.text, 'html.parser')
        dog_img = dog_info.find('div', {'class' : 'rgPetDetailsLargePhoto'})
        dog_img = (dog_img.find('img')).attrs['src']
        #print dog_img
        table_log = {'doggo': dog_img[8:]}
        dog_name = (dog_info.find('div', {'class' : 'pageCenterTitle'})).text
        #print dog_name
        table_log["name"] = dog_name
        dog_breed = (dog_info.find('span', {'id' : 'rgPetDetailsBreed'})).text
        #print dog_breed
        table_log["breed"] = dog_breed
        dog_gender = (dog_info.find('span', {'id' : 'rgPetDetailsSex'})).text
        table_log["sexSN"] = (dog_gender[4:])
        dog_age = (dog_info.find('span', {'id' : 'rgPetDetailsAge'})).text
        table_log["age"] = (dog_age[4:])
        table_log["dogLink"] = dog_url
        table_log["shelter"] = "Yolo County SPCA"
        dog_entry.append(table_log)

main()
