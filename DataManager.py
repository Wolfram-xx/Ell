import sqlite3

def sql_connection():
    try:
        connection = sqlite3.connect('ell_db.db')
        return connection
    except sqlite3.Error as error:
        return error

con = sql_connection()

def sql_connection_open():
    cur = con.cursor()
    return cur

cur = sql_connection_open()

def sql_connection_close():
    con.close()

# проверка: пришел ответ от бд или нет
def check_query_answer(ans):
    if ans:
        return ans
    else:
        return False

def sql_query(query):
    cur.execute(query)
    con.commit()
    ans = cur.fetchall()
    return check_query_answer(ans)

def execute_and_commit(query):
    cur.execute(query)
    con.commit()

def insert(table, column, value):
    query = f"INSERT INTO {table} ({column}) VALUES ({value});"
    execute_and_commit(query)
    return True

def update(table, column, value, id):
    query = f"UPDATE {table} SET {column}='{value}' WHERE id='{id}';"
    execute_and_commit(query)
    return True

def insertImg(table, column, value):
    query = f"INSERT INTO {table} ({column}) VALUES ({value});"
    execute_and_commit(query)
def selectOne(table, column, value, column1):
    query = f"SELECT {column1} FROM {table} WHERE {column}='{value}';"
    execute_and_commit(query)
    return cur.fetchall()

def selectall(table):
    query = f"SELECT * FROM {table};"
    execute_and_commit(query)
    return cur.fetchall()
def selectseveraltable(table1, table2, column, condition):
    query = f"SELECT {column} FROM {table1} INNER JOIN {table2} AS S ON {condition};"
    execute_and_commit(query)
    return cur.fetchall()

def selectseveraltable2(id):
    query = f"SELECT Compon.id, Details.place, " \
            f"Compon.name, Compon.code, Compon.link_image, Compon.outer_diam, Compon.inner_diam, Compon.length, Compon.passport, " \
            f"Details.primary_cost, Details.profitability FROM Details INNER JOIN Compon ON " \
            f"Details.id_img=Compon.id AND Details.id_project={id};"
    execute_and_commit(query)
    ans = cur.fetchall()
    return ans

def delete(table, condition):
    query = f"DELETE FROM {table} WHERE id='{condition}';"
    execute_and_commit(query)
    return True

# user
def select_user_id(column, id): # берет колонку из таблицы Users по id
    query = f"SELECT {column} FROM users WHERE id='{id}';"
    execute_and_commit(query)
    ans = cur.fetchall()
    return check_query_answer(ans)

def select_users_where(column, where): # берет колонку из таблицы Users по условию
    query = f"SELECT {column} FROM users WHERE {where};"
    execute_and_commit(query)
    ans = cur.fetchall()
    return check_query_answer(ans)

def select_projects_all():
    query = "SELECT id, company, date, last_date FROM Project WHERE outer_diam IS NOT NULL ORDER BY last_date DESC;"
    execute_and_commit(query)
    ans = cur.fetchall()
    return check_query_answer(ans)

def select_projects_part(user_id):
    query = f"SELECT id, company, date, last_date FROM Project WHERE outer_diam IS NOT NULL AND engineer={user_id} ORDER BY last_date DESC;"
    execute_and_commit(query)
    ans = cur.fetchall()
    return check_query_answer(ans)

def select_project_id(columns,id):
    query = f"SELECT {columns} FROM Project WHERE id={id};"
    execute_and_commit(query)
    ans = cur.fetchall()
    return check_query_answer(ans)

def insert_new_user(columns, values):
    query = f"INSERT INTO Users ({columns}) VALUES ({values});"
    execute_and_commit(query)
    return True

def select_id_and(code, tab):
    query = f"SELECT id FROM Compon WHERE code LIKE '{code}%' AND thread_type='{tab}';"
    execute_and_commit(query)
    return cur.fetchall()
def select_id_andor(code, OD, ID, thread, tab):
    query = f"SELECT id FROM Compon WHERE code LIKE '{code}%' AND (thread_type='Strike {OD}-{ID} {thread}' OR thread_type='{tab}');"
    execute_and_commit(query)
    return cur.fetchall()
def select_id_andwithoutor(code, OD, ID, thread):
    query = f"SELECT id FROM Compon WHERE code LIKE '{code}%' AND thread_type LIKE '%{OD}-{ID} {thread}';"
    execute_and_commit(query)
    return cur.fetchall()

def selectdistinctsubctringcode(where):
    query = f"SELECT DISTINCT SUBSTRING(code,1,3) FROM Compon WHERE {where};"
    execute_and_commit(query)
    return cur.fetchall()
