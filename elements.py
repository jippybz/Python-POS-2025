from tkinter import *
from tkinter import ttk, messagebox
from basicsql import *

class SalesTab(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.cart = {}
        self.setup_ui()
        
    def setup_ui(self):
        FONT1 = (None, 20)
        FONT2 = (None, 18)
        
        # หัวข้อ
        L1 = Label(self, text='เมนูสำหรับขาย', font=FONT1)
        L1.pack()
        
        # ตัวแปร
        self.v_search = StringVar()
        
        # Frame สำหรับปุ่มสินค้า
        F1 = Frame(self)
        F1.place(x=20, y=50)
        
        # สร้างปุ่มสินค้าจากฐานข้อมูล
        self.create_product_buttons(F1)
        
        # Frame สำหรับค้นหาและตาราง
        F2 = Frame(self)
        F2.place(x=350, y=50)
        
        # ช่องค้นหา barcode
        self.search = ttk.Entry(F2, textvariable=self.v_search, font=(None, 25), width=12)
        self.search.pack(pady=20)
        self.search.bind('<Return>', self.search_product)
        
        # ตารางแสดงสินค้าในตะกร้า
        self.setup_sales_table(F2)
        
        # Frame สำหรับสรุปยอดขาย
        self.setup_summary_section(F2)
        
        # ปุ่ม Checkout
        self.setup_checkout_button(F2)
        
    def create_product_buttons(self, parent):
        """สร้างปุ่มสินค้าจากฐานข้อมูล"""
        col = 0
        row = 0
        
        for i, db in enumerate(view_product(allfield=False), start=1):
            B = ttk.Button(parent, text=db[1], 
                          command=lambda pd=db: self.button_insert(pd[0], pd[1], pd[2], 1))
            B.grid(row=row, column=col, ipadx=10, ipady=20, padx=5)
            col += 1
            if i % 3 == 0:
                col = 0
                row += 1
                
    def setup_sales_table(self, parent):
        """สร้างตารางแสดงสินค้าในตะกร้า"""
        # หัวข้อตาราง (เพิ่ม total)
        sales_header = ['barcode', 'title', 'price', 'quantity', 'total']
        sales_width = [120, 180, 70, 70, 90]
        
        self.table_sales = ttk.Treeview(parent, columns=sales_header, show='headings', height=10)
        self.table_sales.pack(pady=(0, 10))
        
        for hd, w in zip(sales_header, sales_width):
            self.table_sales.heading(hd, text=hd)
            self.table_sales.column(hd, width=w, anchor='center')
            
        # จัดตำแหน่งคอลัมน์
        self.table_sales.column('title', anchor='w')
        self.table_sales.column('price', anchor='e')
        self.table_sales.column('quantity', anchor='e')
        self.table_sales.column('total', anchor='e')
        
    def setup_summary_section(self, parent):
        """สร้างส่วนสรุปยอดขาย"""
        # Frame สำหรับสรุปยอด
        summary_frame = Frame(parent)
        summary_frame.pack(anchor='e', padx=10, pady=10)
        
        # ตัวแปรสำหรับแสดงยอด
        self.v_subtotal = StringVar(value="0.00")
        self.v_vat = StringVar(value="0.00")
        self.v_grand_total = StringVar(value="0.00")
        
        # แสดงยอดรวม
        Label(summary_frame, text='ยอดรวม:', font=(None, 14)).grid(row=0, column=0, sticky='e', padx=5)
        Label(summary_frame, textvariable=self.v_subtotal, font=(None, 14, 'bold')).grid(row=0, column=1, sticky='e', padx=5)
        Label(summary_frame, text='บาท', font=(None, 14)).grid(row=0, column=2, sticky='w')
        
        # แสดง VAT 7%
        Label(summary_frame, text='VAT 7%:', font=(None, 14)).grid(row=1, column=0, sticky='e', padx=5)
        Label(summary_frame, textvariable=self.v_vat, font=(None, 14, 'bold')).grid(row=1, column=1, sticky='e', padx=5)
        Label(summary_frame, text='บาท', font=(None, 14)).grid(row=1, column=2, sticky='w')
        
        # เส้นแบ่ง
        ttk.Separator(summary_frame, orient='horizontal').grid(row=2, column=0, columnspan=3, sticky='ew', pady=5)
        
        # แสดงยอดรวมทั้งหมด
        Label(summary_frame, text='รวมทั้งหมด:', font=(None, 16, 'bold')).grid(row=3, column=0, sticky='e', padx=5)
        Label(summary_frame, textvariable=self.v_grand_total, font=(None, 16, 'bold'), fg='red').grid(row=3, column=1, sticky='e', padx=5)
        Label(summary_frame, text='บาท', font=(None, 16, 'bold')).grid(row=3, column=2, sticky='w')
        
    def button_insert(self, barcode, title, price, quantity=1):
        """เพิ่มสินค้าลงตะกร้า"""
        if barcode not in self.cart:
            self.cart[barcode] = [barcode, title, price, quantity]
        else:
            self.cart[barcode][3] += 1  # เพิ่มจำนวน
            
        self.update_cart_display()
        
    def search_product(self, event=None):
        """ค้นหาสินค้าด้วย barcode"""
        try:
            barcode = self.v_search.get()
            if barcode:
                data = search_barcode(barcode)
                if data:
                    self.button_insert(data[0], data[1], data[2], 1)
                    self.v_search.set('')  # ล้างข้อมูล
                    self.search.focus()  # focus กลับไปที่ช่องค้นหา
                else:
                    messagebox.showwarning("ไม่พบสินค้า", f"ไม่พบสินค้า barcode: {barcode}")
        except Exception as e:
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {str(e)}")
            
    def update_cart_display(self):
        """อัพเดทการแสดงผลตะกร้าและสรุปยอด"""
        # ล้างตาราง
        self.table_sales.delete(*self.table_sales.get_children())
        
        # เพิ่มข้อมูลในตะกร้าพร้อมคำนวณยอดรวมแต่ละรายการ
        subtotal = 0
        for item in self.cart.values():
            barcode, title, price, quantity = item
            total_per_item = price * quantity
            subtotal += total_per_item
            
            # เพิ่มข้อมูลลงตาราง (เพิ่มคอลัมน์ total)
            self.table_sales.insert('', 'end', values=[
                barcode, title, f"{price:,.2f}", quantity, f"{total_per_item:,.2f}"
            ])
        
        # คำนวณและแสดงสรุปยอด
        self.calculate_summary(subtotal)
        
    def calculate_summary(self, subtotal):
        """คำนวณและแสดงสรุปยอดขาย"""
        vat = subtotal * 0.07  # VAT 7%
        grand_total = subtotal + vat
        
        # อัพเดทการแสดงผล
        self.v_subtotal.set(f"{subtotal:,.2f}")
        self.v_vat.set(f"{vat:,.2f}")
        self.v_grand_total.set(f"{grand_total:,.2f}")
        
    def setup_checkout_button(self, parent):
        """สร้างปุ่ม Checkout"""
        checkout_frame = Frame(parent)
        checkout_frame.pack(anchor='e', padx=10, pady=10)
        
        self.checkout_btn = ttk.Button(checkout_frame, text='Checkout', 
                                      command=self.open_checkout_window,
                                      style='Accent.TButton')
        self.checkout_btn.pack(ipadx=30, ipady=10)
        
    def open_checkout_window(self):
        """เปิดหน้าต่าง Checkout"""
        if not self.cart:
            messagebox.showwarning("ตะกร้าว่าง", "กรุณาเลือกสินค้าก่อนทำการ Checkout")
            return
            
        # สร้างหน้าต่าง Checkout
        self.checkout_window = Toplevel(self)
        self.checkout_window.title('ระบบชำระเงิน')
        self.checkout_window.geometry('500x700')
        self.checkout_window.resizable(False, False)
        
        # ทำให้หน้าต่างอยู่กลางหน้าจอ
        self.checkout_window.transient(self.master)
        self.checkout_window.grab_set()
        
        self.setup_checkout_ui()
        
    def setup_checkout_ui(self):
        """สร้าง UI สำหรับหน้าต่าง Checkout"""
        # คำนวณยอดรวม
        subtotal = sum(item[2] * item[3] for item in self.cart.values())
        vat = subtotal * 0.07
        grand_total = subtotal + vat
        
        # หัวข้อ
        Label(self.checkout_window, text='สรุปยอดขาย', font=(None, 20, 'bold')).pack(pady=20)
        
        # แสดงสรุปยอด
        summary_frame = Frame(self.checkout_window)
        summary_frame.pack(pady=10)
        
        Label(summary_frame, text=f'ยอดรวม: {subtotal:,.2f} บาท', font=(None, 14)).pack(anchor='e')
        Label(summary_frame, text=f'VAT 7%: {vat:,.2f} บาท', font=(None, 14)).pack(anchor='e')
        Label(summary_frame, text=f'รวมทั้งหมด: {grand_total:,.2f} บาท', 
              font=(None, 16, 'bold'), fg='red').pack(anchor='e', pady=5)
        
        # เส้นแบ่ง
        ttk.Separator(self.checkout_window, orient='horizontal').pack(fill='x', pady=10)
        
        # ส่วนรับเงิน
        Label(self.checkout_window, text='รับเงิน', font=(None, 16, 'bold')).pack()
        
        # ตัวแปรสำหรับเก็บยอดเงิน
        self.v_paid = StringVar(value="0")
        self.v_change = StringVar(value="0.00")
        self.grand_total = grand_total
        
        # แสดงยอดเงินที่รับ
        paid_frame = Frame(self.checkout_window)
        paid_frame.pack(pady=10)
        
        Label(paid_frame, text='ยอดเงินที่รับ:', font=(None, 14)).grid(row=0, column=0, padx=5)
        self.paid_entry = ttk.Entry(paid_frame, textvariable=self.v_paid, font=(None, 16), width=15)
        self.paid_entry.grid(row=0, column=1, padx=5)
        self.paid_entry.bind('<KeyRelease>', self.calculate_change)
        
        Label(paid_frame, text='บาท', font=(None, 14)).grid(row=0, column=2)
        
        # ปุ่มธนบัตร
        money_frame = Frame(self.checkout_window)
        money_frame.pack(pady=20)
        
        Label(money_frame, text='ธนบัตร:', font=(None, 14)).pack()
        
        bills_frame = Frame(money_frame)
        bills_frame.pack(pady=10)
        
        bills = [20, 50, 100, 500, 1000]
        for i, bill in enumerate(bills):
            btn = ttk.Button(bills_frame, text=f'{bill}', 
                           command=lambda b=bill: self.add_money(b),
                           width=8)
            btn.grid(row=0, column=i, padx=5, pady=5)
            
        # ปุ่มล้างและเพิ่มเงิน
        control_frame = Frame(money_frame)
        control_frame.pack(pady=10)
        
        ttk.Button(control_frame, text='ล้าง', command=self.clear_money, width=10).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text='จ่ายพอดี', command=self.exact_amount, width=10).grid(row=0, column=1, padx=5)
        
        # แสดงเงินทอน
        change_frame = Frame(self.checkout_window)
        change_frame.pack(pady=20)
        
        Label(change_frame, text='เงินทอน:', font=(None, 16, 'bold')).grid(row=0, column=0, padx=10)
        Label(change_frame, textvariable=self.v_change, font=(None, 18, 'bold'), 
              fg='green', bg='lightgray', relief='sunken', width=15).grid(row=0, column=1, padx=10)
        Label(change_frame, text='บาท', font=(None, 16, 'bold')).grid(row=0, column=2)
        
        # ปุ่มบันทึกและยกเลิก
        button_frame = Frame(self.checkout_window)
        button_frame.pack(pady=30)
        
        self.save_btn = ttk.Button(button_frame, text='บันทึกการขาย', 
                                  command=self.save_transaction,
                                  style='Accent.TButton')
        self.save_btn.pack(side='left', ipadx=20, ipady=10, padx=10)
        
        ttk.Button(button_frame, text='ยกเลิก', 
                  command=self.checkout_window.destroy).pack(side='left', ipadx=20, ipady=10, padx=10)
        
        # focus ที่ช่องรับเงิน
        self.paid_entry.focus()
        
    def add_money(self, amount):
        """เพิ่มยอดเงินตามธนบัตรที่เลือก"""
        current = float(self.v_paid.get() or 0)
        new_amount = current + amount
        self.v_paid.set(str(new_amount))
        self.calculate_change()
        
    def clear_money(self):
        """ล้างยอดเงิน"""
        self.v_paid.set("0")
        self.calculate_change()
        
    def exact_amount(self):
        """จ่ายเงินพอดี"""
        self.v_paid.set(str(self.grand_total))
        self.calculate_change()
        
    def calculate_change(self, event=None):
        """คำนวณเงินทอน"""
        try:
            paid = float(self.v_paid.get() or 0)
            change = paid - self.grand_total
            self.v_change.set(f"{change:,.2f}")
            
            # เปลี่ยนสีตามผลลัพธ์
            try:
                change_label = self.checkout_window.nametowidget(self.checkout_window.winfo_children()[-2].winfo_children()[0].winfo_children()[1])
                if change < 0:
                    change_label.config(fg='red')
                    self.save_btn.config(state='disabled')
                else:
                    change_label.config(fg='green')
                    self.save_btn.config(state='normal')
            except:
                # ถ้าไม่สามารถเข้าถึง widget ได้ ให้ทำแค่เปิด/ปิดปุ่มบันทึก
                if change < 0:
                    self.save_btn.config(state='disabled')
                else:
                    self.save_btn.config(state='normal')
                
        except ValueError:
            self.v_change.set("0.00")
            self.save_btn.config(state='disabled')
    
    def clear_cart(self):
        """ล้างสินค้าในตะกร้า - เพิ่ม method ที่หายไป"""
        self.cart = {}
        self.update_cart_display()
            
    def save_transaction(self):
        """บันทึกการขายลงฐานข้อมูล"""
        try:
            # คำนวณยอดต่างๆ
            subtotal = sum(item[2] * item[3] for item in self.cart.values())
            vat = subtotal * 0.07
            total = subtotal + vat
            paid = float(self.v_paid.get())
            change_amount = paid - total
            
            # สร้าง JSON string ของสินค้าที่ขาย
            import json
            items_data = []
            for item in self.cart.values():
                items_data.append({
                    'barcode': item[0],
                    'title': item[1],
                    'price': item[2],
                    'quantity': item[3],
                    'total': item[2] * item[3]
                })
            items_json = json.dumps(items_data, ensure_ascii=False)
            
            # บันทึกลงฐานข้อมูล
            insert_transaction(subtotal, vat, total, paid, change_amount, items_json)
            
            # แสดงข้อความสำเร็จ
            messagebox.showinfo("สำเร็จ", f"บันทึกการขายเรียบร้อย\nเงินทอน: {change_amount:,.2f} บาท")
            
            # ล้างตะกร้าและปิดหน้าต่าง
            self.clear_cart()
            self.checkout_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"เกิดข้อผิดพลาดในการบันทึก: {str(e)}")


