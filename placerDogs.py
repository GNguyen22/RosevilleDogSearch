import requests
from bs4 import BeautifulSoup
import re
import json
import datetime
from dateutil.parser import parse
import logging

def main():
    dog_entry = []
    logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            filename='logs/placerDogs.log',
            level=logging.ERROR,
            datefmt='%Y-%m-%d %H:%M:%S')
    try:
        placerSpca(dog_entry)
    except:
        logging.exception('')
        pass
    try:
        placerAuburn(dog_entry)
    except:
        logging.exception('')
        pass
    try:
        sacSPCA(dog_entry)
    except:
        logging.exception('')
        pass
    try:
        sacShelter(dog_entry)
    except:
        logging.exception('')
        pass
    #yoloSPCA(dog_entry) #foster based organization + application
    try:
        sacBradshawShelter(dog_entry)
    except:
        logging.exception('')
        pass
    normalizeInput(dog_entry)
    print json.dumps(dog_entry)

#currently only accounts for dog image URLs
def normalizeInput(dog_entry):
    for dog in dog_entry:
        dog["doggo"] = dog["doggo"].replace('https://', '')

def handleDate(unformatted_date):
    dt = parse(unformatted_date)
    date = "{:%Y-%m-%d}".format(dt)
    #print date
    return date

def placerSpca(dog_entry):
    placer_dogs = 'https://placerspca.org/adopt-home/dogs/#RosevilleDogs'

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
        #print dog_block
        if (dog_block.find('a')) is None:
            continue
        dog_specific_url = "https://ws.petango.com/webservices/adoptablesearch/" + (dog_block.find('a')).get('href')
        dog_specific_page = requests.get(dog_specific_url)
        dog_specific_soup = BeautifulSoup(dog_specific_page.text, 'html.parser')
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
        dog_item = "https://petharbor.com/" + dog_item
        #print dog_item
        item_page = requests.get(dog_item)
        item_soup = BeautifulSoup(item_page.text, 'html.parser')
        item_block = item_soup.find('table', attrs = {'class': 'DetailTable'})
        #print item_block.text
        unform_date = (item_block.find('td', attrs = {'class' : 'DetailDesc'})).text
        unform_date = re.findall(r"\w+\s\d{1,2},\s\d{4}",unform_date)
        #print unform_date[0]
        if re.findall("I have been adopted", item_block.text):
            pass
        else:
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
            dog_intake = handleDate(unform_date[0])
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

    shelter_dogs = 'https://petharbor.com/results.asp?searchtype=ADOPT&start=4&nopod=1&grid=1&friends=0&samaritans=1&nosuccess=1&orderby=Intake%20Date&rows=96&imght=120&imgres=detail&tWidth=400&view=sysadm.v_scrm_adopt_shelter&nobreedreq=1&nocustom=1&bgcolor=192845&text=ffffff&link=ffffff&alink=ffffff&vlink=ffffff&fontface=arial&fontsize=13&col_bg=4994d0&miles=20&shelterlist=%27scrm%27&atype=&where=type_DOG&PAGE=1'

    page = requests.get(shelter_dogs)
    soup = BeautifulSoup(page.text, 'html.parser')

    dog_grids = soup.findAll('div', attrs = {'class' : 'gridResult'})

    for dog_grid in dog_grids:
        dog_link = 'https://petharbor.com/' + (dog_grid.find('a')).get('href')
        #print dog_page
        dog_page = requests.get(dog_link)
        # ** had to change parser to correctly parse invalid html '<b><u>NOT</b></u>' **
        dog_soup = BeautifulSoup(dog_page.text, 'html5lib')  
        #print dog_soup
        dog_table = dog_soup.find('table', {'class' : 'DetailTable'})
        dog_img = 'petharbor.com/' + (dog_table.find('img')).attrs['src']
        #print dog_img
        table_log = {'doggo': dog_img}
        dog_name = (dog_table.find('font', {'class' : 'Title'})).text
        #print dog_name
        table_log["name"] = dog_name
        dog_info = (dog_table.find('td', attrs = {'class' : 'DetailDesc'})).text
        #print dog_info
        dog_breed = (re.findall(r"(?:male)\S*\s*(.+?)\.", dog_info))[0]
        #print dog_breed
        table_log["breed"] = dog_breed
        dog_gender = (re.findall(r'(?:fe)?male', dog_info))[0]
        #print dog_gender
        table_log["sexSN"] = dog_gender
        try:
            dog_age = re.findall(r"about\s(\d{1,2}\syears?(?: and \d{1,2} months)?)\sold", dog_info)[0].replace('and ', '')
        except:
            dog_age = 'Unknown'
        table_log["age"] = dog_age
        #print table_log['age']
        try:
            dog_intake = handleDate((re.findall(r"\w+\s\d{1,2},\s\d{4}",dog_info))[0])
        except:
            dog_intake = "NA"
        #print dog_intake
        table_log["intake"] = dog_intake
        table_log["dogLink"] = dog_link
        table_log["shelter"] = "Sacramento Front Street Animal Shelter"
        dog_entry.append(table_log)

