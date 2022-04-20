#!/usr/bin/env python3

import pymongo
import pprint

def retrieve_db():
	client = pymongo.MongoClient("mongodb://hsiaopat:Aerodynamicfeathers7@hsiaoer-of-pattys-shard-00-00.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-01.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-02.qdmrj.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-pyw8am-shard-0&authSource=admin&retryWrites=true&w=majority")
	cse_db = client["cse_courses"]
	cse_coll = cse_db["cse_collections"]
	return cse_coll

def search_keyword(keyword, cse_coll):

	found_keyword = []

	for doc in cse_coll.find():
		if keyword in doc["description"].lower():
			found_keyword.append(doc)
		elif keyword in doc["title"].lower():
			found_keyword.append(doc)

	return found_keyword

def main():
	cse_coll = retrieve_db()
	keyword = "machine learning"
	found_keyword = search_keyword(keyword, cse_coll)
	for course in found_keyword:
		print(f'{course["title"]}')

if __name__ == '__main__':
	main()
