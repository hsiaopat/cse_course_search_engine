import requests
import os
import sys
from flask import Flask, render_template, request
import pymongo

app = Flask(__name__)

# retrieve info from database
def retrieveDB():
	# make request
	client = pymongo.MongoClient("mongodb://hsiaopat:Aerodynamicfeathers7@hsiaoer-of-pattys-shard-00-00.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-01.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-02.qdmrj.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-pyw8am-shard-0&authSource=admin&retryWrites=true&w=majority")
	# access database
	cseDB = client["cse_courses"]
	# access collection
	cseColl = cseDB["cse_collections"]

	return cseColl


### REQUIRED COURSE OUTPUT ###

# create dictionary for required courses
def initRequired(cse_coll):
	requiredDict = {}
	# iterate through each hashmap in collection
	for doc in cse_coll.find():
		# append all titles with type required with a taken value of 0
		if doc["type"] == "Required":
			name = doc["title"]
			requiredDict.update({name:0})

	return requiredDict

# search through database for required courses listed in user input, update dictionary
def reqCourseTakenSearch(cse_coll, classTaken, requiredDict):
	# iterate through collection
	for doc in cse_coll.find():
		# if classtaken is in dictionary, append the title to classtakenList, set taken value to 1 and then return classTakenList
		if classTaken.lower() in doc["title"].lower() and doc["title"] in requiredDict:
			requiredDict[doc["title"]] = 1
		elif classTaken in doc["number"] and doc["title"] in requiredDict:
			requiredDict[doc["title"]] = 1

	return requiredDict


### ELECTIVE COURSE OUTPUT ###

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
			if available and takenDict[course["number"]] == 0:
				availableElectives.append(course)
		# if no prereq attribute, append elective
		except KeyError:
			if takenDict[course["number"]] == 0:
				availableElectives.append(course)

	return availableElectives


### CONNECT ALGORITHMS TO FLASK ###

# required course output
def findRequired(courseInput, cseColl, requiredDict):
	# update taken dictionary for required courses based on user input
	for course in courseInput:
		course = course.strip()
		if not course == "":
			requiredDict = reqCourseTakenSearch(cseColl, course, requiredDict)

	# create taken and remaining course lists based on updated dictionary
	requiredTaken = []
	requiredRemaining = []
	for course, taken in requiredDict.items():
		if taken:
			requiredTaken.append(course)
		else:
			requiredRemaining.append(course)

	return requiredTaken, requiredRemaining

# elective course input
def findElectives(courseInput, keywordInput, cseColl, takenDict):
	# update taken dictionary based on user input
	for course in courseInput:
		course = course.strip()
		takenDict = courseTakenSearch(cseColl, course, takenDict)

	# create list of dictionaries for courses that match with keyword input
	foundKeyword = []
	for key in keywordInput:
		key = key.strip()
		foundKeyword = searchKeyword(key, cseColl, foundKeyword)

	# check prereq requirements of found courses
	availableElectives = checkPrereq(foundKeyword, takenDict)

	# create electives course list
	electives = []
	for course in availableElectives:
		electives.append(course["title"])

	return electives

@app.route("/",methods=["POST","GET"])
def index():
	# retrieve database from Mongo
	cseColl = retrieveDB()

	# initialize dictionaries to track user's taken courses
	takenDict = initTaken(cseColl)
	requiredDict = initRequired(cseColl)

	# initialize empty lists for HTML output
	requiredTaken = []
	requiredRemaining = []
	electives = []

	# GET request is sent when html wants some information from python backend
	if request.method == "GET":
		return render_template("index.html", taken=requiredTaken, remaining=requiredRemaining, electivesAvailable=electives)

	# POST request is when the webpage is sending data to python backend
	if request.method == "POST":
		# user input for courses taken
		courseInput = request.form.get("courseInput")
		courseInput = courseInput.split(",")

		# user input for keyword search
		keywordInput = request.form.get("keywordInput")
		keywordInput = keywordInput.split(",")

		# call functions to create display lists
		requiredTaken, requiredRemaining = findRequired(courseInput, cseColl, requiredDict)
		electives = findElectives(courseInput, keywordInput, cseColl, takenDict)

	return render_template("index.html", taken=requiredTaken, remaining=requiredRemaining, electivesAvailable=electives)
