class Shop_billing_system():
    def __init__(self):
        import pymysql as ms
        self.conn=ms.connect(host='localhost',database='shopdb', user='root', password='9582')
        self.cur=self.conn.cursor()
        print('Database connected successfully!!!')

    def Create_table(self):
        query='show tables'
        self.cur.execute(query)
        try:
            x=[i[0] for i in self.cur]
            if 'product_name' not in x:
                self.cur.execute('create table product_name(P_id int primary key Auto_increment, Name varchar(50), Price float, Stock int)')
                print('Product_name---- table created!')
            else:
                print('welcome back!')
        except Exception as e:
            print('Error:', e)


    def add_product(self):
        try:
            n=input('Enter the Name of product')
            p=float(input('Enter the price'))
            s=int(input('Enter the Stock quantity'))
            query='insert into product_name (Name, Price, Stock)values(%s,%s,%s)'
            self.cur.execute(query,(n,p,s))
            self.conn.commit()
            print(f'Product "{n}"added successfully!')
            self.call()
        except Exception as e:
            print('Error', e)

    def view_all(self):
        self.cur.execute('select * from product_name')
        x=self.cur.fetchall()
        print('\nP_ID|Name|Price|Stock')
        print('--------------------')
        for i in x:
            print(i[0],'|',i[1],'|',i[2],'|',i[3])
        self.call()

    
    def update(self):
        s = int(input('Enter the P_id: '))
        query = 'SELECT * FROM product_name WHERE P_id = %s'  
        self.cur.execute(query, (s,))
        x = self.cur.fetchall()

        print('\nP_ID | Name | Price | Stock')
        print('-----------------------------')

        if x:
            for i in x:
                print(i[0], '|', i[1], '|', i[2], '|', i[3])

            print('\n------ Choose field for updation ------')
            print('Enter 1 for Name\nEnter 2 for Price\nEnter 3 for Stock\nEnter 4 for exits')
            

            t = int(input('Enter choice for field updation: '))

            if t == 1:
                new_value = input('Enter new Name: ')
                query = 'UPDATE product_name SET Name = %s WHERE P_id = %s'
            elif t == 2:
                new_value = float(input('Enter new Price: '))
                query = 'UPDATE product_name SET Price = %s WHERE P_id = %s'
            elif t == 3:
                new_value = int(input('Enter new Stock quantity: ')) 
                query = 'UPDATE product_name SET Stock = %s WHERE P_id = %s'
            elif t==4:
                print('Exist from update')
                self.call()
            else:
                print('Invalid Choice!')  
                self.update()

            self.cur.execute(query, (new_value, s))  
            self.conn.commit()
            print('Product updated successfully!')
            h=input('for reupdate field type Y | For Exist type N')
            if h.upper()=='Y':
                self.update()
            else:
                self.call()
        else:
            print('No record found!\nFor Exist fron Update class Type Y for leave or Type N for Stay')
            c=input('Enter Y/N: ')
            if c.upper()=='Y':
                #Enter return field.
                return
                self.call()
            else:
                print('Enter correct choise: ')
                self.update()

    
    def delete(self):
        d=int(input('Enter the P_id: '))
        query='delete from product_name where P_id=%s'
        self.cur.execute(query,(d,))
        self.conn.commit()
        print('Product deleted Successfully!!')
        self.call()
    
    def search(self):
        s=input('Enter product name:  ')
        query='select* from product_name where Name like %s'
        self.cur.execute(query,(s,))
        x=self.cur.fetchall()
        if x:
            print('-----Product found---')
            for i in x:
                print(i)
            self.call()
        else:
            print('No record found!\nFor Exist fron search Type Y for leave or Type N for Stay')
            c=input('Enter Y/N: ')
            if c.upper()=='Y':
                #Enter return field.
                self.call()
            else:
                print('Enter correct product name: ')
                self.search()


    
    def billing(self):
       self.cur.execute('select * from product_name')
       x = self.cur.fetchall()
       
       print('\nP_ID | Name | Price | Stock')
       print('---------------------------')
       for i in x:
           print(i[0], '|', i[1], '|', i[2], '|', i[3])
           
       s = input('Enter P_ID..:  ')
       query = 'select * from product_name where P_ID = %s'
       self.cur.execute(query, (s,))
       product = self.cur.fetchone()
       if product:
           print(f'Stock Qty   :{product[3]}')
           qty = int(input('Enter the Quantity purchased......: '))
           price = product[2]
           total = qty * price
           
           new_stock = product[3] - qty
           update_query = 'UPDATE product_name SET Stock = %s WHERE P_ID = %s'
           self.cur.execute(update_query, (new_stock, product[0]))
           self.conn.commit()
           
           print("\n----- BILL -----")
           print(f"Product ID   : {product[0]}")
           print(f"Product Name : {product[1]}")
           print(f"Price        : {price}")
           print(f"Quantity     : {qty}")
           print(f"Total Amount : {total}")
           print("----------------")

           choice = input("Do you want to print the bill? (Y/N): ")

           if choice.upper() == 'Y':
               self.print_bill(product, qty, total)
           else:
               print("Bill not printed.")

       else:
           print("No record found!")
           c = input("Type Y to search again or N to exit: ")
           if c.upper() == 'Y':
               self.billing()
           else:
               self.call()

    def print_bill(self, product, qty, total):
        import os
        bill_text = (
            "===== BILL RECEIPT =====\n"
            f"Product ID   : {product[0]}\n"
            f"Product Name : {product[1]}\n"
            f"Price        : {product[2]}\n"
            f"Quantity     : {qty}\n"
            "------------------------\n"
            f"Total Amount : {total}\n"
            "========================\n"
            "Thank You!")

        with open("bill.txt", "w") as f:
            f.write(bill_text)
    
        os.startfile("bill.txt", "print")
        self.call()



    def call(self):
        print('Enter the choice\n1 for View\n2 for Add product\n3 for Update record\n4 for Search product\n5 for Delete product\n6 For Billing\n7 for Exist from store')
        g=int(input('Enter the choice: '))
        if g==1:
            self.view_all()
        elif g==2:
            self.add_product()
        elif g==3:
            self.update()
        elif g==4:
            self.search()
        elif g==5:
            self.delete()
        elif g==6:
            self.billing()
        elif g==7:
            print('Exist from Store')
            


x=Shop_billing_system()
x.call()
