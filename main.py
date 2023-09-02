from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['test_db']
collections = db['test_1']

mylist = [
    {
        'id': 'test 3',
        'title': 'Test title 2',
        'url': 'https://www.test2.com',
        'description': 'test description 2'
    }
]

x = collections.insert_many(mylist)

app = Flask(__name__)


@app.route('/home')
def main():
    data = list(collections.find({}))
    return render_template('home.html', data=data)


@app.route('/create')
def create():
    data = list(collections.find({}))
    return render_template('create.html', data=data)


@app.route('/edit')
def edit():
    return render_template('edit.html')


@app.route('/test_db')
def test_db():
    data = list(collections.find({}))
    return render_template("test_db.html", data=data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
