'''
Created by: Brittany Swanson
Contact info: brittanyjswanson@gmail.com

Program to scrape the Austin Animal Center's page for adoptable animals and add them to a database.

Last updated: 2/3/2019
Created: 2/1/2019

'''
import requests
import re
from time import time as time, sleep as sleep
from bs4 import BeautifulSoup


class AACScraper:

    def __init__(self):
        self._animal_dict = dict()


    def scrape_for_dogs(self, animal_type, page_index):
        page = self.scrape_page(animal_type, page_index)
        num_pages = self.process_page(page)

        if 0 < page_index < num_pages:
            sleep(2)
            self.scrape_for_dogs(animal_type, page_index + 1)


    def scrape_page(self, animal_type, page_index):
        base_url = 'http://petharbor.com/results.asp?searchtype=ADOPT&view=sysadm.v_austin&shelterlist=%27ASTN%27&where='
        # WHERE parameter
        if animal_type == "dog":
            where_parameters = "type_DOG"
        elif animal_type == "cat":
            where_parameters = "type_CAT"
        else:
            where_parameters = "type_OTHER"

        page_parameter = '&PAGE=' + str(page_index)

        headers = {
            'Host': 'petharbor.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/71.0.3578.98 Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://www.austintexas.gov/adoptablepets',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9'
        }

        page_URL = base_url + where_parameters + page_parameter
        #print(f"Page URL is: {page_URL}")

        page = requests.get(page_URL, headers=headers)
        print(f"Scraped page {page_index}")
        return page


    def process_page(self, page):
        # Create BeautifulSoup object
        soup = BeautifulSoup(page.text, 'html.parser')

        # Get total pages
        num_pages = self.get_page_count(soup)

        #Get <td> tags
        items = soup.findAll("td", {"class": re.compile("TableContent*")})

        # Grab next 6 rows and add to dictionary
        count = 0
        while (len(items) - count) / 6 >= 1:
            dog_id = items[count+1].get_text()
            description = items[count+2].get_text()
            # age find_age(description)
            # sex
            # fixed
            # name
            breed = items[count+3].get_text()
            location = items[count+4].get_text()
            days_in_shelter = items[count+5].get_text()

            self.store_animal_in_dict(dog_id, description, breed, location, days_in_shelter)
            count += 6

        return num_pages


    '''
    get_page_count

    Finds the <center> tags in the input parameter and pulls out the string in the second <center> tag.
    String follows the format of: "Page ? of ?"

    Inputs:
        BeautifulSoup object

    Return: 
        int

    '''
    def get_page_count(self, soup):
        center_tags_list = soup.findAll('center')
        page_str = center_tags_list[1].get_text()
        print(page_str)

        num_pages = re.search(r'Page \d+ of (\d+)', page_str)

        #print(f"Number of total pages is: {int(num_pages.group(1))}")

        if not num_pages:
            return 0

        return int(num_pages.group(1))


    '''
    store_animal_in_dict

    Takes 5 inputs and adds them to a dictionary using the first input as the key and the combination of all as the value (in list form).  Adds
    these values to the instance variable self._animal_dict[]

    Inputs:
        animal_id
        description
        breed
        location
        days_in_shelter

    Return: 
        None

    '''
    def store_animal_in_dict(self, animal_id, description, breed, location, days_in_shelter):
        templist = []

        templist.append(animal_id)
        templist.append(description)
        templist.append(breed)
        templist.append(location)
        templist.append(days_in_shelter)
        self._animal_dict[animal_id] = templist


    def show_animals(self):
        for animal_id, animal in self._animal_dict.items():
            print(animal_id, animal)


    '''
    begin_menu

    Draws the options on the console.

    Inputs
        None

    Returns:
        None

    '''
    def begin_menu(self):
        print(30 * "-" + " MENU " + 30 * "-")
        print("1. Scrape AAC Dogs")
        print("2  View Dogs")
        print("3  Run Tests")
        print("10  Exit")
        print(67 * "-")


    '''
            TESTING FUNCTIONS
    '''
    def tests_main(self):
        scraper = AACScraper()
        scraper.begin_menu()
        user_response = input("Did the menu display on the page correctly? Y or N")
    
        if user_response == "N":
            print("FAILED - begin_menu()")
        else:
            print("PASSED - begin_menu()")
    
        scraper.find_age("My name is Lola.I am a white and tricolor . I am about 2 years old.")


    def find_age(self, description):
        sentences = description.split(".")
        sentences = list(filter(None, sentences))

        count = 0
        while count < len(sentences):
            sentences[count] = sentences[count].lstrip()
            sentences[count] = sentences[count].rstrip()
            count += 1


'''
main

Drives the menu selection process.

Functions called:
    scrape_for_dogs()

'''
def main():
    scraper = AACScraper()
    loop = True
    
    while loop:
        scraper.begin_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            print("Scraping for AAC dogs...")
            scraper.scrape_for_dogs("dog", 34)
        elif choice == "2":
            print("Viewing dogs.")
            scraper.show_animals()
        elif choice == "3":
            print("Running tests.")
            scraper.tests_main()
        elif choice == "10":
            print("You've chosen to exit.  Good-bye.")
            loop = False
        else:
            input("Wrong option selection. Press any key...")


if __name__ == "__main__":
    main()


'''
    store_animal_in_dict("A0000001", "Description of an animal here.", "animal breed", "in foster", "001 days")
    print(self._animal_dict)

    #Mock up a soup object

    get_page_count(soup)
    

    test_string = 'Page 1 of 9'
    num_pages = get_page_count(test_string)

    print(num_pages)
    '''
