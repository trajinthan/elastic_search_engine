from flask import Flask, render_template, request
from search import search
from elasticsearch_dsl import Index

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def ui_search():
    if request.method == 'POST':
        query = request.form['term']
        res = search(query)
        hits = res['hits']['hits']
        time = res['took']
        num_results =  res['hits']['total']['value']
        return render_template('result.html', query=query, hits=hits, num_results=num_results,time=time)

    if request.method == 'GET':
        return render_template('result.html', init='True')

if __name__ == '__main__':
    app.run(debug=True)
