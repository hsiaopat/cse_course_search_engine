#!/usr/bin/env python3

import pymongo
import pprint

def retrieve_db():
	client = pymongo.MongoClient("mongodb://hsiaopat:Aerodynamicfeathers7@hsiaoer-of-pattys-shard-00-00.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-01.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-02.qdmrj.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-pyw8am-shard-0&authSource=admin&retryWrites=true&w=majority")
	cse_db = client["cse_courses"]
	cse_coll = cse_db["cse_collections"]
	return cse_coll

def initTaken(cse_coll): #create dictionary for required courses
	#go thru each hashmap in collection
	takenDict = {}
	for doc in cse_coll.find():
		number = doc["number"]
		takenDict.update({number:0})
	return takenDict

def courseTakenSearch(cse_coll, course, takenDict):#cse_coll is collection, classTaken is input String
	#loop thru collection
	for doc in cse_coll.find():
		#if classtaken is in dictionary, append the title to classtakenList, set taken value to 1 and then return classTakenList
		if course.lower() in doc["title"].lower() and doc["number"] in takenDict:
			takenDict[doc["number"]] = 1
		elif course in doc["number"] and doc["number"] in takenDict:
			takenDict[doc["number"]] = 1
	return takenDict

def search_keyword(keyword, cse_coll, found_keyword):

	for doc in cse_coll.find():
		if doc in found_keyword:
			pass
		elif keyword in doc["description"].lower() and doc["type"] == "Elective":
			found_keyword.append(doc)
		elif keyword in doc["title"].lower() and doc["type"] == "Elective":
			found_keyword.append(doc)
		elif keyword in doc["number"] and doc["type"] == "Elective":
			found_keyword.append(doc)

	return found_keyword

def checkPrereq(found_keyword, takenDict):

	availableElectives = []

	for course in found_keyword:
		try:
			available = True
			for prereq in course["prerequisites"]:
				if not isinstance(prereq, str):
					for orPrereq in prereq:
						if takenDict[orPrereq] == 0:
							available = False
				else:
					if takenDict[prereq] == 0:
						available = False

			if available:
				availableElectives.append(course)

		except KeyError:
			availableElectives.append(course)

	return availableElectives


def main():
	cse_coll = retrieve_db()

	takenDict = initTaken(cse_coll)
	takenCourses = "20289, 20221, Data Science, CSE Service Projects"
	takenCourses = takenCourses.split(",")
	for course in takenCourses:
		course = course.strip()
		takenDict = courseTakenSearch(cse_coll, course, takenDict)

	pprint.pprint(takenDict)
	print(len(takenDict))

	keywords = "machine learning, 30125, database"
	keywords = keywords.split(",")
	found_keyword = []
	for key in keywords:
		key = key.strip()
		found_keyword = search_keyword(key, cse_coll, found_keyword)

	for course in found_keyword:
		print(f'{course["title"]}')

	print('')
	availableElectives = checkPrereq(found_keyword, takenDict)
	for course in availableElectives:
		print(f'{course["title"]}')



if __name__ == '__main__':
	main()
