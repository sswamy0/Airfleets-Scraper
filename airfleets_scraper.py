import os
import logging
import time
import csv
from os import path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class AirfleetScraper:

    def __init__(self, quiet):
        self.selenium_driver_path = "Enter chromedriver.exe path here"
        self.browser = self._get_browser(quiet)
        self.requests_number = 0
        self.logger = self._setup_logger()

    def _setup_logger(self):
        project_base_path = path.dirname(path.dirname(path.abspath(__file__)))
        log_directory = f'{project_base_path}{path.sep}log'
        
        # Ensure the 'log' directory exists
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)  # Create the directory if it doesn't exist
        
        # Define the log file path
        log_name = f'{log_directory}{path.sep}scraper.log'
        
        # Configure the logger
        logging.basicConfig(filename=log_name, level=logging.WARNING)
        return logging.getLogger('scraper')

    def _get_browser(self, quiet):
        options = Options()
        if quiet:
            options.add_argument('--headless')  # Run headless if quiet mode is enabled
        service = Service(self.selenium_driver_path)
        return webdriver.Chrome(service=service, options=options)

    def _get_url_with_delay(self, url):
        if self.requests_number <= 264:
            self.browser.get(url)
            self.requests_number += 1
        else:
            print('Sleeping 5 minutes to avoid being banned due to "Too many requests"')
            time.sleep(300)  # Sleep for 5 minutes
            self.browser.get(url)
            self.requests_number = 1

        # Be nice to the server and add a delay between requests
        time.sleep(20)
        print(f'Request number: {self.requests_number}')
        
        # Get page source after the request
        page_source = self.browser.page_source
        print("Page source fetched successfully.")
        
        # Parse the page source using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all rows corresponding to the airplanes
        rows = soup.find_all('tr', class_='tabcontent2')
        
        # Extract information from each row
        plane_data = []
        for row in rows:
            cols = row.find_all('td')
            msn = cols[0].get_text(strip=True)
            ln = cols[1].get_text(strip=True)
            plane_type = cols[2].get_text(strip=True)
            airline = cols[3].get_text(strip=True)
            first_flight = cols[4].get_text(strip=True)
            registration = cols[5].get_text(strip=True)
            status = cols[6].get_text(strip=True)
            
            plane_data.append([msn, ln, plane_type, airline, first_flight, registration, status])

        return plane_data  # Return the plane data

    def scrape_airfleet(self, target_url, plane):
        print(f"Fetching data from {target_url}")
        plane_data = self._get_url_with_delay(target_url)

        # Append to a CSV file based on the plane
        csv_file = f"airfleet_data_{plane}.csv"
        file_exists = os.path.isfile(csv_file)

        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header only if the file is new
            if not file_exists:
                writer.writerow(['MSN', 'LN', 'Type', 'Airline', 'First Flight', 'Registration', 'Status'])
            # Write the data rows
            writer.writerows(plane_data)
        
        print(f"Data successfully written to {csv_file}")

    def close_browser(self):
        self.browser.quit()