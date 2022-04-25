#!/usr/bin/env python3

import pymongo
import pprint

# fetch database
def retrieveDB():
	# make request
	client = pymongo.MongoClient("mongodb://hsiaopat:Aerodynamicfeathers7@hsiaoer-of-pattys-shard-00-00.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-01.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-02.qdmrj.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-pyw8am-shard-0&authSource=admin&retryWrites=true&w=majority")
	# access database
	cseDB = client["cse_courses"]
	# access collection
	cseColl = cseDB["cse_collections"]

	return cseColl

# initialize dictionary to track taken courses
def initTaken(cseColl):
	takenDict = {}
	# iterate through database documents and update dictionary
	for doc in cseColl.find():
		number = doc["number"]
		takenDict.update({number:0})

	return takenDict

# update taken courses dictionary based on user input
def courseTakenSearch(cseColl, course, takenDict):
	# iterate through database
	for doc in cseColl.find():
		# search for user's course in course number/title and update if found
		if course.lower() in doc["title"].lower() and doc["number"] in takenDict:
			takenDict[doc["number"]] = 1
		elif course in doc["number"] and doc["number"] in takenDict:
			takenDict[doc["number"]] = 1

	return takenDict

# search for keywork in course entries
def searchKeyword(keyword, cseColl, foundKeyword):
	# iterate through database
	for doc in cseColl.find():
		# check if course is already in list
		if doc in foundKeyword:
			pass
		# append if keyword is found in description/title/number
		elif keyword in doc["description"].lower() and doc["type"] == "Elective":
			foundKeyword.append(doc)
		elif keyword in doc["title"].lower() and doc["type"] == "Elective":
			foundKeyword.append(doc)
		elif keyword in doc["number"] and doc["type"] == "Elective":
			foundKeyword.append(doc)

	return foundKeyword

# cross check user's taken courses with prereqs of electives
def checkPrereq(foundKeyword, takenDict):
	availableElectives = []
	# iterate through list of electives with keyword(s)
	for course in foundKeyword:
		# check for prereqs attribute
		try:
			available = False
			# iterate through prereqs
			for prereq in course["prerequisites"]:
				# check element class
				# if the element is a single string, it is a required prereq
				# (i.e., the case of XX and YY non-optionally)
				if isinstance(prereq, str):
					if takenDict[prereq] == 1:
						available = True
				# if the element is not a single string, it must be a list
				# of strings (i.e., the case of XX or YY optionally)
				else:
					for orPrereq in prereq:
						if takenDict[orPrereq] == 1:
							available = True
							break
			# append elective if user meets prereqs
			if available:
				availableElectives.append(course)
		# if no prereq attribute, append elective
		except KeyError:
			availableElectives.append(course)

	return availableElectives


def main():
	# retrieve database of course entries
	cseColl = retrieveDB()

	# create dictionary for taken courses
	takenDict = initTaken(cseColl)
	takenCourses = "20289, 20221, Data Science, CSE Service Projects" # test string
	takenCourses = takenCourses.split(",")
	for course in takenCourses:
		course = course.strip()
		takenDict = courseTakenSearch(cseColl, course, takenDict)

	# REMOVE
	#pprint.pprint(takenDict)
	#print(len(takenDict))

	# search for keywords
	keywords = "machine learning, 30125, database" # test string
	keywords = keywords.split(",")
	foundKeyword = []
	for key in keywords:
		key = key.strip()
		foundKeyword = searchKeyword(key, cseColl, foundKeyword)

	# REMOVE
	#for course in foundKeyword:
	#	print(f'{course["title"]}')

	#print('')
	# check prereqs of found electives
	availableElectives = checkPrereq(foundKeyword, takenDict)
	for course in availableElectives:
		print(f'{course["title"]}')


if __name__ == '__main__':
	main()
