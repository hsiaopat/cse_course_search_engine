#!/usr/bin/env python3
import pymongo
import pprint

#retrieve info from database
def retrieve_db():
	client = pymongo.MongoClient("mongodb://hsiaopat:Aerodynamicfeathers7@hsiaoer-of-pattys-shard-00-00.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-01.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-02.qdmrj.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-pyw8am-shard-0&authSource=admin&retryWrites=true&w=majority")
	cse_db = client["cse_courses"]
	cse_coll = cse_db["cse_collections"]
	return cse_coll
#search

def initRequired(cse_coll): #create dictionary for required courses
	#go thru each hashmap in collection
	requiredDict = {}
	for doc in cse_coll.find():
		#append all titles with type required with a taken value of 0
		if doc["type"] == "Required":
			name = doc["title"]
			print(name)
			requiredDict[name].append(0)
	return requiredDict
			
def initElective(cse_coll): #create dictionary for elective courses
	#go thru each hashmap in collection
	electiveDict = {}
	for doc in cse_coll.find():
		#append all titles with type electives with a taken value of 0
		if doc["type"] == "Elective":
			electiveDict[doc["title"]].append(0)
	return electiveDict

def reqCourseTakenSearch(cse_coll,classTaken, requiredDict):#cse_coll is collection, classTaken is input String
	reqTakenList = []
	#loop thru collection
	for doc in cse_coll.find():
		#if classtaken is in dictionary, append the title to classtakenList, set taken value to 1 and then return classTakenList
		if classTaken in requiredDict.keys():
			requiredDict[classTaken] = 1
			reqTakenList.append(classTaken)
	return reqTakenList

def electiveTakenSearch(cse_coll,classTaken, electiveDict):
	electiveTakenList = []
	#loop thru collection
	for doc in cse_coll.find():
		#if classTaken in dict, append dictionary.key() to electiveTakenList and in hashmap for electives, set taken value to 0
		if classTaken in electiveDict.keys():
			electiveDict[classTaken] = 1
			electiveTakenList.append(classTaken)
	return electiveTakenList

def main():
	cse_coll = retrieve_db()
	requiredDict = {}
	electiveDict = {}
	requiredDict = initRequired(cse_coll)
	electiveDict = initElective(cse_coll)
	search = "error"
	if search not in requiredDict.keys() and search not in electiveDict.keys():
		print("uh oh")
		return 1
	reqTakenList = reqCourseTakenSearch(cse_coll,search,requiredDict)
	electiveTakenList = electiveTakenSearch(cse_coll,search,electiveDict)
	
	print('\n'.join(reqTakenList))

	print('\n'.join(electiveTakenList))

	
	
	
if __name__ == '__main__':
	main()


#display list of required courses left

#display list of electives for you
