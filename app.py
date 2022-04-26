import requests
import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# retrieve info from database
def retrieve_db():
	# make request
	client = PyMongo(app,"mongodb://hsiaopat:Aerodynamicfeathers7@hsiaoer-of-pattys-shard-00-00.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-01.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-02.qdmrj.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-pyw8am-shard-0&authSource=admin&retryWrites=true&w=majority")
	client_db = client.db
	db = client_db["cse_courses"]
	# access database
	#db = client["cse_courses"]
	# access collection
	cse_coll = db

	return cse_coll
	#return jsonify([todo for todo in todos])



@app.route("/",methods=["POST","GET"])
# retrieve info from database
#def retrieve_db():
#	# make request
#	client = PyMongo(app,uri="mongodb://hsiaopat:Aerodynamicfeathers7@hsiaoer-of-pattys-shard-00-00.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-01.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-02.qdmrj.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-pyw8am-shard-0&authSource=admin&retryWrites=true&w=majority")
#	db = client.db
	# access database
	#cse_db = client["cse_courses"]
	# access collection
	#cse_coll = cse_db["cse_collections"]


#	#return cse_coll
#	todos = db.todos.find()
#	print(todos)
#	return jsonify([todo for todo in todos])

def index():

	cseColl = retrieve_db()
	print(cseColl)

	takenDict = initTaken(cseColl)
	print(takenDict)
	requiredTaken = initRequired(cseColl)
	electiveTaken = initElective(cseColl)
	requiredTaken = ["Fundamentals of Computing", "Discrete Math"]
	requiredRemaining = ["Discrete Math", "Logic Design"]
	electives = []

	if request.method == "GET": #GET request is sent when html wants some information from python backend
		return render_template("index.html", taken=requiredTaken, remaining=requiredRemaining, electivesAvailable=electives)

	if request.method == "POST": #POST request is when the webpage is sending data to python backend

		courseInput = request.form.get("courseInput")
		keywordInput = request.form.get("keywordInput")
		requiredTaken = reqCourseTakenSearch(cseColl, courseInput, requiredTaken)
		electives = findElectives(courseInput, keywordInput, cseColl, takenDict)

	return render_template("index.html", taken=requiredTaken, remaining=requiredRemaining, electivesAvailable=electives)


def findElectives(courseInput, keywordInput, cseColl, takenDict):

	courseInput = courseInput.split()
	for course in courseInput:
		course = course.strip()
		takenDict = courseTakenSearch(cseColl, course, takenDict)

	keywordInput = keywordInput.split(",")
	foundKeyword = []
	for key in keywordInput:
		key = key.strip()
		foundKeyword = searchKeyword(key, cseColl, foundKeyword)

	availableElectives = checkPrereq(foundKeyword, takenDict)
	electives = []
	for course in availableElectives:
		electives.append(course["title"])

	return electives



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

# create dictionary for required courses
def initRequired(cseColl):
	requiredDict = {}
	# iterate through each hashmap in collection
	for doc in cseColl.find():
		# append all titles with type required with a taken value of 0
		if doc["type"] == "Required":
			name = doc["title"]
			requiredDict.update({name:0})

	return requiredDict

# create dictionary for elective courses
def initElective(cseColl):
	electiveDict = {}
	# iterate through each hashmap in collection
	for doc in cseColl.find():
		# append all titles with type electives with a taken value of 0
		if doc["type"] == "Elective":
			name = doc["title"]
			electiveDict.update({name:0})

	return electiveDict

# search through database for required courses listed in user input, update dictionary
def reqCourseTakenSearch(cseColl, classTaken, requiredDict):
	count = 0
	# iterate through collection
	for doc in cseColl.find():
		# if classtaken is in dictionary, append the title to classtakenList, set taken value to 1 and then return classTakenList
		if classTaken.lower() in doc["title"].lower() and doc["title"] in requiredDict:
			requiredDict[classTaken] = 1
		elif classTaken in doc["number"] and doc["title"] in requiredDict:
			requiredDict[doc["title"]] = 1
	'''
	for key,value in requiredDict.items():
		if(value == 1):
			reqTakenList.append(key)
	'''

	return requiredDict

# search through database for elective courses listed in user input, update dictionary
def electiveTakenSearch(cseColl, classTaken, electiveDict):
	# loop thru collection
	for doc in cseColl.find():
		# if classTaken in dict, append dictionary.key() to electiveTakenList and in hashmap for electives, set taken value to 0
		if classTaken.lower() in doc["title"].lower() and doc["title"] in electiveDict:
			electiveDict[classTaken] = 1
		elif classTaken in doc["number"] and doc["title"] in electiveDict:
			electiveDict[doc["title"]] = 1
	'''
	for key,value in electiveDict.items():
		if(value == 1):
			electiveTakenList.append(key)
	'''

	return electiveDict
