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
