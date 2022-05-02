
from flask import Flask, render_template, request, url_for

import mysql.connector 
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd = "1234",
  database="Buy_Sell_books"
)

# db = mydb.cursor()

app = Flask(__name__)

app.config['SECRET_KEY'] = '49bf8924ee4eb2a97a849140'

from Book_store import routes