class ProductTab(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        FONT1 = (None, 20)
        FONT2 = (None, 18)
        
        # Frame สำหรับเพิ่มสินค้า
        FT21 = Frame(self)
        FT21.place(x=600, y=50)
        
        L2 = Label(FT21, text='เพิ่มสินค้า', font=FONT1)
        L2.pack(pady=20)
        
        # ตัวแปร
        self.v_barcode2 = StringVar()
        self.v_title2 = StringVar()
        self.v_price2 = StringVar()
        self.v_category2 = StringVar()
        self.v_category2.set('fruit')
        
        # ฟอร์มเพิ่มสินค้า
        Label(FT21, text='barcode', font=FONT2).pack()
        self.ET21 = ttk.Entry(FT21, textvariable=self.v_barcode2, font=FONT2)
        self.ET21.pack()
        
        Label(FT21, text='ชื่อสินค้า', font=FONT2).pack()
        self.ET22 = ttk.Entry(FT21, textvariable=self.v_title2, font=FONT2)
        self.ET22.pack()
        
        Label(FT21, text='ราคา', font=FONT2).pack()
        self.ET23 = ttk.Entry(FT21, textvariable=self.v_price2, font=FONT2)
        self.ET23.pack()
        
        Label(FT21, text='ประเภท', font=FONT2).pack()
        self.ET24 = ttk.Entry(FT21, textvariable=self.v_category2, font=FONT2)
        self.ET24.pack()
        
        # ปุ่มบันทึก
        Bsave = ttk.Button(FT21, text='บันทึก', command=self.savedata)
        Bsave.pack(ipadx=20, ipady=10, pady=20)
        
        # ตารางแสดงสินค้า
        self.setup_product_table()
        self.update_table_product()
        
    def setup_product_table(self):
        """สร้างตารางแสดงสินค้า"""
        FT22 = Frame(self)
        FT22.place(x=20, y=50)
        
        product_header = ['barcode', 'title', 'price', 'category']
        product_width = [150, 200, 50, 100]
        
        self.table_product = ttk.Treeview(FT22, columns=product_header, show='headings', height=10)
        self.table_product.pack()
        
        for hd, w in zip(product_header, product_width):
            self.table_product.heading(hd, text=hd)
            self.table_product.column(hd, width=w, anchor='center')
            
        self.table_product.column('price', anchor='e')
        
    def savedata(self):
        """บันทึกข้อมูลสินค้าใหม่"""
        try:
            barcode = self.v_barcode2.get()
            title = self.v_title2.get()
            price = self.v_price2.get()
            category = self.v_category2.get()
            
            if not all([barcode, title, price, category]):
                messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
                return
                
            # ตรวจสอบราคาเป็นตัวเลข
            try:
                float(price)
            except ValueError:
                messagebox.showerror("ข้อมูลผิดพลาด", "ราคาต้องเป็นตัวเลข")
                return
                
            insert_product(barcode, title, price, category)
            
            # ล้างข้อมูลในฟอร์ม
            self.v_barcode2.set('')
            self.v_title2.set('')
            self.v_price2.set('')
            self.v_category2.set('fruit')
            
            # อัพเดทตาราง
            self.update_table_product()
            self.ET21.focus()
            
            messagebox.showinfo("สำเร็จ", "บันทึกข้อมูลสินค้าเรียบร้อย")
            
        except Exception as e:
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {str(e)}")
            
    def update_table_product(self):
        """อัพเดทตารางแสดงสินค้า"""
        self.table_product.delete(*self.table_product.get_children())
        data = view_product(allfield=False)
        for d in data:
            self.table_product.insert('', 'end', values=d)