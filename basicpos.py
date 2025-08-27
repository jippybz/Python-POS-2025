from tkinter import *
from tkinter import ttk, messagebox

GUI = Tk()
GUI.geometry('500x400')
GUI.title('ยายน้อยการค้า')

L1 = Label(GUI,text='ยายน้อยการค้า',font=('tahoma',20))
L1.pack()

#-----------------------------------------
def apple():
    text='แอปเปิ้ลนำเข้านิวซีแลนด์ ราคากิโลกรัมละ 100 บาท'
    messagebox.showinfo('ข้อมูลสินค้า',text)


B1 = ttk.Button(GUI,text='แอปเปิ้ล',command=apple)
B1.pack(ipadx=20,ipady=20)
#-----------------------------------------
def mango():
    text='มะม่วงเขียวเสวย ราคากิโลกรัมละ 10 บาท'
    messagebox.showinfo('ข้อมูลสินค้า',text)


B2 = ttk.Button(GUI,text='มะม่วง',command=mango)
B2.pack(ipadx=20,ipady=20)
#-----------------------------------------
def durian():
    text='ทุเรียนหมอนทองพรีเมียม ราคากิโลกรัมละ 300 บาท'
    messagebox.showinfo('ข้อมูลสินค้า',text)


B3 = ttk.Button(GUI,text='ทุเรียน',command=durian)
B3.pack(ipadx=20,ipady=20)
#-----------------------------------------
def grape():
    text='องุ่นเคียวโฮ ราคากิโลกรัมละ 150 บาท'
    messagebox.showinfo('ข้อมูลสินค้า',text)


B4 = ttk.Button(GUI,text='องุ่น',command=grape)
B4.pack(ipadx=20,ipady=20)



GUI.mainloop()
