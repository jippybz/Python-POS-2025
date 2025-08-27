import random
from tkinter import *
from tkinter import ttk, messagebox

GUI = Tk()
GUI.geometry('700x650')
GUI.title('ยายน้อยการค้า')

L1 = Label(GUI, text='ยายน้อยการค้า', font=('tahoma', 20), fg='green')
L1.grid(row=0, column=0, columnspan=4, pady=10)

# กล่องค้นหา
search_var = StringVar()
search_entry = Entry(GUI, textvariable=search_var, font=('tahoma', 12), width=30)
search_entry.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

def search_products():
    keyword = search_var.get().lower()
    for name, (btn, _) in buttons.items():
        if keyword in name.lower():
            btn.grid()
        else:
            btn.grid_remove()

search_btn = Button(GUI, text='ค้นหา', command=search_products)
search_btn.grid(row=1, column=3, padx=5)

# รายการสินค้า
products = [
    ('แอปเปิ้ล', 'แอปเปิ้ลนำเข้านิวซีแลนด์ ราคากิโลกรัมละ 100 บาท'),
    ('มะม่วง', 'มะม่วงเขียวเสวย ราคากิโลกรัมละ 10 บาท'),
    ('ทุเรียน', 'ทุเรียนหมอนทองพรีเมียม ราคากิโลกรัมละ 300 บาท'),
    ('องุ่น', 'องุ่นเคียวโฮ ราคากิโลกรัมละ 150 บาท'),
    ('กล้วยน้ำว้า', 'กล้วยน้ำว้าห่ามหวาน ราคากิโลกรัมละ 25 บาท'),
    ('ส้มโอ', 'ส้มโอขาวแตงกวา ราคาลูกละ 50 บาท'),
    ('แตงโม', 'แตงโมกินรีหวานฉ่ำ ราคากิโลกรัมละ 18 บาท'),
    ('สับปะรด', 'สับปะรดภูแล ราคาผลละ 30 บาท'),
    ('ลำไย', 'ลำไยอบแห้ง ราคากิโลกรัมละ 90 บาท'),
    ('เงาะ', 'เงาะโรงเรียน ราคากิโลกรัมละ 45 บาท'),
    ('ชมพู่', 'ชมพู่เพชร ราคากิโลกรัมละ 35 บาท'),
    ('มังคุด', 'มังคุดคัดเกรดพรีเมียม ราคากิโลกรัมละ 70 บาท'),
    ('ฝรั่ง', 'ฝรั่งกิมจู ราคากิโลกรัมละ 30 บาท'),
    ('ส้มเขียวหวาน', 'ส้มเขียวหวานหวานชื่นใจ ราคากิโลกรัมละ 40 บาท'),
    ('มะพร้าว', 'มะพร้าวน้ำหอม ราคาลูกละ 25 บาท'),
    ('ขนุน', 'ขนุนทองประเสริฐ ราคากิโลกรัมละ 60 บาท'),
    ('อินทผลัม', 'อินทผลัมอบแห้ง ราคากิโลกรัมละ 120 บาท'),
    ('ลูกพลับ', 'ลูกพลับเกาหลี ราคาลูกละ 20 บาท'),
    ('สาลี่', 'สาลี่ทอง ราคากิโลกรัมละ 80 บาท'),
    ('เชอร์รี่', 'เชอร์รี่สดอเมริกา ราคากิโลกรัมละ 200 บาท'),
    ('บลูเบอร์รี่', 'บลูเบอร์รี่นำเข้า ราคากล่องละ 90 บาท'),
    ('ลูกพีช', 'ลูกพีชนำเข้าจากญี่ปุ่น ราคาลูกละ 60 บาท'),
    ('ราสพ์เบอร์รี่', 'ราสพ์เบอร์รี่ราคากล่องละ 110 บาท')
]

def show_product_info(text):
    messagebox.showinfo('ข้อมูลสินค้า', text)

# สีสุ่มไม่ซ้ำกันสำหรับปุ่ม
colors = ['#FFADAD', '#FFD6A5', '#FDFFB6', '#CAFFBF', '#9BF6FF', '#A0C4FF',
          '#BDB2FF', '#FFC6FF', '#FFFFFC', '#D0F4DE', '#FDFCDC', '#FFE5EC',
          '#D8F3DC', '#FEC8D8', '#E0BBE4', '#FAEDCB', '#B5EAD7', '#FFDAC1',
          '#C7CEEA', '#F2D7D5', '#F6DFEB', '#DEFDE0', '#E6E6FA']

buttons = {}

# สร้างปุ่ม
for index, (name, info) in enumerate(products):
    row = (index // 4) + 2
    col = index % 4
    color = colors[index % len(colors)]
    btn = Button(GUI, text=name, command=lambda t=info: show_product_info(t),
                 bg=color, activebackground='white', relief=RAISED)
    btn.grid(row=row, column=col, padx=5, pady=5, ipadx=10, ipady=10, sticky='nsew')
    buttons[name] = (btn, info)

# กำหนดให้ column ยืดหยุ่นตามขนาดหน้าต่าง
for i in range(4):
    GUI.columnconfigure(i, weight=1)

GUI.mainloop()

