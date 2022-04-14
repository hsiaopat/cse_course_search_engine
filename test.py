#!/usr/bin/env python3

import pymongo
import pprint

def retrieve_db():
	#hi
	cse_db = client["cse_courses"]
	cse_coll = cse_db["cse_collections"]
	return cse_coll

def main():
	cse_coll = retrieve_db()
	for doc in cse_coll.find():
		print(f'{doc["department"]} {doc["number"]} {doc["title"]}');

if __name__ == '__main__':
	main()
	
