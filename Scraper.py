from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

Start_URL = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"

browser = webdriver.Chrome("C:/Users/Lenovo/Downloads/chromedriver.exe")
browser.get(Start_URL)

time.sleep(10)
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", 
            "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
planet_data = []
new_planet_data = []

def scrape():
    for i in range(0, 453):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        
        for ultag in soup.find_all("ul", attrs = {"class", "exoplanet"}):
            litags = ultag.find_all("li")
            templist = []

            for index, litag in enumerate(litags):
                if index == 0:
                    templist.append(litag.find_all("a")[0].contents[0])
                else:
                    try:
                        templist.append(litag.contents[0])
                    except:
                        templist.append("")
            
            hyperlink_litag = litags[0]
            templist.append("https://exoplanets.nasa.gov" + hyperlink_litag.find_all("a", href=True)[0]["href"])
            planet_data.append(templist)
    
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i} Page Done 1")

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        templist = []

        for trtag in soup.find_all("tr", attrs={"class":"fact_row"}):
            tdtags = trtag.find_all("td")

            for tdtag in tdtags:
                try:
                    templist.append(tdtag.find_all("div", attrs={"class":"value"})[0].contents[0])
                except:
                    templist.append("")
        
        new_planet_data.append(templist)
    
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

scrape()

for index, data in enumerate(planet_data):
    scrape_more_data(data[5])
    print(f"{index + 1} Page Done 2")

finalplanetdata = []

for index, data in enumerate(planet_data):
    finalplanetdata.append(data + finalplanetdata[index])

file = open("final.csv", "w")
csvwriter = csv.writer(file)
csvwriter.writerow(headers)
csvwriter.writerows(finalplanetdata)