from sqlalchemy import create_engine, text 
from faker import Faker
import random
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)
@app.route("/user",methods=["GET"])

def get_users():
    users = run_sql_with_result("SELECT * FROM users")
    data=[]
    for row in users:
        users = {
        "id":row[0],
        "firstname":row[1],
        "lastname": row[2],
        "age": row[3],
        "email": row[4],
        "job": row[5]
         }
        data.append(users)
    return jsonify(data)


db_string = "postgresql://root:root@localhost:5432/postgres"
engine = create_engine(db_string)
fake=Faker()
create_table_users = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    age INT,
    email VARCHAR(200),
    job VARCHAR(100)
);
"""

create_table_app = """
CREATE TABLE IF NOT EXISTS Application (
    id SERIAL PRIMARY KEY,
    appname VARCHAR(100),
    username VARCHAR(100),
    lastconnetcion TIMESTAMP WITH TIME ZONE,
    user_id INTEGER REFERENCES users(id)
);
"""

def run_sql(query:str):
    with engine.connect() as connection:
        trans = connection.begin()
        connection.execute(text(query))
        trans.commit()


def run_sql_with_result(query:str):
    with engine.connect() as connection:
        trans = connection.begin()
        result = connection.execute(text(query))
        trans.commit()
        return result

def populate():

    apps=["facebook","Twitter","Youtube","TikTok","Instagram"]
    num_apps = random.randint(1,5)

    for _ in range(100):
         
        

        firstname=fake.first_name()
        lastname = fake.last_name()
        age=random.randrange(18,50)
        email=fake.email()
        job =fake.job().replace("'","")
        #print(firstname,lastname,age,email,job)
        insert_query = f"""
            INSERT INTO users (firstname, lastname,age,email,job) 
            VALUES ('{firstname}','{lastname}', '{age}','{email}','{job}')
            RETURNING id
           """
       
        user_id=run_sql_with_result(insert_query).scalar()

        for i in range(num_apps):
            app_name = random.choice(apps)
            lastconnection= datetime.now()
            username=fake.user_name()
            sql_insert_app = f"""
                INSERT INTO Application (appname, username,lastconnetcion,user_id)
                VALUES ('{app_name}','{username}','{lastconnection}','{user_id}')
                """
            run_sql(sql_insert_app)

        print(user_id)




if __name__ == '__main__' :
    
    app.run(host="0.0.0.0",port=8081,debug=True)
    #run_sql(create_table_users)
    #run_sql(create_table_app)
    #populate()





