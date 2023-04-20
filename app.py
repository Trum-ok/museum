from flask import Flask, render_template
import sqlite3

# import pandas as pd
# from sqlalchemy import create_engine
#
# data = pd.read_excel('templates/static/tables/dasabate.xlsx')
#
# # Преобразуем поле 'amount' в тип int
# data['amount'] = data['amount'].astype(int)
#
# engine = create_engine('sqlite:///exhibits.db', echo=True)
# sqlite_connection = engine.connect()
#
# data.to_sql('exhibits', sqlite_connection, if_exists='replace', index=False)


conn = sqlite3.connect('exhibits.db')  # database connection
c = conn.cursor()

app = Flask(__name__, template_folder='templates', static_folder="templates/static")


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
    # print(data)
    return render_template('/table.html', data=data)


@app.route('/')
@app.route("/contacts/")
@app.route("/contacts.html/")
def contacts():
    return render_template('/contacts.html')


if __name__ == '__main__':
    app.run(debug=True)
