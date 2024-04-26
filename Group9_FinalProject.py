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


def main():
    db = Database('cowboypm.sqlite')
    user_management = UserManagement()

    print("\n=== Welcome to the Cowboy Property Management System ===")
    print("Select a login mode:")
    print("1. Admin")
    print("2. Employee")
    print("3. Renter")
    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        role = 'admin'
    elif choice == '2':
        role = 'employee'
    elif choice == '3':
        role = 'renter'
    else:
        print("Invalid choice. Exiting.")
        return

    print(f"=== {role.capitalize()} Login ===")
    username = input("Enter username: ")
    password = input("Enter password: ")

    authenticated_role = user_management.authenticate(username, password)
    if authenticated_role == role:
        print(f"Welcome, {username}! You are logged in as a {role}.")
        if role == 'admin':
            admin_menu(db)
        elif role == 'employee':
            employee_menu(db)
        elif role == 'renter':
            renter_menu(db)
        else:
            print("Invalid user role.")
    else:
        print("Invalid username or password. Please try again.")

    db.close_connection()

if __name__ == "__main__":
    main()
