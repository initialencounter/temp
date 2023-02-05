from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

def init():
    conn = sqlite3.connect("mswar_rank.sqlite")
    cursor = conn.cursor()
    sql = """create table if not exists sign_in(
        id integer primary key autoincrement,
        date datetime not null,
        jsonStr str
    )
    """
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

async def add_data(jsonStr) -> any:
    init()
    conn = sqlite3.connect("mswar_rank.sqlite")
    cursor = conn.cursor()
    sql = f'''INSERT INTO sign_in VALUES(null, date(CURRENT_TIMESTAMP,'localtime'), {jsonStr}")'''
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()



async def get_data():
    init()
    conn = sqlite3.connect("mswar_rank.sqlite")
    cursor = conn.cursor()
    order_sql = "SELECT * FROM sign_in ORDER BY date"
    data = cursor.execute(order_sql).fetchall()[0]
    cursor.close()
    conn.commit()
    conn.close()
    return data


app = FastAPI()
class Item(BaseModel):
    update_time: str
    mine_rank: str
    puzzle_rank: str

@app.get("/")
def read_root():
    return {"data": "tapsss.com"}

@app.post("/upload")
async def read_item(item:Item):
    await add_data(item)
    return 'success!'


@app.get("/get")
async def send_rank():                                     # 发送群排名
    rank_text = await get_data()
    return rank_text
