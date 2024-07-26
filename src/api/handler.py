from src import database as db
import sqlalchemy


sql = sqlalchemy.text("""
                      select *
                      from table
                      where id > :arg1
                      """)

val1 = "some data"

with db.engine.begin() as connection:
    result = connection.execute(sql, {"arg1": val1}).fetchone()
