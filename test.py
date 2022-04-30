#!/usr/bin/env python3

import pymongo
import pprint

def retrieve_db():
	client = pymongo.MongoClient("mongodb://hsiaopat:Aerodynamicfeathers7@hsiaoer-of-pattys-shard-00-00.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-01.qdmrj.mongodb.net:27017,hsiaoer-of-pattys-shard-00-02.qdmrj.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-pyw8am-shard-0&authSource=admin&retryWrites=true&w=majority")
	cse_db = client["cse_courses"]
	cse_coll = cse_db["cse_collections"]
	return cse_coll

def search_keyword(keyword, cse_coll):
	for doc in cse_coll.find():
		if keyword in doc["description"].lower():
			print(f'{doc["department"]} {doc["number"]} {doc["title"]}');
		elif keyword in doc["title"].lower():
			print(f'{doc["department"]} {doc["number"]} {doc["title"]}');

def main():
	cse_coll = retrieve_db()
	keyword = "machine learning"
	search_keyword(keyword, cse_coll)

if __name__ == '__main__':
	main()
