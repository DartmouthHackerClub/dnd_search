from flask import Flask, request, session, render_template, redirect
from dnd_ldap import lookup
import re

app = Flask(__name__)

@app.route("/")
def index():
    return redirect('/search')

@app.route("/search")
def search():
    err_msg = ""
    raw_results = []
    results = []
    attributes = ['cn','mail','dndAssignedNetid']

    query = request.args.get('query')

    if not query:
        err_msg = "Please specifiy a query"
    else:
        raw_results = lookup(query, None)

    if raw_results == None:
        results = []
        err_msg = "LDAP query failed"

    
    for result in raw_results:
        result = { attribute: result[attribute] for attribute in attributes }
        results.append(result)

    return render_template('search.html', results=results, err_msg=err_msg)

if __name__ == "__main__":
    app.run(debug=True)
