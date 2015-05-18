#!/usr/bin/env python3

from flask import Flask, abort, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/invite/create')
def invite_create():
    return render_template("invite/create.html")

@app.route('/invite/redeem/<string:invite_id>')
def invite_redeem(invite_id):
    return render_template("invite/redeem.html", invite_id=invite_id)

app.run(debug=True)