from flask import Flask, request, session, render_template, redirect
from dnd_ldap import lookup
import re

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', results=[], err_msg="")

@app.route("/search")
def search():
    err_msg = ""
    raw_results = []
    results = []
    attributes = ['mail','dndAssignedNetid','cn','dndHinmanaddr','dndDeptclass','telephoneNumber']

    query = request.args.get('query')

    if not query:
        err_msg = "Please specify a query"
    else:
        results = lookup(query)

    if results == None:
        results = []
        err_msg = "LDAP query failed"

    if request.is_xhr:
        return render_template('search.html', results=results, err_msg=err_msg)
    else:
        return render_template('index.html', results=results, err_msg=err_msg)

if __name__ == "__main__":
    app.run(debug=False)
