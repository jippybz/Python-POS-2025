from tkinter import *
from tkinter import ttk, messagebox
import os
from basicsql import *

#ใช้งานจริงควรใช้อันนี้
#PATH = os.getcwd()
#print(PATH)
#p1 = os.path.join(PATH,'tab1.png')

GUI = Tk()
w = 900
h = 500

ws = GUI.winfo_screenwidth()
hs = GUI.winfo_screenheight()

x = (ws/2)-(w-2) 
y = (hs/2)-(h-2)

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')
#GUI.geometry('900x500')
GUI.title('โปรแกรมขายของยายน้อยการค้า')

################MENU#######################
menubar = Menu(GUI)
GUI.config(menu=menubar)

#File Menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='เปิดเมนูเพิ่มสินค้า',command=lambda: print('Add Product'))
filemenu.add_command(label='ออกจากโปรแกรม',command=lambda: GUI.quit())


#About Menu

def AboutMenu(event=None):
    GUI2 = Toplevel()
    w = 500
    h = 300

    ws = GUI.winfo_screenwidth()
    hs = GUI.winfo_screenheight()

    x = (ws/2)-(w-2)
    y = (hs/2)-(h-2)

    GUI2.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

    jipjip_icon = PhotoImage(file='jipjip.png').subsample(2) # .subsample(2) resize down / 2
    Label(GUI2,image=jipjip_icon).pack()

    Label(GUI2,text='โปรแกรมสำหรับขายของ by jipjipstore\nTel: 0907437633').pack()

    GUI2.mainloop()


aboutmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='About',menu=aboutmenu)
aboutmenu.add_command(label='เกี่ยวกับโปรแกรม',command=AboutMenu)

GUI.bind('<F2>',AboutMenu)


################TAB####################

Tab = ttk.Notebook(GUI)
Tab.pack(fill=BOTH,expand=1)

T1 = Frame(Tab)
T2 = Frame(Tab)

tab_icon1 = PhotoImage(file='tab1.png')
tab_icon2 = PhotoImage(file='tab2.png')

Tab.add(T1,text='เมนูขาย',image=tab_icon1,compound='left')
Tab.add(T2,text='เพิ่มสินค้า',image=tab_icon2,compound='left')

FONT1 = (None,20)
FONT2 = (None,18) 
#######################TAB1############################

L1 = Label(T1,text='เมนูสำหรับขาย',font=FONT1)
L1.pack()

#ตัวแปร
v_title = StringVar()
v_price = StringVar()
v_quantity = StringVar()
v_result = StringVar()

#product
def product(t,p):
    v_title.set(t)
    v_price.set(str(p))
    v_quantity.set('1')

cart = {}

def button_insert(b,t,p,q=1):
    table_sales.delete(*table_sales.get_children())
    if b not in cart:
        cart[b] = [b,t,p,q]
    else:
        cart[b][3]=cart[b][3] + 1 # เพิ่มครั้งละ 1 ถ้าหากมีข้อมูลอยู่แล้ว
    for c in cart.values():
        table_sales.insert('','end',values=c)

#calculate



# zone 1
F1 = Frame(T1)
F1.place(x=20,y=50)

# Label(F1, text='ขายผลไม้', font=(None, 20)).grid(row=0, column=0, columnspan=3)

database = [['Apple', 100],
            ['Banana', 20],
            ['Mango', 30],
            ['Coconut', 40],
            ['Durian', 200],
            ['Orange', 25],
            ['Pineapple', 50],
            ['Grapes', 60],
            ['Strawberry', 80],
            ['Blueberry', 90],
            ['Watermelon', 70],
            ['Papaya', 35],
            ['Guava', 30],
            ['Lychee', 45],
            ['Longan', 40],
            ['Rambutan', 55],
            ['Tamarind', 25],
            ['Avocado', 100],
            ['Kiwi', 60],
            ['Pomegranate', 120]
]
col = 0
row = 0

# for i,db in enumerate(database[:15],start=1):
#     B = ttk.Button(F1, text=db[0], command=lambda pd=db: button_insert('-',pd[0], pd[1],1))
#     B.grid(row=row, column=col, ipadx=10, ipady=20, padx=5)
#     col = col + 1 #col+=1
#     if i % 3 == 0:
#         col = 0
#         row = row + 1
for i,db in enumerate(view_product(allfield=False),start=1):
    B = ttk.Button(F1, text=db[1], command=lambda pd=db: button_insert(pd[0],pd[1],pd[2],1))
    B.grid(row=row, column=col, ipadx=10, ipady=20, padx=5)
    col = col + 1 #col+=1
    if i % 3 == 0:
        col = 0
        row = row + 1

