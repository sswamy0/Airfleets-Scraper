# Airfleets-Scraper
A Python web scraper for airfleets.net. Extracts all data from selected aircraft types. You will need to download a ChromeDriver that matches your current version of Chrome from here https://developer.chrome.com/docs/chromedriver/downloads.


You will need to complete a captcha for each page of the production list of the aircraft you have selected. If you end up in a captcha loop just enter the link into your browser and complete the captcha there and run the scraper again. I could not get past the captcha loop when trying to implement pagination so this the best I got. You should adjust the delay between requests as needed.
