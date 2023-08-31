from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['test_db']
collections = db['test_1']

app = Flask(__name__)


@app.route('/home')
def main():
    data = list(collections.find({}))
    return render_template('home.html', data=data)


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/test_db')
def test_db():
    data = list(collections.find({}))
    return render_template("test_db.html", data=data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
