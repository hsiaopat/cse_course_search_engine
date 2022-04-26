import requests
import os
import sys
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/",methods=["POST","GET"])
def index():

	#cseColl = retrieveDB()

	#takenDict = initTaken(cseColl)
	#requiredTaken = initRequired(cseColl)
	#electiveTaken = initElective(cseColl)
	requiredTaken = ["Fundamentals of Computing", "Dicrete Math"]
	requiredRemaining = ["Discrete Math", "Logic Design"]
	electives = ["CSE Service Projects", "Data Science", "Programming Challenges"]


	if request.method == "GET": #GET request is sent when html wants some information from python backend
		return render_template("index.html", taken=requiredTaken, remaining=requiredRemaining, electivesAvailable=electives)

	if request.method == "POST": #POST request is when the webpage is sending data to python backend

		courseInput = request.form.get("courseInput")
		keywordInput = request.form.get("keywordInput")
		#requiredTaken = findRequired(courseInput, cseColl, requiredDict, electiveDict)
		#electives = findElectives(courseInput, keywordInput, cseColl, takenDict)

	return render_template("index.html", taken=requiredTaken, remaining=requiredRemaining, electivesAvailable=electives)

	#all our methods
