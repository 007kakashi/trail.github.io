from flask import Flask, render_template,request
import numpy as np

app=Flask(__name__)

@app.route('/')
def show():
    render_template('thank.html')

if __name__=='main':
    app.run(debug=True)