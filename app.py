import os
import asyncio
import asyncpg
import sqlite3
import logging
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, render_template, request
from colorlog import ColoredFormatter

from db.main import Database

logging.basicConfig(level=logging.INFO, filename="log.log")
logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)

console.setFormatter(formatter)
logger.addHandler(console)

load_dotenv()
database_url = os.getenv("DATABASE_URL")

app = Flask(__name__, template_folder='templates', static_folder="templates/static")
CORS(app)


async def get_data():
    pool = await main()
    db = Database(pool)
    data = await db.items.get_all()
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
    data = asyncio.run(get_data())
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
    data = asyncio.run(get_data())
    return render_template('/example.html', data=data)


@app.route('/')
@app.route("/item/")
@app.route('/item.html')
def item():
    data = asyncio.run(get_data())
    loop_index = request.args.get('value')
    loop_index_mod = loop_index.replace("/", "")
    return render_template(f'/item.html', data=data, item_number=int(loop_index_mod))


async def main():
    try:
        pool = await asyncpg.create_pool(database_url)
    except Exception as e:
        logging.warning("Failed to connect to database", exc_info=e)
        return
    if not pool:
        raise AssertionError
    return pool

if __name__ == '__main__':
    # pool = asyncio.run(main())
    app.run(debug=True)
