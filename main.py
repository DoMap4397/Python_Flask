from flask import Flask, render_template, request, redirect, jsonify, sessions
from pymongo import MongoClient
import uuid
import time

client = MongoClient('mongodb://localhost:27017/')
db = client['pentest_db']
collections = db['vulnerable']

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/Vulnerable')


@app.route('/Vulnerable')
def Vulnerable_index():
    data = list(collections.find({}))
    return render_template('Vulnerable/index.html', data=data)


@app.route('/Vulnerable/Create', methods=["POST", "GET"])
def Vulnerable_create():
    if request.method == "GET":
        return render_template('Vulnerable/add.html')
    else:
        response = {
            "ok": False,
            "mesg": "Nothing",
            "data": []
        }
        title = request.form['title']
        url = request.form['url']
        # if url:
        #     found_url = url.query.filter_by().first()
        #     if found_url:
        #         url = found_url
        #     else:
        #         url = request.form['url']
        description = request.form['description']
        try:
            obj = {
                'id': f'vul-{uuid.uuid4()}-{int(time.time())}',
                'title': title,
                'url': url,
                'description': description
            }
            collections.insert_one(obj)
            response = {
                "ok": True,
                "mesg": "Create successfully",
                "data": []
            }
        except Exception as err:
            response = {
                "ok": False,
                "mesg": "Something wrong",
                "data": []
            }
        return jsonify(response)


@app.route('/Vulnerable/Edit/<vul_id>', methods=['PUT', 'GET'])
def Vulnerable_edit(vul_id):
    if request.method == 'GET':
        data = collections.find_one({"id": vul_id})
        if not data:
            return "check"
        return render_template('Vulnerable/edit.html', data=data)
    else:
        response = {
            "ok": False,
            "mesg": "Nothing",
            "data": []
        }
        title = request.form['title']
        url = request.form['url']
        description = request.form['description']
        try:
            data = collections.find_one({'id': vul_id})
            collections.update_one(
                {'id': vul_id},
                {"$set": {
                    "title": request.form.get('title'),
                    "url": request.form.get('url'),
                    "description": request.form.get('description')
                }
                })
            response = {
                "ok": True,
                "mesg": "Edit successfully",
                "data": [data]
            }
        except Exception as err:
            response = {
                "ok": False,
                "mesg": "Something wrong",
                "data": []
            }
        return jsonify(response)


@app.route('/Vulnerable/delete/<vul_id>', methods=['POST'])
def Vulnerable_delete(vul_id):
    collections.delete_one({"id": vul_id})
    response = {
        "ok": True,
        "mesg": "Delete successfully",
        "data": []
    }
    return jsonify(response)


@app.route('/home')
def main():
    data = list(collections.find({}))
    return render_template('home.html', data=data)


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/add', methods=['POST'])
def add_data():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        description = request.form['description']
        try:
            obj = {
                'title': title,
                'url': url,
                'description': description
            }
            collections.insert_one(obj)

        except Exception as err:
            print(err)
        return redirect('/home')


@app.route('/edit')
def edit():
    return render_template('edit.html')


@app.route('/test_db')
def test_db():
    data = list(collections.find({}))
    return render_template("test_db.html", data=data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=False)
