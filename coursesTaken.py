#!/usr/bin/env python3
import pymongo
import pprint

# retrieve info from database
def retrieve_db():
	client = pymongo.MongoClient("mongodb://hsiaopat:Aerodynamicfeathers7@hsiaoer-of-pattys-shard-00-00.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-01.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-02.qdmrj.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-pyw8am-shard-0&authSource=admin&retryWrites=true&w=majority")
	cse_db = client["cse_courses"]
	cse_coll = cse_db["cse_collections"]
	return cse_coll

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

# create dictionary for elective courses
def initElective(cse_coll):
	electiveDict = {}
	# iterate through each hashmap in collection
	for doc in cse_coll.find():
		# append all titles with type electives with a taken value of 0
		if doc["type"] == "Elective":
			name = doc["title"]
			electiveDict.update({name:0})

	return electiveDict

# search through database for required courses listed in user input, update dictionary
def reqCourseTakenSearch(cse_coll, classTaken, requiredDict):
	count = 0
	# iterate through collection
	for doc in cse_coll.find():
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
def electiveTakenSearch(cse_coll, classTaken, electiveDict):
	# loop thru collection
	for doc in cse_coll.find():
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

#Main function
def main():
	cse_coll = retrieve_db()
	requiredDict = initRequired(cse_coll)
	electiveDict = initElective(cse_coll)
	search = "20289, 20221, Data Science"
	userInput = search.split(",")
	for course in userInput:
		course = course.strip()

	#if search not in requiredDict.keys() and search not in electiveDict.keys():
	#	print("uh oh")
	#	return 1


		requiredDict = reqCourseTakenSearch(cse_coll,course,requiredDict)
		electiveDict = electiveTakenSearch(cse_coll,course,electiveDict)

	print("Taken:")
	for course in requiredDict:
		if requiredDict[course] == 1:
			print(course)

	print("\nNeed to take:")
	for course in requiredDict:
		if requiredDict[course] == 0:
			print(course)

	print("\nUntaken electives:")
	for course in electiveDict:
		if electiveDict[course] == 0:
			print(course)

	#pprint.pprint(requiredDict)
	#pprint.pprint(electiveDict)




if __name__ == '__main__':
	main()


#display list of required courses left

#display list of electives for you


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















def findRequired(courseInput, cseColl, requiredDict, electiveDict):
	courseInput = courseInput.split(",")
	for course in courseInput:
		course = course.strip()
		requiredTaken = reqCourseTakenSearch(cseColl, course, requiredDict)
		electiveTaken = electiveTakenSearch(cseColl, course, electiveDict)

	return requiredTaken


def findElectives(courseInput, keywordInput, cseColl, takenDict):

	courseInput = courseInput.split()
	for course in courseInput:
		course = course.strip()
		takenDict = courseTakenSearch(cseColl, course, takenDict)

	keywordInput = keywordInput.split(",")
	foundKeyword = []
	for key in keywords:
		key = key.strip()
		foundKeyword = searchKeyword(key, cseColl, foundKeyword)

	# availableElectives
	availableElectives = checkPrereq(foundKeyword, takenDict)
	electives = []
	for course in availableElectives:
		electives.append(course["title"])

	return electives


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
