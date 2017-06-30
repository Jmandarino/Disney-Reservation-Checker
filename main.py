# python 3.5

from twilio.rest import TwilioRestClient
from twilio.rest.resources import Connection
from twilio.rest.resources.connection import PROXY_TYPE_SOCKS4
from twilio.rest.resources.connection import PROXY_TYPE_HTTP


from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import os

account_sid  = None
auth_token = None
twilio_number = None
to_number = None


date_day = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May",
            "06":"June", "07":"July", "08":"August", "09":"September", "10":"October",
            "11": "November", "12":"December"}

class Alert:
    def __init__(self, restaurant_name, date, times = []):
        self.restaurant_name = restaurant_name
        self.times = []
        self.date =





class Reservation:
    def __init__(self, time, date, party):
        self.time = time
        self.party = party
        self.date = date



class Restaurant:
    def __init__(self, name, link,  reservations = []):
        self.name = name
        self.reservations = reservations
        self.link = link



def get_settings():

    if os.path.isfile("account.json"):
        json_data = open("account.json").read()
        data = json.loads(json_data)
    else:
        Exception("No 'account.json' file found")


    if data["to_phone_number"]:
        global to_number
        to_number = data["to_phone_number"]

    if data['account_sid'] and data['auth_token'] and data['twilio_number']:
        global account_sid
        global auth_token
        global twilio_number
        account_sid = data['account_sid']
        auth_token = data['auth_token']
        twilio_number = data['twilio_number']
    else:
        Exception("Missing Arguments in 'account.json,' please include account_sid, auth_token, and twilio_number")

def json_to_object(json):


def get_availibility(r_list, driver):
    # get restraunt
    for x in r_list:
        # get reservation
        for y in x.reservations:

            driver.get(x.link)
            # get day and date as numbers
            arr = y.date.split('/')
            # turn numeric date to text
            month = date_day[arr[0]]
            day = arr[1]
            # open the calender
            elm = driver.find_element(By.XPATH, '//*[@id="diningAvailabilityForm-searchDateid-base"]/div/button')
            elm.click()
            # get the month at the top of the calender
            elm = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/span[1]')
            # until we have the correct month we click the next month
            while(elm.text.lower() != month.lower()):
                elm = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/a[2]')
                elm.click()
                elm = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/span[1]')

            elements = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody')

            for dates in elements:
                # needs to be tested
                if dates.is_enabled() and str(dates.get_attribute("a")):
                    print("hi")













if __name__ == "__main__":
    # stores list of restaurants
    restaurant_list = []

    # get restaurants
    # process in file
    infile = open("places.json", "r")

    data = json.load(infile)

    #parse data and convert to objects
    for x in data["places"]:
        name = x["name"]
        link = x["link"]
        # stores temp list of reservations
        reservation_list = []

        for y in x["reservations"]:
            time = y["time"]
            date = y["date"]
            party= y["party"]

            reservation_list.append(Reservation(time, date, party))

        restaurant_list.append(Reservation(name, link, restaurant_list))

    #close file
    infile.close()

    #print(data)

    driver = webdriver.Chrome()

