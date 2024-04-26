import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS EMPLOYEE (
                            EMP_ID INTEGER PRIMARY KEY,
                            Last TEXT,
                            First TEXT,
                            Position TEXT
                            )""")
        self.cur.execute('''CREATE TABLE IF NOT EXISTS PROPERTY (
                            PROPERTY_ID INTEGER PRIMARY KEY,
                            Address TEXT,
                            Manager TEXT
                            )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS UNIT (
                            UNIT_ID INTEGER PRIMARY KEY,
                            UNIT_NUMBER TEXT,
                            Bed INTEGER,
                            Bath INTEGER,
                            Price REAL
                            )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS MAINTENANCE (
                            ID INTEGER PRIMARY KEY,
                            UNIT_ID INTEGER,
                            EMP_ID INTEGER,
                            Date TEXT,
                            Issue TEXT,
                            Status TEXT,
                            FOREIGN KEY (UNIT_ID) REFERENCES UNIT(UNIT_ID),
                            FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID)
                            )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS LEASE (
                            LEASE_ID INTEGER PRIMARY KEY,
                            RENTER_ID INTEGER,
                            EMP_ID INTEGER,
                            UNIT_ID INTEGER,
                            Price REAL,
                            Period TEXT,
                            FOREIGN KEY (RENTER_ID) REFERENCES RENTER(RENTER_ID),
                            FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID),
                            FOREIGN KEY (UNIT_ID) REFERENCES UNIT(UNIT_ID)
                            )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS RENTER (
                            RENTER_ID INTEGER PRIMARY KEY,
                            Last TEXT,
                            First TEXT
                            )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS PAYMENT (
                            PAYMENT_ID INTEGER PRIMARY KEY,
                            LEASE_ID INTEGER,
                            RENTER_ID INTEGER,
                            EMP_ID INTEGER,
                            Period TEXT,
                            Date TEXT,
                            Amount REAL,
                            FOREIGN KEY (LEASE_ID) REFERENCES LEASE(LEASE_ID),
                            FOREIGN KEY (RENTER_ID) REFERENCES RENTER(RENTER_ID),
                            FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID)
                            )''')
        self.conn.commit()

    def add_employee(self, last, first, position):
        self.cur.execute("INSERT INTO EMPLOYEE (Last, First, Position) VALUES (?, ?, ?)", (last, first, position))
        self.conn.commit()
        print("Employee added successfully.")

    def get_employee(self, emp_id):
        self.cur.execute("SELECT * FROM EMPLOYEE WHERE EMP_ID=?", (emp_id,))
        return self.cur.fetchone()

    def update_employee_position(self, emp_id, new_position):
        self.cur.execute("UPDATE EMPLOYEE SET Position=? WHERE EMP_ID=?", (new_position, emp_id))
        self.conn.commit()
        print("Employee position updated successfully.")

    def delete_employee(self, emp_id):
        self.cur.execute("DELETE FROM EMPLOYEE WHERE EMP_ID=?", (emp_id,))
        self.conn.commit()
        print("Employee deleted successfully.")

    def close_connection(self):
        self.conn.close()


# Add a new employee
def add_new_employee(db, last, first, position):
    db.add_employee(last, first, position)


# Lookup a current employee
def lookup_employee(db, emp_id):
    employee = db.get_employee(emp_id)
    print("Retrieved employee:", employee)


# Update an employee's position
def update_employee(db, emp_id, new_position):
    db.update_employee_position(emp_id, new_position)


# Delete an employee
def delete_employee(db, emp_id):
    db.delete_employee(emp_id)


if __name__ == "__main__":
    db = Database('cowboypm.sqlite')

    # #Add a new employee
    # db.add_employee('Doe', 'John', 'Manager')
    #
    # # Lookup a current employee
    # employee = db.get_employee(1)
    # print("Retrieved employee:", employee)
    #
    # # Update an employee's position
    # db.update_employee_position(1, 'Supervisor')
    #
    # # Delete an employee
    # db.delete_employee(1)


class Renter:
   RENTER_ID = None
   name_last = None
   name_first = None


   def __init__(self, RENTER_ID, Last, First):
       self.RENTER_ID = RENTER_ID
       self.name_last = Last
       self.name_first = First


   def lookup_renter_info(self):
       print("Renter name: " +self.name_first+ " " +self.name_last)
       print("Renter ID: " +self.RENTER_ID)




class Employee:


   name_first = None
   name_last = None
   EMP_ID = None
   position = None


   def __init__(self, name_first, name_last, EMP_ID, position):
       self.name_first = name_first
       self.name_last = name_last
       self.EMP_ID = EMP_ID
       self.position = position


   def lookup_emp_info(self):
       print("Employee name: " +self.name_first+ " " +self.name_last)
       print("Employee ID: " +self.EMP_ID)
       print("Employee position: " +self.position)




emp_1 = Employee("John", "Doe", "1", "Admin")
emp_2 = Employee("Fred", "Holly", "2", "Employee")




# print(emp_1.name_first)
# print(emp_1.name_last)
# print(emp_1.EMP_ID)
# print(emp_1.position)
emp_1.lookup_emp_info()
