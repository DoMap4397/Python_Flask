from flask import Flask, render_template, request, redirect, jsonify
from flask_paginate import Pagination, get_page_args
from databases.connect_db import collections
import uuid
import time

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/Vulnerable')


users = list(range(200))


def get_users(offset=0, per_page=10):
    return users[offset: offset + per_page]


@app.route('/Vulnerable')
def Vulnerable_index():
    data = list(collections.find({}))
    page, per_page, offset = get_page_args(page_paramrter='page', per_page_paramter='per_page')

    total = len(users)

    pagination_users = get_users(offset=offset, per_page=per_page)

    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('Vulnerable/index.html', data=data,
                           users=pagination_users, page=page,
                           per_page=per_page, pagination=pagination)


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
        description = request.form['description']
        urls = list(collections.find({'url': request.form['url']}))
        url = url.split('?')[0].split('#')[0]
        if len(urls) > 0:
            response = {
                "ok": False,
                "mesg": "Url already exists!",
                "data": []
            }
        else:
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


@app.route('/Vulnerable/Edit/<vul_id>', methods=['POST', 'GET'])
def Vulnerable_edit(vul_id):
    if request.method == 'GET':
        data = collections.find_one({'id': vul_id})
        if not data:
            return "check"
        return render_template('Vulnerable/edit.html', data=data)
    if request.method == 'POST':
        response = {
            "ok": False,
            "mesg": "Nothing",
            "data": []
        }
        try:
            title = request.form.get('title')
            url = request.form.get('url')
            description = request.form.get('description')
            collections.update_one(
                {'id': vul_id},
                {"$set": {
                    "title": title,
                    "url": url,
                    "description": description
                }
                })
            response = {
                "ok": True,
                "mesg": "Edit successfully",
                "data": []
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


# @app.route('/home')
# def main():
#     data = list(collections.find({}))
#     return render_template('home.html', data=data)
#
#
# @app.route('/create')
# def create():
#     return render_template('create.html')
#
#
# @app.route('/add', methods=['POST'])
# def add_data():
#     if request.method == 'POST':
#         title = request.form['title']
#         url = request.form['url']
#         description = request.form['description']
#         try:
#             obj = {
#                 'title': title,
#                 'url': url,
#                 'description': description
#             }
#             collections.insert_one(obj)
#
#         except Exception as err:
#             print(err)
#         return redirect('/home')
#
#
# @app.route('/edit')
# def edit():
#     return render_template('edit.html')


@app.route('/test_db')
def test_db():
    data = list(collections.find({}))
    return render_template("test_db.html", data=data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=False)
