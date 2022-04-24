import requests
import os
import sys
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
	#what data do we need?

	if request.method == 'GET': #GET request is sent when html wants some information from python backend
		return render_template('nameOfHtmlImake', reqTakenList, electiveTakenList, availableElectives)
		#we have to talk ab available electives vs elective search

	if request.method == 'POST': #POST request is when the webpage is sending data to python backend
		reqTakenList = request.form.get('laskdfjl')
		#get all we need from python code

		finalData = [] #blah

		return render_template("nameofhtmlImake") #alskdfjlskdf)

	#all our methods

