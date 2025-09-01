from tkinter import *
from tkinter import ttk, messagebox
import os
from elements import SalesTab, ProductTab

GUI = Tk()
w = 900
h = 550

ws = GUI.winfo_screenwidth()
hs = GUI.winfo_screenheight()

x = (ws/2)-(w-2) 
y = (hs/2)-(h-2)
 
GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')
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

    try:
        jipjip_icon = PhotoImage(file='jipjip.png').subsample(2)
        Label(GUI2,image=jipjip_icon).pack()
    except:
        pass

    Label(GUI2,text='โปรแกรมสำหรับขายของ by jipjipstore\nTel: 0907437633').pack()

    GUI2.mainloop()

aboutmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='About',menu=aboutmenu)
aboutmenu.add_command(label='เกี่ยวกับโปรแกรม',command=AboutMenu)

GUI.bind('<F2>',AboutMenu)

################TAB####################
Tab = ttk.Notebook(GUI)
Tab.pack(fill=BOTH,expand=1)

#สร้าง Frame สำหรับแต่ละแท็บ
T1 = Frame(Tab)
T2 = Frame(Tab)

# สร้าง instance ของ class
sales_tab = SalesTab(Tab)
product_tab = ProductTab(Tab)

# เพิ่ม Tab พร้อม icon
try:
    tab_icon1 = PhotoImage(file='tab1.png')
    tab_icon2 = PhotoImage(file='tab2.png')
    Tab.add(sales_tab, text='เมนูขาย', image=tab_icon1, compound='left')
    Tab.add(product_tab, text='เพิ่มสินค้า', image=tab_icon2, compound='left')
except:
    # ถ้าหา icon ไม่เจอ ใช้ text อย่างเดียว
    Tab.add(sales_tab, text='เมนูขาย')
    Tab.add(product_tab, text='เพิ่มสินค้า')

GUI.mainloop()