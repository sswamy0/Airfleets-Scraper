from airfleets_scraper import AirfleetScraper

def main():
    #You will need to find out how the plane/page is formatted in the url. You will also need to find how many pages of tables are there for your selected plane. 
    #You can do this by searching up your desired aircraft and "production list" and viewing the url of the airfleets.net result.
    #For example this is how all the Boeing aircraft should be represented: planes = {'b717': '4', 'b737': '63', 'b737ng': '177', 'b747': '32', 'b757': '21','b767': '27', 'b777': '35', 'b787': '24'}
    planes = {}

    base_url = 'https://www.airfleets.net/listing/'

    for plane, pages in planes.items():
        for page in range(1, int(pages) + 1):
            # Create a new instance of AirfleetScraper for each plane and page
            scraper = AirfleetScraper(quiet=False)  # Set quiet=True for headless mode
            
            url = f"{base_url}{plane}-{page}.htm"
            scraper.scrape_airfleet(url, plane)
            scraper.close_browser()  # Close the browser after scraping each page

if __name__ == "__main__":
    main()