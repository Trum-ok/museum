import os
import sqlite3
from flask import Flask, render_template, request

conn = sqlite3.connect('exhibits.db')
c = conn.cursor()

app = Flask(__name__, template_folder='templates', static_folder="templates/static")

folder_path = "../Museum/templates"
count = 0

for file_name in os.listdir(folder_path):
    if file_name.startswith('item_'):
        count += 1


def get_data():
    conn = sqlite3.connect('exhibits.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM exhibits')
    data = cur.fetchall()
    conn.close()
    return data


@app.route('/')
@app.route("/index/")
@app.route("/index.html/")
def index():
    return render_template('/index.html')


@app.route('/')
@app.route("/table/")
@app.route("/table.html/")
def table():
    data = get_data()
    return render_template('/table.html', data=data)


@app.route('/')
@app.route("/contacts/")
@app.route("/contacts.html/")
def contacts():
    return render_template('/contacts.html')


@app.route('/')
@app.route("/example/")
@app.route("/example.html/")
def example():
    data = get_data()
    return render_template('/example.html', data=data)


@app.route('/')
@app.route("/item/")
@app.route('/item.html')
def item():
    data = get_data()
    loop_index = request.args.get('value')
    loop_index_mod = loop_index.replace("/", "")
    return render_template(f'/item.html', data=data, item_number=int(loop_index_mod))


if __name__ == '__main__':
    app.run(debug=True)
