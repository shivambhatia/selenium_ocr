"""
Designed By: Shivam Bhatia
Date: 10/07/2021
Used to extract data from the given url using cloud vision api
to bypass the captcha text using OCR
"""

from flask import Flask, redirect, url_for, request
app = Flask(__name__)
from flask import jsonify
import detect

    
url = "https://drt.gov.in/front/page1_advocate.php"
   
    
@app.route('/getData',methods = ['POST', 'GET'])
def getData():
   """
   request params:
   name: Enter Party Name
   schemaname: Select DRT/DRAT

   Function will return the list of data rows return from table
   """
   if request.method == 'POST':
      name = request.form.get('name',None)
      schemaname=request.form.get('schemaname',None)
      if name==None or schemaname==None:
          return "Invalid Inputs"
      else:
          data=detect.main(url,name,schemaname)
          return jsonify(data)
   else:
      return "Invalid Request Use POST REQUEST ONLY WITH PARAMS"

if __name__ == '__main__':
   app.run(debug = True)