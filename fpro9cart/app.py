from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta

app = Flask(__name__);

app.secret_key="abcde1234"
app.permanent_session_lifetime=timedelta(minutes=5) # 세션 만료 시간 5분 

products = [
    {"id":1,"name":"노트북","price":3500000},
    {"id":2,"name":"물티슈","price":3500},
    {"id":3,"name":"종이컵","price":350},
    {"id":4,"name":"볼펜","price":1500},
]



@app.route('/')
def product_list():
    return render_template("products.html",products=prod);