# Disney-Reservation-Checker
Checks for reservation availability for Walt Disney World restaurants

### Purpose

When booking a vacation at Walt Disney World you can reserve a table up to 180 days in advanced. Some of the more desireable
 restraunts will be booked the full 6 months in advanced. This program aims Text the user when a reservation is found by constantly 
 checking for new reservations. 
 
 
 ### How it works
 
 This Python program leverages Selenium to check a list of restaurants and reservations you want to make every 5 minutes by
 spawning a copy of a ChromeDriver and using Disney's website to check for a reservation. The website is then processed and 
 if a reservation if found the user will receive a text with the available times. 
 
 #### Technologies used
 
 * Twilio Api (to text the user)
 * Python 3.x
 * Selenium (for website scripting automation)
 
 
 ## Getting Started
 
 To get started you must install the dependencies:
 * Twilio
 * Selenium
 
 Install via pip: `pip install twilio` & `pip install selenium`
 
 If you are on OSX you should install chrome driver via brew. `brew install chromedriver`. Windows Users should be able
  to use the chromedriver provided. 

 
 ##### Required Files:
 
 This program requires you to have both `accounts.json` & `places.json`
 
 I have included an example of `places.json`. The reservation you want to make is going to be stored in this file. Here is an example:
 
 
 ```json
 {
	"places": [{
		"name": "Ohana",
		"link": "https://disneyworld.disney.go.com/dining/polynesian-resort/ohana/",

		"reservations": [{
				"time": "7:00pm",
				"date": "08/27/17",
                "party":"2"
			}
		]
	},
      {
		"name": "50's prime",
		  "link": "https://disneyworld.disney.go.com/dining/hollywood-studios/50s-prime-time-cafe/",
		"reservations": [{
				"time": "7:00 pm",
				"date": "12/18/17",
                "party":"2"
		},
		 {
		 "time": "8:00pm",
		  "date": "01/01/17",
		  "party":"3"
		
		}]
		
	}
    ]
}
 
```

 The name of the restaurant is what you will be text back so the value doesn't matter. The link to the restaurant must be the one 
 that disney provides. Reservations require a time, date and party. They also must be in a specifc form.
 
 
 **Time**: the format must be the follow: HH:MM pm or HH:MM am ex: "07:30 am". Times go by 30 minute increments, eg. 7:25 
 pm is **NOT** valid. The period must be in lower case
 
 **Date**: the format must be DD/MM/YY eg. 01/01/17
 
 **Party**: A reservation can be in the range of 1-49
 
 
 `accounts.json` is used to text via your Twilio account. you must sign up for your own account which is free. All 
 information must be filled in. 
  
  
  ```json
  {
  "account_sid": "",
  "auth_token":"",
  "twilio_number":"+11234567890",
  "to_phone_number": ["+1234567890","+1234567890"]
 }


```

**account_sid** & **auth_token**: The SID and token can be found at the [Twilio Console](https://www.twilio.com/console)

**twilio_number**: To obtain a twilio number follow this [link](https://www.twilio.com/console/phone-numbers/getting-started)

**to_phone_number**: Must be a *Verified* number on your twilio account. Please follow the directions to verify 
your phone number. This program now supports multiple phone numbers as an array input. 
[here](https://www.twilio.com/console/phone-numbers/verified)


 
 
 