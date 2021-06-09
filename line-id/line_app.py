from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://dyecdtbvhahphu:5bfe0d9be7f6e02cb46a5ceefb0dd4455611ab226bd4cd2e27c8db25d7eb4a39@ec2-52-204-20-42.compute-1.amazonaws.com:5432/d38t3cq6b7sp2f"

db.init_app(app)

@app.route('/')
def index():
    sql_cmd = '''
        CREATE TABLE IF NOT EXISTS stocks (
                id TEXT PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                closing_price REAL NOT NULL
        );
        '''
    
    query_data = db.engine.execute(sql_cmd)
    callback = 'INSERT INTO stocks (id, name, closing_price) VALUES (2330,"台積電", 220);'
    callback = db.engine.execute(callback)
    print(query_data)
    return 'hello heroku'
@app.route('/select')
def select():
    sql_cmd='''
        SELECT *
        FROM stocks;
        '''
    query_data = db.engine.execute(sql_cmd)
    print(query_data)
    return 'This is test2'
if __name__ == "__main__":
    app.run()