def yoloSPCA(dog_entry):
    yoloSPCA = "https://yolospca.org/adopt/view-adoptable-animals"

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

def sacBradshawShelter(dog_entry):
    bradshawShelter = "https://animalcare.saccounty.net/Adoption/Pages/ViewAllAdoptableAnimals.aspx"

    page = requests.get(bradshawShelter)
    soup = BeautifulSoup(page.text, 'html.parser')

    dogUrl = (soup.find('a', text="View list of Adoptable Dogs")).get('href')
    dogUrl = dogUrl.replace("rows=10", "rows=100")
    #print dogUrl

    dog_req = requests.get(dogUrl)
    dog_soup = BeautifulSoup(dog_req.text, 'html.parser')

    dog_entries = dog_soup.findAll('tr', attrs = {'align' : 'CENTER'})

    for dog_item in dog_entries[1:]:
        #print dog_item.text
        if (re.findall("I am adopted", dog_item.text)):
            pass #print "skip"
        else:
            dog_specific_url = 'https://petharbor.com/' + (dog_item.find('a', attrs = {'alt' : 'Click on this picture to see more information about this animal'})).get('href')
            #print dog_specific_url
            dog_spec_page = requests.get(dog_specific_url)
            dog_spec_soup = BeautifulSoup(dog_spec_page.text, 'html.parser')

            dog_img = dog_spec_soup.find('td', attrs = {'align' : 'center'})
            dog_img = 'petharbor.com/' + (dog_img.find('img')).attrs['src']
            #print dog_img
            table_log = {'doggo': dog_img}
            #print "didn't skip"
            dog_name = (dog_spec_soup.find('font', {'class' : 'Title'})).text
            #print dog_name
            table_log["name"] = dog_name
            dog_info = (dog_spec_soup.find('td', attrs = {'class' : 'DetailDesc'})).text
            #print dog_info
            dog_breed = (re.findall(r"(?:male)\S*\s*(.+?)\.", dog_info))[0]
            #print dog_breed
            table_log["breed"] = dog_breed
            dog_gender = (re.findall(r'(?:fe)?male', dog_info))[0]
            #print dog_gender
            table_log["sexSN"] = dog_gender
            try:
                dog_age = re.findall(r"about\s(\d{1,2}\syears?(?: and \d{1,2} months)?)\sold", dog_info)[0].replace('and ', '')
            except:
                dog_age = 'Unknown'
            table_log["age"] = dog_age
            #print table_log['age']
            #dog_intake = handleDate((re.findall(r"\w+\s\d{1,2},\s\d{4}",dog_info))[0])
            dog_intake = (dog_item.text)[-10:]
            table_log["intake"] = dog_intake
            table_log["dogLink"] = dog_specific_url
            table_log["shelter"] = "Sacramento Bradshaw Shelter"
            dog_entry.append(table_log)


main()
