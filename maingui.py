from tkinter import *
from tkinter import ttk, messagebox
import os
from basicsql import *
from elements import SalesTab, ProductTab

GUI = Tk()
w = 1000
h = 700

ws = GUI.winfo_screenwidth()
hs = GUI.winfo_screenheight()

x = (ws/2)-(w/2)
y = (hs/2)-(h/2)

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')
GUI.title('โปรแกรมขายของร้านลุง')

##########MENU###########
menubar = Menu(GUI)
GUI.config(menu=menubar)

#File Menu
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='เปิดเมนูเพิ่มสินค้า', command=lambda: print('Add Product'))
filemenu.add_command(label='ออกจากโปรแกรม', command=lambda: GUI.quit())

#About Menu
def AboutMenu(event=None):
    GUI2 = Toplevel()
    w = 500
    h = 300
    
    ws = GUI.winfo_screenwidth()
    hs = GUI.winfo_screenheight()
    
    x = (ws/2)-(w/2)
    y = (hs/2)-(h/2)
    
    GUI2.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')
    
    try:
        uncle_icon = PhotoImage(file='uncle.png').subsample(2)
        Label(GUI2, image=uncle_icon).pack()
    except:
        pass  # ถ้าไม่มีไฟล์รูปก็ข้าม
    
    Label(GUI2, text='โปรแกรมนี้เป็นโปรแกรมสำหรับขายของ\nคุณสามารถใช้งานได้ฟรี ไม่มีค่าใช้จ่าย\nTel: 0812345678').pack()
    
    GUI2.mainloop()

aboutmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='About', menu=aboutmenu)
aboutmenu.add_command(label='เกี่ยวกับโปรแกรม', command=AboutMenu)

GUI.bind('<F12>', AboutMenu)

##########TAB###########
Tab = ttk.Notebook(GUI)
Tab.pack(fill=BOTH, expand=1)

# สร้าง Tab โดยใช้ Class
sales_tab = SalesTab(Tab)
product_tab = ProductTab(Tab)

# เพิ่ม Tab พร้อม icon (ถ้ามี)
try:
    tab_icon1 = PhotoImage(file='tab1.png')
    tab_icon2 = PhotoImage(file='tab2.png')
    Tab.add(sales_tab, text='เมนูขาย', image=tab_icon1, compound='left')
    Tab.add(product_tab, text='เพิ่มสินค้า', image=tab_icon2, compound='left')
except:
    # ถ้าไม่มีไฟล์รูปก็ใช้ข้อความอย่างเดียว
    Tab.add(sales_tab, text='เมนูขาย')
    Tab.add(product_tab, text='เพิ่มสินค้า')

GUI.mainloop()