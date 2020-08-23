''' Scrapes https://www.almanac.com/gardening/planting-calendar for gardening info '''

import requests
from bs4 import BeautifulSoup
from flask_login import current_user
from datetime import date
from dateutil.parser import parse

class Scraping:

    # plants_times is a list of plants along with all their start times
    # returns a list of plants (strings) that can be planted now 
    # NOTE: This is the function whose results you want to use in the suggestions
    # also NOTE: plants_times input should be the output from scrape_tables (below)
    def find_range(plants_times):
        messages_to_print = []
        today = date.today()
        for item in plants_times:
            plant_name = item[0]
            seeds_indoors = Scraping.parse_date(item[1])
            seedlings_outdoors = Scraping.parse_date(item[2])
            seeds_outdoors = Scraping.parse_date(item[3])

            if seeds_indoors != "N/A" and (today - seeds_indoors).days <= 15:
                message = "You can start " + plant_name + " seeds indoors by " + seeds_indoors.strftime("%B %d") + "."
                messages_to_print.append(message)
            
            elif seeds_outdoors != "N/A" and (today - seeds_outdoors).days <= 15:
                message = "You can start " + plant_name + " seeds outdoors by " + seeds_outdoors.strftime("%B %d") + "."
                messages_to_print.append(message)

            if len(messages_to_print) == 0:
                messages_to_print.append("It's currently not a suitable time to start planting in your area. Check back another day for more suggestions!")

        return messages_to_print


    # This function establishes a connection to the website and scrapes the data from it
    # zipcode argument should be the logged-in user's zipcode
    # this function assumes that zipcode is a string - it needs to be a string for the function to work
    # if the zipcode is currently not a string, make sure to convert it to a string before inputting it into this
    def scrape_tables(zipcode):
        plant_text = []
        times_parsed = []
        plant_groups = []

        URL = 'https://www.almanac.com/gardening/planting-calendar/zipcode/' + zipcode
        req = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = req.text

        soup = BeautifulSoup(webpage, 'html.parser')
        plants = soup.findAll("tr", class_="plantrow")
        for plant in plants:
            plant_text.append(plant.find("a").text)
        start_times = soup.findAll("td")

        for time in start_times:
            times_parsed.append(time.text)

        for i in range(len(times_parsed) // 3):
            plant_groups.append((plant_text[i], times_parsed[3*i], times_parsed[3*i + 1], times_parsed[3*i + 2]))

        return plant_groups


    # parses the dates scraped from the website into datetime objects
    def parse_date(datestr):
        if datestr == "N/A":
            return datestr

        if "-" in datestr:
            dash_index = datestr.index("-")
            if datestr[dash_index+1].isdigit() is False:
                datestr = datestr[dash_index+1:dash_index+8]
            else:
                datestr = datestr[0:dash_index-2] + datestr[dash_index+1:dash_index+3]

        return parse(datestr).date()
