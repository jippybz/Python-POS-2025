from tkinter import *
from tkinter import ttk

GUI = Tk()
GUI.geometry('900x600')
GUI.title('โปรแกรมขายผลไม้ลุง')

FONT1 = (None, 18)

L1 = Label(GUI, text='โปรแกรมขายผลไม้ลุง', font=FONT1)
L1.pack(pady=10)

# ตัวแปรหลัก
v_title = StringVar()
v_price = StringVar()
v_quantity = StringVar()
v_result = StringVar()
v_result.set('--------ผลลัพธ์--------')

# ฟังก์ชันเลือกสินค้า
def product(t, p):
    v_title.set(t)
    v_price.set(p)
    v_quantity.set('1')

# ฟังก์ชันคำนวณ
def Calculate(event=None):
    try:
        title = v_title.get()
        price = float(v_price.get())
        quantity = float(v_quantity.get())
        cal = price * quantity
        text = f'สินค้า: {title} ราคา: {price:,.2f} บาท จำนวน: {quantity:,.0f} รวม: {cal:,.2f} บาท'
        v_result.set(text)
    except:
        v_result.set('กรุณากรอกข้อมูลให้ครบและถูกต้อง')

# ฟังก์ชันเพิ่มจำนวนเมื่อกด F1
def spin_up(event=None):
    try:
        qty = float(v_quantity.get())
    except:
        qty = 0
    v_quantity.set(str(qty + 1))

GUI.bind('<F1>', spin_up)
GUI.bind('<Return>', Calculate)

# ========= โซนปุ่มสินค้า ==========
F1 = Frame(GUI)
F1.place(x=50, y=60)

# รายการผลไม้ [ชื่อ, ราคา, สีพาสเทล]
products = [
    ('Apple', 100, 'lightcoral'),
    ('Mango', 20, 'khaki'),
    ('Orange', 30, 'lightsalmon'),
    ('Banana', 15, 'lemonchiffon'),
    ('Grape', 50, 'thistle'),
    ('Watermelon', 80, 'palegreen'),
    ('Pineapple', 60, 'moccasin'),
    ('Durian', 250, 'honeydew'),
    ('Strawberry', 120, 'lightpink'),
]

# ตั้งค่า grid layout ให้ขนาดปุ่มเท่ากัน
rows = 3
cols = 3
for r in range(rows):
    F1.grid_rowconfigure(r, weight=1)
for c in range(cols):
    F1.grid_columnconfigure(c, weight=1)

# สร้างปุ่มแบบเท่ากัน สีพาสเทล
for i, (name, price, color) in enumerate(products):
    r, c = divmod(i, cols)
    btn = Button(F1, text=name, bg=color, fg='black', font=(None, 14),
                 command=lambda n=name, p=price: product(n, p))
    btn.grid(row=r, column=c, padx=5, pady=5, sticky='nsew', ipadx=10, ipady=10)

# ========= โซนป้อนข้อมูล ==========
F2 = Frame(GUI)
F2.place(x=550, y=60)

Label(F2, text='สินค้า', font=FONT1).pack()
E1 = ttk.Entry(F2, textvariable=v_title, font=FONT1)
E1.pack()
E1.focus()

Label(F2, text='ราคา', font=FONT1).pack()
E2 = ttk.Entry(F2, textvariable=v_price, font=FONT1)
E2.pack()

Label(F2, text='จำนวน', font=FONT1).pack()
E3 = ttk.Entry(F2, textvariable=v_quantity, font=FONT1)
E3.pack()

# ปุ่มคำนวณ
ttk.Button(F2, text='คำนวณ', command=Calculate).pack(pady=20, ipady=10, ipadx=20)

# แสดงผลลัพธ์
R1 = Label(GUI, textvariable=v_result, font=FONT1, fg='green')
R1.place(x=200, y=500)

GUI.mainloop()


