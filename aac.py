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

_animal_dict = dict()

'''
get_page_count

Finds the <center> tags in the input parameter and pulls out the string in the second <center> tag.
String follows the format of: "Page ? of ?"

Inputs:
	BeautifulSoup object

Return: 
	int

'''
def get_page_count(soup):
	center_tags_list = soup.findAll('center')
	page_str = center_tags_list[1].get_text()
	print(page_str)

	num_pages = re.search(r'Page \d+ of (\d+)',page_str)

	#print(f"Number of total pages is: {int(num_pages.group(1))}")

	if not num_pages:
		return 0

	return int(num_pages.group(1))


def find_age(description):
	sentences = description.split(".")
	sentences = list(filter(None, sentences))

	count = 0
	while count < len(sentences):
		sentences[count] = sentences[count].lstrip()
		sentences[count] = sentences[count].rstrip()
		count+=1




'''
store_animal_in_dict

Takes 5 inputs and adds them to a dictionary using the first input as the key and the combination of all as the value (in list form).  Adds
these values to the global _animal_dict[]

Inputs:
	animal_id
	description
	breed
	location
	days_in_shelter

Return: 
	None

'''
def store_animal_in_dict(animal_id, description, breed, location, days_in_shelter):

	templist = []

	templist.append(animal_id)
	templist.append(description)
	templist.append(breed)
	templist.append(location)
	templist.append(days_in_shelter)
	_animal_dict[animal_id] = templist


def process_page(page):
	#Create BeautifulSoup object
	soup = BeautifulSoup(page.text, 'html.parser')

	#Get total pages
	num_pages = get_page_count(soup)

	#Get <td> tags
	items = soup.findAll("td", {"class" : re.compile("TableContent*")})

	#Grab next 6 rows and add to dictionary
	count = 0
	while (len(items) - count) / 6 >= 1:
		dog_id = items[count+1].get_text()
		description = items[count+2].get_text()
		#age find_age(description)
		#sex
		#fixed
		#name
		breed = items[count+3].get_text()
		location = items[count+4].get_text()
		days_in_shelter = items[count+5].get_text()

		store_animal_in_dict(dog_id, description, breed, location, days_in_shelter)
		count+=6
	return num_pages



def scrape_page(animal_type, page_index):
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

	page = requests.get(page_URL,headers=headers)
	print(f"Scraped page {page_index}")
	return page



def show_animals():
	for animal_id, animal in _animal_dict.items():
		print(animal_id, animal)


def scrape_for_dogs(animal_type, page_index):
	
	page = scrape_page(animal_type, page_index)
	num_pages = process_page(page)

	if 0 < page_index < num_pages:
		sleep(2)
		scrape_for_dogs(animal_type, page_index + 1)



'''
begin_menu

Draws the options on the console.

Inputs
	None

Returns:
	None

'''
def begin_menu():
	print(30 * "-" + " MENU " + 30 * "-")
	print("1. Scrape AAC Dogs")
	print("2  View Dogs")
	print("3  Run Tests")
	print("10  Exit")
	print(67 * "-")


'''
		TESTING FUNCTIONS
'''
def tests_main():
	begin_menu()
	user_response = input("Did the menu display on the page correctly? Y or N")
	if user_response == "N":
		print("FAILED - begin_menu()")
	else:
		print("PASSED - begin_menu()")

	#Calling find_age()
	find_age("My name is Lola.I am a white and tricolor . I am about 2 years old.")

'''
main

Drives the menu selection process.

Functions called:
	scrape_for_dogs()

'''
def main():
	loop = True

	while loop:
		begin_menu()
		choice = input("Choose an option: ")

		if choice=="1":
			print("Scraping for AAC dogs...")
			scrape_for_dogs("dog", 34)
		elif choice=="2":
			print("Viewing dogs.")
			show_animals()
		elif choice=="3":
			print("Running tests.")
			tests_main()
		elif choice=="10":
			print("You've chosen to exit.  Good-bye.")
			loop=False
		else:
			input("Wrong option selection. Press any key...")


if __name__ == "__main__":
	main()





'''
	store_animal_in_dict("A0000001", "Description of an animal here.", "animal breed", "in foster", "001 days")
	print(_animal_dict)

	#Mock up a soup object

	get_page_count(soup)
	

	test_string = 'Page 1 of 9'
	num_pages = get_page_count(test_string)

	print(num_pages)
	'''