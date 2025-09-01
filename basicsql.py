import sqlite3

conn = sqlite3.connect('posdb.sqlite3')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS product (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT,
            title TEXT,
            price REAL,
            category TEXT,
            unit TEXT,
            button TEXT,
            status TEXT,
            note TEXT)""")

# เพิ่ม table transaction (ใช้ backticks เพราะ transaction เป็น reserved word)
c.execute("""CREATE TABLE IF NOT EXISTS `transaction` (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            subtotal REAL,
            vat REAL,
            total REAL,
            paid REAL,
            change_amount REAL,
            items TEXT)""")

def insert_product(barcode,title,price,category,unit='ชิ้น',button='-',status='instock',note=''):
    with conn:
        command = 'INSERT INTO product VALUES(?,?,?,?,?,?,?,?,?)'
        c.execute(command,(None,barcode,title,price,category,unit,button,status,note))
        conn.commit()
        print('saved')

def view_product(allfield=True):
    with conn:
        if allfield:
            command = 'SELECT * FROM product'
        else:
            command = 'SELECT barcode,title,price,category FROM product'
        c.execute(command)
        data = c.fetchall()
        print(data)

    return data

def delete_product(barcode):
    with conn:
        command = 'DELETE FROM product WHERE barcode=(?)'
        c.execute(command,([barcode]))
        conn.commit()

def search_barcode(barcode):
    with conn:
        command = 'SELECT barcode,title,price,category FROM product WHERE barcode=(?)'
        c.execute(command,([barcode]))
        data = list(c.fetchone())
        print(data)
        return data

def insert_transaction(subtotal, vat, total, paid, change_amount, items):
    import datetime
    with conn:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        command = 'INSERT INTO `transaction` VALUES(?,?,?,?,?,?,?,?)'
        c.execute(command, (None, current_time, subtotal, vat, total, paid, change_amount, items))
        conn.commit()
        print('Transaction saved')

if __name__ == '__main__':
    # insert_product('1002','Durian',200,'fruit')
    # delete_product('1002')
    # search_barcode('1003')
    view_product()