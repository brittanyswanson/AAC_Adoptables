from AAC_Adoptables.aac import *

# find_age()
def test_find_age_months_only():
	test_str = "'Shelter staff named me Millie.I am a black and white spayed female. I am about 10 months old.'"
	age = find_age(test_str)

	assert age == 300

def test_find_age_month_only():
	test_str = "'Shelter staff named me Millie.I am a black and white spayed female. I am about 10 month old.'"
	age = find_age(test_str)

	assert age == 300


def test_find_age_year_only():
	test_str = "'Shelter staff named me Millie.I am a black and white spayed female. I am about 1 year old.'"
	age = find_age(test_str)

	assert age == 365


def test_find_age_years_only():
	test_str = "'Shelter staff named me Millie.I am a black and white spayed female. I am about 1 years old.'"
	age = find_age(test_str)

	assert age == 365


def test_find_age_years_and_months():
	test_str = "'Shelter staff named me Millie.I am a black and white spayed female. I am about 3 years and 5 months old.'"
	age = find_age(test_str)

	assert age == 1245



def test_find_age_years_and_month():
	test_str = "'Shelter staff named me Millie.I am a black and white spayed female. I am about 3 years and 1 month old.'"
	age = find_age(test_str)

	assert age == 1125



# find_sex()
def test_find_sex_male():
	test_str = "'Shelter staff named me Millie.I am a black and white spayed male. I am about 3 years and 1 month old.'"
	sex = find_sex(test_str)

	assert sex == "male"


def test_find_sex_female():
	test_str = "'Shelter staff named me Millie.I am a black and white spayed female. I am about 3 years and 1 month old.'"
	sex = find_sex(test_str)

	assert sex == "female"


def test_find_sex_unknown():
	test_str = "'Shelter staff named me Millie.I am a black and white spayed. I am about 3 years and 1 month old.'"
	sex = find_sex(test_str)

	assert sex == "unknown"