# def apple():
#     v_title.set('Apple')
#     v_price.set('200')
#     v_quantity.set('1')



# B1 = ttk.Button(F1,text='Apple',command=lambda: product('Apple',100))
# B1.grid(row=0,column=0,ipadx=10,ipady=20)

# B2 = ttk.Button(F1,text='Mango',command= lambda: product('Mango',20))
# B2.grid(row=0,column=1,ipadx=10,ipady=20)

# B3 = ttk.Button(F1,text='Orange',command= lambda: product('Orange',30))
# B3.grid(row=0,column=2,ipadx=10,ipady=20)

# GUI.bind('<F1>',lambda x=None: v_quantity.set(float(v_quantity.get())+1))  # Spin up

# zone 2

style = ttk.Style()
style.configure('Treeview.Heading',font=(None,12))

F2 = Frame(T1)
F2.place(x=350,y=50)

v_search = StringVar()
search = ttk.Entry(F2,textvariable=v_search,font=(None,25),width=12)
search.pack(pady=20)

def search_product(event=None):
    barcode = v_search.get()
    data = search_barcode(barcode)
    table_sales.delete(*table_sales.get_children())
    if data[0] not in cart:
        cart[data[0]] = [data[0],data[1],data[2],1]
    else:
        cart[data[0]][3]=cart[data[0]][3] + 1 # เพิ่มครั้งละ 1 ถ้าหากมีข้อมูลอยู่แล้ว
    for c in cart.values():
        table_sales.insert('','end',values=c)
    v_search.set('') #clear data
    search.focus() #ให้ cursor วิ่งไปที่ช่องค้นหา barcode
search.bind('<Return>',search_product)

sales_header = ['barcode','title','price','quantity']
sales_width = [150,200,80,80]

table_sales = ttk.Treeview(F2,columns=sales_header,show='headings',height=10)
table_sales.pack()

for hd,w in zip(sales_header,sales_width):
    table_sales.heading(hd,text=hd)
    table_sales.column(hd,width=w,anchor='center')  # anchor='w'(left)
    
table_sales.column('title',anchor='w')
table_sales.column('price',anchor='e')
table_sales.column('quantity',anchor='e')



#######################TAB2############################
def update_table_product():
    table_product.delete(*table_product.get_children()) #clear data in table
    data = view_product(allfield=False)
    for d in data:
        table_product.insert('','end',values=d)


FT21 = Frame(T2)
FT21.place(x=600,y=30)

L2 = Label(FT21,text='เพิ่มสินค้า',font=FONT1)
L2.pack()

v_barcode2 = StringVar()
v_title2 = StringVar()
v_price2 = StringVar()
v_category2 = StringVar()

L = Label(FT21,text='barcode',font=FONT2).pack()
ET21 = ttk.Entry(FT21,textvariable=v_barcode2,font=FONT2)
ET21.pack()

L = Label(FT21,text='ชื่อสินค้า',font=FONT2).pack()
ET22 = ttk.Entry(FT21,textvariable=v_title2,font=FONT2)
ET22.pack()

L = Label(FT21,text='ราคา',font=FONT2).pack()
ET23 = ttk.Entry(FT21,textvariable=v_price2,font=FONT2)
ET23.pack()

L = Label(FT21,text='ประเภท',font=FONT2).pack()
ET24 = ttk.Entry(FT21,textvariable=v_category2,font=FONT2)
ET24.pack()

def savedata():
    barcode = v_barcode2.get()
    title = v_title2.get()
    price = v_price2.get()
    category = v_category2.get()
    insert_product(barcode,title,price,category)
    v_barcode2.set('')
    v_title2.set('')
    v_price2.set('')
    v_category2.set('')
    view_product()
    update_table_product()
    ET21.focus()

Bsave = ttk.Button(FT21,text='บันทึก',command=savedata)
Bsave.pack(ipadx=20,ipady=10,pady=20)


### ตารางโชว์ข้อมูลสินค้า

FT22 = Frame(T2)
FT22.place(x=50,y=50)

product_header = ['barcode','title','price','category']
product_width = [150,200,50,100]

table_product = ttk.Treeview(FT22,columns=product_header,show='headings',height=10)
table_product.pack()

for hd,w in zip(product_header,product_width):
    table_product.heading(hd,text=hd)
    table_product.column(hd,width=w,anchor='center')  # anchor='w'(left)
    

table_product.column('price',anchor='e')


# insert
# table_product.insert('','end',values=['1001','banana',20,'fruit'])


update_table_product()

GUI.mainloop()
