import mysql.connector
from mysql.connector import Error


class Reapir_DB:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(host='localhost',
                                        database='repair_db',
                                        user='root',
                                        password='12345678')
            if self.connection.is_connected():
                self.db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", self.db_Info)
                self.cursor = self.connection.cursor()
                self.cursor.execute("select database();")
                self.record = self.cursor.fetchone()
                print("You're connected to database: ", self.record)
        except Error as e:
            print("Error while connecting to MySQL", e)
    def __del__(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")

    def print_exec(self, sql):
        print("===================SQL-Query=======================")
        print(sql)
        print("-------------------Result--------------------------")
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print(result)
        print("===================================================")

    def first_simple(self, command): #Show Device names where owners have certain name
        sql_query = f"SELECT Name FROM Devices WHERE ID in (SELECT Device_ID FROM Ownership_document WHERE Owner_ID IN (SELECT ID FROM Clients WHERE Person_ID IN(SELECT ID FROM Persons WHERE First_Name = '{command}')))"
        self.print_exec(sql_query)

    def second_simple(self, command): #show emails of clients that own device with certain problem
        sql_query = f"SELECT Email FROM Clients WHERE ID in (SELECT Owner_ID FROM Ownership_document WHERE Device_ID in (SELECT ID FROM Devices WHERE Breakage = '{command}'))"
        self.print_exec(sql_query)

    def third_simple(self, command): #show salaries of all masters that have certain specialization
        sql_query = f"SELECT Salary FROM Masters WHERE ID in (SELECT Master_ID FROM Specialization WHERE Service_ID in (SELECT ID FROM Services WHERE Services_name = '{command}'))"
        self.print_exec(sql_query)

    def fourth_simple(self, command): #show show Last names of all Clients that have contract with certain Status (1, 2, 3)
        sql_query = f"SELECT Last_name FROM Persons WHERE ID in (SELECT Person_ID FROM Clients WHERE ID in (SELECT Client_ID FROM Contract WHERE Status = {command}))"
        self.print_exec(sql_query)

    def fifth_simple(self, command): #Show Masters last names where salary is bigger than certain value
        sql_query = f"SELECT Last_name FROM Persons WHERE ID in (SELECT Person_ID FROM Masters WHERE Salary > {command})"
        self.print_exec(sql_query)

    def execute(self):
        command = ""
        while True:
            print("Put 1/2/3/4/5 for first/second/third/fourth/fifth simple query:")
            command = input()
            print("")
            if command == "STOP":
                break
            elif command == "1":
                print("Show Device names where owners have certain name")
                print("input arguments:")
                command = input()
                self.first_simple(command)
            elif command == "2":
                print("Show emails of clients that own device with certain problem")
                print("input arguments:")
                command = input()
                self.second_simple(command)  
            elif command == "3":
                print("Show salaries of all masters that have certain specialization")
                print("input arguments:")
                command = input()
                self.third_simple(command)
            elif command == "4":
                print("Show show Last names of all Clients that have contract with certain Status (1, 2, 3)")
                print("input arguments:")
                command = input()
                self.fourth_simple(command)
            elif command == "5":
                print("Show Masters last names where salary is bigger than certain value")
                print("input arguments:")
                command = input()
                self.fifth_simple(command)
    




def main():
    db = Reapir_DB()
    db.execute()

if __name__ == "__main__":
    main()

