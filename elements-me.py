from tkinter import *
from tkinter import ttk, messagebox
from basicsql import *

class SalesTab(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.cart = {}
        self.setup_variables()
        self.create_widgets()
        
    def setup_variables(self):
        # ตัวแปรเดิม
        self.v_title = StringVar()
        self.v_price = StringVar()
        self.v_quantity = StringVar()
        self.v_result = StringVar()
        self.v_search = StringVar()
        
        # ตัวแปรสำหรับสรุปยอด
        self.v_subtotal = StringVar()
        self.v_vat = StringVar()
        self.v_total = StringVar()
        
        # ตัวแปรสำหรับ checkout
        self.v_paid = StringVar()
        self.v_change = StringVar()
        
        # ตั้งค่าเริ่มต้น
        self.v_subtotal.set('0.00')
        self.v_vat.set('0.00')
        self.v_total.set('0.00')
        self.v_paid.set('0')
        self.v_change.set('0.00')
        
    def create_widgets(self):
        FONT1 = (None, 20)
        FONT2 = (None, 18)
        
        # Title
        L1 = Label(self, text='เมนูสำหรับขาย', font=FONT1)
        L1.pack()
        
        # Style for table
        style = ttk.Style()
        style.configure('Treeview.Heading', font=(None, 12))
        
        # Zone 1 - Product buttons
        self.create_product_zone()
        
        # Zone 2 - Sales zone
        self.create_sales_zone()
        
        # คำนวณครั้งแรก
        self.after(100, self.calculate_summary)
        
    def create_product_zone(self):
        # zone 1
        F1 = Frame(self)
        F1.place(x=20, y=50)
        
        col = 0
        row = 0
        
        try:
            products = view_product(allfield=False)
            for i, db in enumerate(products, start=1):
                # สร้าง function แยกเพื่อแก้ปัญหา lambda closure
                def make_command(product_data):
                    return lambda: self.button_insert(product_data[0], product_data[1], product_data[2], 1)
                
                B = ttk.Button(F1, text=db[1], command=make_command(db))
                B.grid(row=row, column=col, ipadx=10, ipady=20, padx=5)
                col = col + 1
                if i % 3 == 0:
                    col = 0
                    row = row + 1
        except Exception as e:
            Label(F1, text=f'ไม่มีสินค้าในฐานข้อมูล: {e}').pack()
                
    def create_sales_zone(self):
        # zone 2
        F2 = Frame(self)
        F2.place(x=350, y=50)
        
        # Search entry
        self.search_entry = ttk.Entry(F2, textvariable=self.v_search, font=(None, 25), width=12)
        self.search_entry.pack(pady=20)
        self.search_entry.bind('<Return>', self.search_product)
        
        # Sales table
        sales_header = ['barcode', 'title', 'price', 'quantity', 'total']
        sales_width = [120, 150, 80, 80, 100]
        
        self.table_sales = ttk.Treeview(F2, columns=sales_header, show='headings', height=8)
        self.table_sales.pack()
        
        for hd, w in zip(sales_header, sales_width):
            self.table_sales.heading(hd, text=hd)
            self.table_sales.column(hd, width=w, anchor='center')
            
        self.table_sales.column('title', anchor='w')
        self.table_sales.column('price', anchor='e')
        self.table_sales.column('quantity', anchor='e')
        self.table_sales.column('total', anchor='e')
        
        # Summary zone ด้านล่างตาราง
        self.create_summary_zone(F2)
        
    def create_summary_zone(self, parent):
        # Frame สำหรับสรุปยอด - วางด้านล่างตาราง
        F_summary = Frame(parent)
        F_summary.pack(pady=20)
        
        FONT_SUMMARY = (None, 16, 'bold')
        FONT_VALUE = (None, 14)
        
        # Subtotal
        subtotal_frame = Frame(F_summary)
        subtotal_frame.pack(fill='x', pady=2)
        Label(subtotal_frame, text='ยอดรวม (Subtotal):', font=FONT_VALUE).pack(side='left')
        Label(subtotal_frame, textvariable=self.v_subtotal, font=FONT_VALUE).pack(side='right')
        Label(subtotal_frame, text='บาท', font=FONT_VALUE).pack(side='right')
        
        # VAT 7%
        vat_frame = Frame(F_summary)
        vat_frame.pack(fill='x', pady=2)
        Label(vat_frame, text='VAT 7%:', font=FONT_VALUE).pack(side='left')
        Label(vat_frame, textvariable=self.v_vat, font=FONT_VALUE).pack(side='right')
        Label(vat_frame, text='บาท', font=FONT_VALUE).pack(side='right')
        
        # แยกเส้น
        separator = Frame(F_summary, height=2, bg='gray')
        separator.pack(fill='x', pady=5)
        
        # Grand Total
        total_frame = Frame(F_summary)
        total_frame.pack(fill='x', pady=5)
        Label(total_frame, text='รวมทั้งหมด (Grand Total):', font=FONT_SUMMARY, fg='red').pack(side='left')
        Label(total_frame, textvariable=self.v_total, font=FONT_SUMMARY, fg='red').pack(side='right')
        Label(total_frame, text='บาท', font=FONT_SUMMARY, fg='red').pack(side='right')
        
        # Checkout Button
        checkout_frame = Frame(F_summary)
        checkout_frame.pack(fill='x', pady=10)
        self.checkout_btn = ttk.Button(checkout_frame, text='Checkout', command=self.open_checkout)
        self.checkout_btn.pack()
        
    def calculate_summary(self):
        """คำนวณยอดรวม VAT และยอดสุทธิ"""
        subtotal = 0
        
        # คำนวณจากข้อมูลใน cart
        for item in self.cart.values():
            try:
                price = float(item[2])  # แปลงเป็น float เพื่อป้องกัน error
                quantity = int(item[3])  # แปลงเป็น int
                subtotal += price * quantity
            except (ValueError, IndexError):
                continue
            
        vat_amount = subtotal * 0.07  # VAT 7%
        grand_total = subtotal + vat_amount
        
        # อัพเดทการแสดงผล
        self.v_subtotal.set(f'{subtotal:,.2f}')
        self.v_vat.set(f'{vat_amount:,.2f}')
        self.v_total.set(f'{grand_total:,.2f}')
        
        # คำนวณเงินทอนด้วยถ้ามีการป้อนเงิน
        self.calculate_change()
        
        print(f"Debug - Cart: {self.cart}")
        print(f"Debug - Subtotal: {subtotal}, VAT: {vat_amount}, Total: {grand_total}")
        
    def update_cart_display(self):
        """อัพเดทการแสดงผลตะกร้าและคำนวณยอดรวม"""
        self.table_sales.delete(*self.table_sales.get_children())
        
        # แสดงข้อมูลใหม่พร้อม total แต่ละรายการ
        for c in self.cart.values():
            try:
                price = float(c[2])
                quantity = int(c[3])
                total_per_item = price * quantity
                display_data = c + [f'{total_per_item:,.2f}']  # เพิ่ม total ใน list
                self.table_sales.insert('', 'end', values=display_data)
            except (ValueError, IndexError):
                continue
            
        # คำนวณยอดรวมทั้งหมด
        self.calculate_summary()
        
        print(f"Debug - Cart contents: {self.cart}")
        
    def product(self, t, p):
        self.v_title.set(t)
        self.v_price.set(str(p))
        self.v_quantity.set('1')
        
    def button_insert(self, b, t, p, q=1):
        # function เดิม + เพิ่มคำนวณ total
        if b not in self.cart:
            self.cart[b] = [b, t, p, q]
        else:
            self.cart[b][3] = self.cart[b][3] + 1 # เพิ่มครั้งละ 1 ถ้าหากมีข้อมูลอยู่แล้ว
        
        # อัพเดทการแสดงผล
        self.update_cart_display()
            
    def search_product(self, event=None):
        # function เดิม + เพิ่มคำนวณ total
        barcode = self.v_search.get()
        try:
            data = search_barcode(barcode)
            if data[0] not in self.cart:
                self.cart[data[0]] = [data[0], data[1], data[2], 1]
            else:
                self.cart[data[0]][3] = self.cart[data[0]][3] + 1 # เพิ่มครั้งละ 1 ถ้าหากมีข้อมูลอยู่แล้ว
            
            self.v_search.set('') # clear data
            self.search_entry.focus() # ให้ cursor วิ่งไปที่ช่องค้นหา barcode
            
            # อัพเดทการแสดงผล
            self.update_cart_display()
        except:
            messagebox.showerror("Error", "ไม่พบสินค้า")
            self.v_search.set('')
            
    def open_checkout(self):
        """เปิดหน้าต่าง Checkout"""
        if not self.cart:
            messagebox.showwarning("Warning", "ไม่มีสินค้าในตะกร้า")
            return
            
        # สร้าง Toplevel window
        self.checkout_window = Toplevel()
        self.checkout_window.title('ชำระเงิน - Checkout')
        self.checkout_window.geometry('600x700')
        self.checkout_window.transient(self.parent)
        self.checkout_window.grab_set()
        
        # Center window
        self.checkout_window.update_idletasks()
        x = (self.checkout_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.checkout_window.winfo_screenheight() // 2) - (700 // 2)
        self.checkout_window.geometry(f'600x700+{x}+{y}')
        
        self.create_checkout_widgets()
        
    def create_checkout_widgets(self):
        """สร้าง widgets สำหรับหน้า checkout"""
        FONT_TITLE = (None, 18, 'bold')
        FONT_NORMAL = (None, 14)
        FONT_BIG = (None, 24, 'bold')
        
        # Title
        Label(self.checkout_window, text='ระบบชำระเงิน', font=FONT_TITLE, fg='blue').pack(pady=10)
        
        # คำนวณยอดใหม่
        subtotal = sum(float(item[2]) * int(item[3]) for item in self.cart.values())
        vat_amount = subtotal * 0.07
        grand_total = subtotal + vat_amount
        
        # เก็บค่าเพื่อใช้ในการคำนวณ
        self.checkout_total = grand_total
        
        # สรุปยอดขาย - กรอบสีเทา
        summary_frame = Frame(self.checkout_window, relief='solid', bd=1, bg='#f0f0f0')
        summary_frame.pack(fill='x', padx=20, pady=10)
        
        Label(summary_frame, text='สรุปยอดขาย', font=FONT_TITLE, bg='#f0f0f0').pack(pady=5)
        
        subtotal_text = f"ยอดรวม: {subtotal:,.2f} บาท"
        vat_text = f"VAT 7%: {vat_amount:,.2f} บาท"
        total_text = f"รวมทั้งหมด: {grand_total:,.2f} บาท"
        
        Label(summary_frame, text=subtotal_text, font=FONT_NORMAL, bg='#f0f0f0').pack()
        Label(summary_frame, text=vat_text, font=FONT_NORMAL, bg='#f0f0f0').pack()
        Label(summary_frame, text=total_text, font=(None, 16, 'bold'), fg='red', bg='#f0f0f0').pack(pady=5)
        
        # รับเงิน - กรอบสีเทา
        payment_frame = Frame(self.checkout_window, relief='solid', bd=1, bg='#f0f0f0')
        payment_frame.pack(fill='x', padx=20, pady=10)
        
        Label(payment_frame, text='รับเงิน', font=FONT_TITLE, bg='#f0f0f0').pack(pady=5)
        Label(payment_frame, text='ลูกค้าชำระ:', font=FONT_NORMAL, bg='#f0f0f0').pack()
        
        # แสดงจำนวนเงินที่รับ - ตัวเลขใหญ่สีน้ำเงิน
        self.paid_display = Label(payment_frame, textvariable=self.v_paid, font=(None, 32, 'bold'), 
                                 fg='blue', bg='#f0f0f0')
        self.paid_display.pack(pady=10)
        
        # ปุ่มธนบัตร
        Label(payment_frame, text='เลือกธนบัตร:', font=FONT_NORMAL, bg='#f0f0f0').pack()
        
        bills_frame = Frame(payment_frame, bg='#f0f0f0')
        bills_frame.pack(pady=10)
        
        bills = [20, 50, 100, 500, 1000]
        for bill in bills:
            btn = ttk.Button(bills_frame, text=f'{bill}', width=8, 
                           command=lambda b=bill: self.add_bill(b))
            btn.pack(side='left', padx=5)
            
        # ปุ่มเคลียร์
        clear_btn = ttk.Button(bills_frame, text='เคลียร์', width=8, command=self.clear_paid)
        clear_btn.pack(side='left', padx=5)
        
        # หรือกรอกจำนวนเงิน
        manual_frame = Frame(payment_frame, bg='#f0f0f0')
        manual_frame.pack(pady=10)
        Label(manual_frame, text='หรือกรอกจำนวนเงิน:', font=FONT_NORMAL, bg='#f0f0f0').pack()
        
        entry_frame = Frame(manual_frame, bg='#f0f0f0')
        entry_frame.pack(pady=5)
        
        self.manual_entry = ttk.Entry(entry_frame, font=FONT_NORMAL, width=15, justify='center')
        self.manual_entry.pack(side='left', padx=5)
        self.manual_entry.bind('<Return>', self.set_manual_from_entry)
        self.manual_entry.bind('<KeyRelease>', self.on_manual_entry_change)  # เพิ่มการตรวจสอบ real-time
        
        manual_btn = ttk.Button(entry_frame, text='ยืนยัน', command=self.set_manual_from_entry)
        manual_btn.pack(side='left', padx=5)
        
        # เงินทอน - กรอบสีเขียว
        change_frame = Frame(self.checkout_window, relief='solid', bd=2, bg='#e8f5e8')
        change_frame.pack(fill='x', padx=20, pady=10)
        
        Label(change_frame, text='เงินทอน', font=FONT_TITLE, bg='#e8f5e8', fg='green').pack(pady=5)
        
        # สร้าง v_change_checkout สำหรับ checkout window
        self.v_change_checkout = StringVar()
        self.v_change_checkout.set('0.00 บาท')
        
        # แสดงเงินทอนขนาดใหญ่
        self.change_display = Label(change_frame, textvariable=self.v_change_checkout, 
                                   font=(None, 36, 'bold'), fg='green', bg='#e8f5e8')
        self.change_display.pack(pady=15)
        
        # สถานะการชำระเงิน
        self.payment_status = Label(change_frame, text='', font=(None, 14, 'bold'), bg='#e8f5e8')
        self.payment_status.pack(pady=5)
        
        # ปุ่มบันทึกและยกเลิก
        button_frame = Frame(self.checkout_window)
        button_frame.pack(pady=20)
        
        self.save_btn = ttk.Button(button_frame, text='บันทึกการขาย', command=self.save_transaction)
        self.save_btn.pack(side='left', ipadx=20, ipady=10, padx=10)
        
        cancel_btn = ttk.Button(button_frame, text='ยกเลิก', command=self.checkout_window.destroy)
        cancel_btn.pack(side='left', ipadx=20, ipady=10, padx=10)
        
        # คำนวณครั้งแรก
        self.calculate_change_checkout()
        
    def add_bill(self, amount):
        """เพิ่มจำนวนเงินจากการกดปุ่มธนบัตร"""
        current = int(self.v_paid.get()) if self.v_paid.get().isdigit() else 0
        new_amount = current + amount
        self.v_paid.set(str(new_amount))
        self.calculate_change_checkout()
        
    def clear_paid(self):
        """เคลียร์จำนวนเงินที่รับ"""
        self.v_paid.set('0')
        self.manual_entry.delete(0, 'end')  # เคลียร์ entry ด้วย
        self.calculate_change_checkout()
        
    def set_manual_from_entry(self, event=None):
        """ตั้งค่าจำนวนเงินจากการพิมพ์"""
        try:
            amount = float(self.manual_entry.get())
            self.v_paid.set(str(int(amount)))
            self.calculate_change_checkout()
        except ValueError:
            messagebox.showerror("Error", "กรุณาใส่ตัวเลขที่ถูกต้อง")
            
    def on_manual_entry_change(self, event=None):
        """ตรวจสอบการเปลี่ยนแปลงใน manual entry real-time"""
        try:
            if self.manual_entry.get():
                amount = float(self.manual_entry.get())
                self.v_paid.set(str(int(amount)))
                self.calculate_change_checkout()
        except ValueError:
            pass  # ไม่แสดง error ขณะพิมพ์
            
    def calculate_change_checkout(self):
        """คำนวณเงินทอนในหน้า checkout"""
        try:
            paid = int(self.v_paid.get()) if self.v_paid.get().isdigit() else 0
            total = self.checkout_total
            
            change = paid - total
            
            if change >= 0:
                self.v_change_checkout.set(f'{change:,.2f} บาท')
                self.change_display.config(fg='green')
                self.payment_status.config(text='✓ เงินเพียงพอ', fg='green')
                self.save_btn.config(state='normal')  # เปิดใช้งานปุ่มบันทึก
            else:
                shortage = abs(change)
                self.v_change_checkout.set(f'ขาดอีก {shortage:,.2f} บาท')
                self.change_display.config(fg='red')
                self.payment_status.config(text='⚠ เงินไม่เพียงพอ', fg='red')
                self.save_btn.config(state='disabled')  # ปิดการใช้งานปุ่มบันทึก
                
            print(f"Debug Change - Paid: {paid}, Total: {total}, Change: {change}")
        except Exception as e:
            self.v_change_checkout.set('0.00 บาท')
            self.payment_status.config(text='', fg='black')
            self.save_btn.config(state='disabled')
            print(f"Debug Change Error: {e}")
            
    def calculate_change(self):
        """คำนวณเงินทอนสำหรับหน้าหลัก (ถ้าต้องการ)"""
        try:
            paid = int(self.v_paid.get()) if self.v_paid.get().isdigit() else 0
            # ใช้ค่าจาก cart
            subtotal = sum(float(item[2]) * int(item[3]) for item in self.cart.values())
            vat_amount = subtotal * 0.07
            total = subtotal + vat_amount
            
            change = paid - total
            
            if change >= 0:
                self.v_change.set(f'{change:,.2f}')
            else:
                shortage = abs(change)
                self.v_change.set(f'ขาด {shortage:,.2f}')
                    
        except (ValueError, AttributeError) as e:
            self.v_change.set('0.00')
            
    def save_transaction(self):
        """บันทึกการขายลง database"""
        try:
            subtotal = sum(float(item[2]) * int(item[3]) for item in self.cart.values())
            vat_amount = subtotal * 0.07
            grand_total = subtotal + vat_amount
            paid = int(self.v_paid.get()) if self.v_paid.get().isdigit() else 0
            
            if paid < grand_total:
                messagebox.showerror("Error", "เงินที่จ่ายไม่เพียงพอ")
                return
                
            change_amount = paid - grand_total
            
            # สร้างรายการสินค้าเป็น string
            items_str = "; ".join([f"{item[1]} x{item[3]} = {float(item[2])*int(item[3]):.2f}" 
                                 for item in self.cart.values()])
            
            # บันทึกลง database
            insert_transaction(subtotal, vat_amount, grand_total, paid, change_amount, items_str)
            
            # แสดงข้อความยืนยันพร้อมข้อมูลการชำระเงิน
            confirm_message = f"""บันทึกการขายเรียบร้อย
            
ยอดรวม: {subtotal:,.2f} บาท
VAT 7%: {vat_amount:,.2f} บาท
รวมทั้งหมด: {grand_total:,.2f} บาท
รับเงิน: {paid:,.2f} บาท
เงินทอน: {change_amount:,.2f} บาท"""
            
            messagebox.showinfo("Success", confirm_message)
            
            # เคลียร์ตะกร้า
            self.clear_cart()
            self.checkout_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {str(e)}")
            
    def clear_cart(self):
        """เคลียร์ตะกร้าสินค้า"""
        self.cart.clear()
        self.v_paid.set('0')  # รีเซ็ตเงินที่รับด้วย
        self.update_cart_display()


class ProductTab(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_variables()
        self.create_widgets()
        self.update_table_product()
        
    def setup_variables(self):
        self.v_barcode2 = StringVar()
        self.v_title2 = StringVar()
        self.v_price2 = StringVar()
        self.v_category2 = StringVar()
        
    def create_widgets(self):
        FONT1 = (None, 20)
        FONT2 = (None, 18)
        
        # Add product form
        self.create_product_form()
        
        # Product table
        self.create_product_table()
        
    def create_product_form(self):
        FONT1 = (None, 20)
        FONT2 = (None, 18)
        
        FT21 = Frame(self)
        FT21.place(x=600, y=30)
        
        L2 = Label(FT21, text='เพิ่มสินค้า', font=FONT1)
        L2.pack()
        
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
        
        Bsave = ttk.Button(FT21, text='บันทึก', command=self.savedata)
        Bsave.pack(ipadx=20, ipady=10, pady=20)
        
    def create_product_table(self):
        FT22 = Frame(self)
        FT22.place(x=50, y=50)
        
        product_header = ['barcode', 'title', 'price', 'category']
        product_width = [150, 200, 50, 100]
        
        self.table_product = ttk.Treeview(FT22, columns=product_header, show='headings', height=10)
        self.table_product.pack()
        
        for hd, w in zip(product_header, product_width):
            self.table_product.heading(hd, text=hd)
            self.table_product.column(hd, width=w, anchor='center')
            
        self.table_product.column('price', anchor='e')
        
    def savedata(self):
        barcode = self.v_barcode2.get()
        title = self.v_title2.get()
        price = self.v_price2.get()
        category = self.v_category2.get()
        
        if barcode and title and price and category:
            try:
                insert_product(barcode, title, price, category)
                self.v_barcode2.set('')
                self.v_title2.set('')
                self.v_price2.set('')
                self.v_category2.set('')
                self.update_table_product()
                self.ET21.focus()
                messagebox.showinfo("Success", "บันทึกสินค้าเรียบร้อย")
            except Exception as e:
                messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {str(e)}")
        else:
            messagebox.showwarning("Warning", "กรุณากรอกข้อมูลให้ครบถ้วน")
            
    def update_table_product(self):
        self.table_product.delete(*self.table_product.get_children())
        try:
            data = view_product(allfield=False)
            for d in data:
                self.table_product.insert('', 'end', values=d)
        except:
            pass