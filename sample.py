import database as db

cursor = db.conn.cursor(dictionary=True)


query = "SELECT * FROM tbl_account";

cursor.execute(query)

results = cursor.fetchall()
rows = []

def addAcc():
    account_id = 1
    cursor.execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,))



for row in results:
    for key, value in row.items():
        print(f"{key}: {value} ")
    print()

