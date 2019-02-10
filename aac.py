'''
Created by: Brittany Swanson
Contact info: brittanyjswanson@gmail.com

Program to scrape the Austin Animal Center's page for adoptable animals and add them to a MySQL database.

Last updated: 2/8/2019
Created: 2/1/2019

'''


import requests
import re
from time import time as time, sleep as sleep
from bs4 import BeautifulSoup

_animal_dict = dict()


#used in scrape_all_pages()
def get_page_count(page):
	#Create BeautifulSoup object
	soup = BeautifulSoup(page.text, 'html.parser')

	center_tags_list = soup.findAll('center')
	page_str = center_tags_list[1].get_text()

	num_pages = re.search(r'Page \d+ of (\d+)',page_str)


	if not num_pages:
		return 0

	return int(num_pages.group(1))



#used in find_sex() and find_age()
def split_by_sentences(description):
	#split string by sentences
	if description.count('.') > 1:
		sentences = description.split(".")
	else:
		sentences = description

	#remove empty items in list
	sentences = list(filter(None, sentences))

	#Loop through each item in the list and remove trailing and leading white space
	count = 0
	while count < len(sentences):
		sentences[count] = sentences[count].lstrip()
		sentences[count] = sentences[count].rstrip()
		count+=1

	return sentences


#used in find_sex() and find_age()
def narrow_to_specific_sentence(sentences,sentence_identifier):
	for line in sentences:
		if (line.find(sentence_identifier) != -1):
			return line


	return -1



#used in find_age()
def age_in_days(num_str, matched_keyword, age_keywords):
	#convert num_str to number
	if num_str.isdigit():
		age_number = int(num_str)
	else:
		return "Error converting string to int in age_in_days() function."

	age_days = age_number * age_keywords[matched_keyword]

	return age_days



#used in process_page()
def find_age(description):
	animal_age = 0
	sentences = split_by_sentences(description)
	age_line = narrow_to_specific_sentence(sentences, "old")
	words_in_age_sentence = age_line.split()

	age_keywords = {
				"years": 365,
				"year": 365, 
				"months": 30, 
				"month": 30, 
				"weeks": 7, 
				"week": 7, 
				"days": 1, 
				"day": 1
				}

	for word in age_keywords:

		if word in words_in_age_sentence:
			age_keyword_location = words_in_age_sentence.index(word)
		else:
			age_keyword_location = -1


		if (age_keyword_location != -1):
			# age_keyword was identified.  Grab previous word.
			animal_age += age_in_days(words_in_age_sentence[age_keyword_location-1], word, age_keywords)

	return animal_age



#used in process_page()
def find_sex(description):
	sentences = split_by_sentences(description)
	sex_line = narrow_to_specific_sentence(sentences, "female")

	if sex_line == -1:
		if narrow_to_specific_sentence(sentences, "male") == -1:
			return "unknown"
		else:
			return "male"
	elif sex_line.find("female") != -1:
		return "female"
	else:
		return "unknown"


#used in process_page()
def store_animal_in_dict(animal_id, age, sex, breed, location, days_in_shelter):

	templist = []

	templist.append(animal_id)
	templist.append(age)
	templist.append(sex)
	templist.append(breed)
	templist.append(location)
	templist.append(days_in_shelter)
	_animal_dict[animal_id] = templist




def process_page(page):
	#Create BeautifulSoup object
	soup = BeautifulSoup(page.text, 'html.parser')

	#Get <td> tags
	items = soup.findAll("td", {"class" : re.compile("TableContent*")})

	#Grab next 6 rows(td) and add to dictionary
	count = 0
	while (len(items) - count) / 6 >= 1:
		dog_id = items[count+1].get_text()
		description = items[count+2].get_text()


		age = find_age(description)
		sex = find_sex(description)
		#Need code for: altered/unaltered
		#Need code for: color
		#Need code for: name

		breed = items[count+3].get_text()
		location = items[count+4].get_text()
		days_in_shelter = items[count+5].get_text()

		store_animal_in_dict(dog_id, age, sex, breed, location, days_in_shelter)
		count+=6



#used by scrape_page()
def build_url(animal_type, page_index):
	base_url = 'http://petharbor.com/results.asp?searchtype=ADOPT&view=sysadm.v_austin&shelterlist=%27ASTN%27&where='

	# WHERE parameter
	if animal_type == "dog":
		where_parameters = "type_DOG"
	elif animal_type == "cat":
		where_parameters = "type_CAT"
	else:
		where_parameters = "type_OTHER"

	page_parameter = '&PAGE=' + str(page_index)

	page_URL = base_url + where_parameters + page_parameter

	return page_URL




#used by scrape_all_pages()
def scrape_page(animal_type, page_index):
	page_URL = build_url(animal_type, page_index)

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

	page = requests.get(page_URL,headers=headers)
	print(f"Scraped page {page_index}")
	return page




#used by main() and recursive
def scrape_all_pages(animal_type, page_index):
	page = scrape_page(animal_type, page_index)
	total_num_pages = get_page_count(page)

	process_page(page)

	if 0 < page_index < total_num_pages:
		sleep(2)
		scrape_all_pages(animal_type, page_index + 1)




#used by main()
def show_animals():
	for animal_id, animal in _animal_dict.items():
		print(animal_id, animal)




#used by main()
def begin_menu():
	print(30 * "-" + " MENU " + 30 * "-")
	print("1. Scrape AAC Dogs")
	print("2  View Dogs")
	print("10  Exit")
	print(67 * "-")




def main():
	loop = True

	while loop:
		begin_menu()
		choice = input("Choose an option: ")

		if choice=="1":
			scrape_all_pages("dog", 39)
		elif choice=="2":
			show_animals()
		elif choice=="10":
			print("You've chosen to exit.  Good-bye.")
			loop=False
		else:
			input("Wrong option selection. Press any key...")




if __name__ == "__main__":
	main()