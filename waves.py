import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np
import re
import requests

""" I made this project to learn web scraping. This is my first project using BeautifulSoup and I plan on optimizing
my code as I continue to learn the software."""

tmp_url = "https://www.surfline.com/surf-report/terra-mar-point/5842041f4e65fad6a77088a6"
oside_pier_south_url = "https://www.surfline.com/surf-report/oceanside-pier-southside/584204204e65fad6a7709435"
oside_pier_north_url = "https://www.surfline.com/surf-report/oceanside-pier-northside/5842041f4e65fad6a7708835"
oside_harbor_url = "https://www.surfline.com/surf-report/oceanside-harbor-north-jetty/5842041f4e65fad6a7708832"
grandview_url = "https://www.surfline.com/surf-report/grandview/5842041f4e65fad6a770889f"
seaside_reef_url = "https://www.surfline.com/surf-report/seaside-reef/5842041f4e65fad6a77088b3"
d_street_url = "https://www.surfline.com/surf-report/d-street/5842041f4e65fad6a77088b7"
la_jolla_url = "https://www.surfline.com/surf-report/la-jolla-shores/5842041f4e65fad6a77088cc"
swamis_url = "https://www.surfline.com/surf-report/swami-s/5842041f4e65fad6a77088b4"
urls = [tmp_url, oside_harbor_url, oside_pier_north_url, oside_pier_south_url, swamis_url, grandview_url, d_street_url]

class Report:
    
    def __init__(self):
        self.waves = pd.DataFrame()
        
    def report_surf(self):
        # making rows for dataframe
        location = np.array([])
        condition = np.array([])
        height = np.array([])
        water_temp = np.array([])
        weather = np.array([])
        tide = np.array([])
        wind = np.array([])
        for url in urls:
            # Opening up connection, grabbing the page
            url_page = requests.get(url)
            # html parser
            url_soup = soup(url_page.text, "html.parser")
            # 'Terra Mar Point Surf'
            url_loc = url_soup.h1.text.replace(" Report & Forecast", "")
            # current conditions (i.e. top table on website)
            current_cond = url_soup.find("div", {"class": "sl-spot-report"})
            url_cond = current_cond.div.text.lower()
            # len(url_data) == 4
            url_data = url_soup.findAll("div", {"class": "sl-spot-forecast-summary__stat"})
            # takes current wave height
            pattern = '[0-9]+-[0-9]+FT'
            url_height = re.findall(pattern, url_data[0].text)[0].replace("FT", " FT")
            # takes current tide
            pattern = "[0-9].[0-9]+FT"
            url_tide = re.findall(pattern, url_data[1].text)[0].replace("FT", " FT")
            # takes wind speed
            pattern = '[0-9]+[A-Z]+'
            url_wind = re.findall(pattern, url_data[2].text)[0].replace("KTS", " ")
            # outside temp
            pattern = '[0-9]+ ºF'
            url_weather = url_soup.find("div", {"class":"sl-wetsuit-recommender__conditions__weather"}).text
            url_weather = re.findall(pattern, url_weather)[0]
            # use for water temp
            wetsuit = url_soup.find("div", {"class":"sl-wetsuit-recommender__conditions"})
            # water temp
            pattern = '[0-9]+ - [0-9]+ ºF'
            H20temp = re.findall(pattern, wetsuit.div.text)[0]
            # columns for DataFrame
            columns = np.array(["location", "condition", "wave height", "H20temp", "weather",  "tide", "wind"])
            # making rows for DataFrame
            location = np.append(location, url_loc)
            condition = np.append(condition, url_cond)
            height = np.append(height, url_height)
            water_temp = np.append(water_temp, H20temp)
            weather = np.append(weather, url_weather)
            # sunrise = np.array([1])
            # sunset = np.array([1])
            tide = np.append(tide, url_tide)
            wind = np.append(wind, url_wind)
        # making dataframe
        report = pd.DataFrame(columns = columns)
        report['location'] = location
        report['condition'] = condition
        report['wave height'] = height
        report['H20temp'] = water_temp
        report['weather'] = weather
        # report['sunrise'] = sunrise
        # report['sunset'] = sunset
        report['tide'] = tide
        report['wind'] = wind
        self.waves = report
        # return the DataFrame
        return report   
    
    def best(self):
        if self.waves.size == 0:
            return "Need to run .report_surf() first."
        if len(self.waves[self.waves['condition'] == 'fair']) > 0:
            # converts wind collumn to integers
            report['wind'] = np.array([int(re.findall(pattern, i)[0]) for i in report['wind']])
            # best location has lowest wind
            best_location = self.waves.sort_values('wind', ascending=True).iloc[0,0]
            return f"The best location is {best_location}."
        else:
            return "There is no good surf today."
           
print("'r.waves' will display the wave report")
print("'r.best() will show the best surf location (if any).")
print("loading...")
r = Report()
r.report_surf()
