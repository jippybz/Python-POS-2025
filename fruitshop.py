from tkinter import *
from tkinter import ttk

GUI = Tk()
GUI.geometry('800x500')
GUI.title('โปรแกรมขายผลไม้')

FONT1 = (None,18)

L1 = Label(GUI,text='โปรแกรมขายผลไม้ลุง',font=FONT1)
L1.pack()


# zone 1
F1 = Frame(GUI)
F1.place(x=20,y=50)

def apple():
    v_title.set('Apple')
    v_price.set('200')
    v_quantity.set('1')

def product(t,p):
    v_title.set(t)
    v_price.set(p)
    v_quantity.set('1')

B1 = ttk.Button(F1,text='Apple',command=lambda: product('Apple',100))
B1.grid(row=0,column=0,ipadx=10,ipady=20)

B2 = ttk.Button(F1,text='Mango',command= lambda: product('Mango',20))
B2.grid(row=0,column=1,ipadx=10,ipady=20)

B3 = ttk.Button(F1,text='Orange',command= lambda: product('Orange',30))
B3.grid(row=0,column=2,ipadx=10,ipady=20)

GUI.bind('<F1>',lambda x=None: v_quantity.set(float(v_quantity.get())+1))  # Spin up

# zone 2
F2 = Frame(GUI)
F2.place(x=500,y=50)

L = Label(F2,text='สินค้า',font=FONT1).pack()
v_title = StringVar()
E1 = ttk.Entry(F2,textvariable=v_title,font=FONT1)
E1.pack()
E1.focus()

L = Label(F2,text='ราคา',font=FONT1).pack()
v_price = StringVar()
E2 = ttk.Entry(F2,textvariable=v_price,font=FONT1)
E2.pack()

L = Label(F2,text='จำนวน',font=FONT1).pack()
v_quantity = StringVar()
E3 = ttk.Entry(F2,textvariable=v_quantity,font=FONT1)
E3.pack()


#zone 3

def Calculate():
    title = v_title.get()
    price = float(v_price.get())
    quantity = float(v_quantity.get())
    print(title,price,quantity)
    cal = price * quantity
    text = f'สินค้า: {title} ราคา: {price:,.2f} จำนวน: {quantity:,.2f} รวม: {cal:,.2f}'
    v_result.set(text)
    v_title.set('')
    v_price.set('')
    v_quantity.set('')


BC1 =ttk.Button(F2,text='Calculate',command=Calculate)
BC1.pack(pady=20,ipady=20,ipadx=10)

v_result = StringVar()
v_result.set('--------result--------')
R1 = Label(GUI,textvariable=v_result,font=FONT1)
R1.place(x=200,y=400)


GUI.mainloop()