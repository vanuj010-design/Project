class attendence():
    def __init__(self):
        import pymysql as ms
        self.conn=ms.connect(host='localhost', user='root', database='anuj', password='9582')
        self.cur=self.conn.cursor()
        self.d_=int(input('Enter the date in format: ddmmyyyy'))

    def table(self):
        query='show tables'
        self.cur.execute(query)
        try:
            x=[i[0] for i in self.cur]
            if 'attendence' not in x:
                self.cur.execute('create table attendence (id int not null, batch_id varchar(30), name varchar(30), gender varchar(1),date int, attendence varchar(1),primary key (id, date))')
                print('New tabele created')
            else:
                print('welcome back')
        except Exception as e:
            print('Error:', e)

    def new_admission(self):
        i1=input('If there is new addmission (Y/N)')
        if i1.upper() =='Y':
            print('enter new student detail')
            self.detail()
        else:
            print('Take attendence for left student on date',self.d_)
            self.con_attendence()

    def detail(self):
        si=int(input('Enter Student ID: '))
        bi=input('Enter batch ID: ')
        sn=input('Enter Full name: ')
        g=input('Enter gender')
        a=input('Enter the attendence')
        
        sub = input('Enter "S" to submit detail or "N" to cancel: ')
        if sub.upper() == 'S':
            query = 'INSERT INTO attendence (id, batch_id, name, gender, date, attendence) VALUES (%s, %s, %s, %s, %s, %s)'
            self.cur.execute(query, (si, bi, sn, g, self.d_, a))
            self.conn.commit()
            print('Record added successfully.')
            self.new_admission()
        

    def con_attendence(self):
        print('\n----Taking attandence for rest of student---')
        self.cur.execute('select distinct id, batch_id, name, gender from attendence')
        all_student= self.cur.fetchall()
        for i in all_student:
            si, bi, sn, g=i
            self.cur.execute('select * from attendence where id=%s and date=%s',(si, self.d_))
            result= self.cur.fetchone()
            if result:
                continue
            print(f'\nID: {si}, Name: {sn}')
            a = input('Enter attendance (P/A): ')
            query = 'INSERT INTO attendence (id, batch_id, name, gender, date, attendence) VALUES (%s, %s, %s, %s, %s, %s)'
            self.cur.execute(query, (si, bi, sn, g, self.d_, a))
            self.conn.commit()

        print('\n Attendance completed for all students.')
        
                
        
x=attendence()
x.table()
x.new_admission()