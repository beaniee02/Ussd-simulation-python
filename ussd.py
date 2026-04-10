import mysql.connector as sql
import random
import sys

class Bank:

    def __init__(self):
        self.my_con = sql.connect(host='127.0.0.1', username='root', password='busolami2003@', db='bank')

        self.my_cursor = self.my_con.cursor()

        self.my_cursor.execute("CREATE TABLE IF NOT EXISTS register(customer_id INT(2) PRIMARY KEY AUTO_INCREMENT, fname VARCHAR(20), lname VARCHAR(20), dob VARCHAR(8), phonenum VARCHAR(11), email VARCHAR(50), residential_address VARCHAR(50))")
        self.my_con.commit()

        


        # self.my_cursor.execute('ALTER TABLE register ADD balance INT(5)')
        # self.my_con.commit()
        # print('column renamed successfully')

        # self.my_cursor.execute('ALTER TABLE register ADD PIN INT(4) UNIQUE')
        # self.my_con.commit()
        # print('column added successfully')

        # self.my_request = "SELECT * FROM register"
        # self.my_cursor.execute(self.my_request)
        # for each in self.my_cursor.fetchall():
        #     print(each)

        # self.my_query = "UPDATE register SET balance = 20000, PIN = 1903 WHERE email=%s"
        # self.my_val = ('jibola@gmail.com', )
        # self.my_cursor.execute(self.my_query, self.my_val)
        # self.my_con.commit()
        # print('jibola"s balance is updated successfully')

        # self.query = "DELETE FROM register WHERE email=%s"
        # self.val = ('busolami@gmail.com',)
        # self.my_cursor.execute(self.query, self.val)
        # self.my_con.commit()
        # print('record deleted successfully')

    def prompt(self):
        print('''
                    1. Register
                    2. Login
            ''')
        self.ask = input('Enter the number of the operation you want to perform>>> ')
        if self.ask == '1':
            return self.register()
        elif self.ask == '2':
            return self.login()
        else:
            return self.prompt()

    def register(self):
        self.first_name = input('Enter your first name>>> ')
        self.last_name = input('Enter your last name>>> ')
        self.date_of_birth = input('Enter your date of birth(YY-MM-DD)>>> ')
        self.contact = input('Enter your phone number>>> ')
        self.email = input('Enter your email address>>> ')
        self.address = input('Enter your residential address>>> ')
        self.random_acct = random.randint(00000000, 99999999)
        self.account = f'20{self.random_acct}'
        print('To activate your account, you have to make a deposit of at least N2000')
        while True:
            try:
                self.deposit_amount = int(input('How much do you want to deposit? '))
                if self.deposit_amount >= 2000:
                    print(f'You have deposited a sum of {self.deposit_amount} into your account')
                    break
                else:
                    print('The minimum amount you can deposit is N2000')
            except ValueError:
                print('You have entered an invalid amount')

        while True:
            try:
                self.pin = int(input('Create a 4 digit pin that you will be using for your ATM/ONLINE transactions>>> '))
                if len(str(self.pin)) == 4:
                    print('You have successfully created a pin for your transactions.')
                    break
                else:
                    print('Your pin must be exactly 4 digis.')
            except ValueError:
                print('Invalid pin! The use of alphabet is not allowed in the creation of your pin')

        self.my_query = "INSERT INTO register(fname, lname, dob, phonenum, email, residential_address, accountnum, balance, PIN) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.user_info= (self.first_name, self.last_name, self.date_of_birth, self.contact, self.email, self.address, self.account, self.deposit_amount, self.pin)

        try:
            self.my_cursor.execute(self.my_query, self.user_info)
            self.my_con.commit()
            print(f'Dear {self.first_name} {self.last_name}, you have successfully opened an account with our bank and your account number is {self.account}.')
        except sql.Error as e:
            print(f'Error: {e}')

        self.pre_login = input('Do you want to login into your account?(Yes/No) ')
        if self.pre_login == "yes":
            return self.login()
        if self.pre_login == "no":
            sys.exit()

    def login(self):
        print('''
                    1. USSD
                    2. ATM
            ''')
        self.prompt_user = input('Enter the number of the operation you want to perform>>> ')
        if self.prompt_user == '1':
            ussd_inst = Ussd()
            ussd_inst.dial()
        elif self.prompt_user == '2':
            pass
        
    # def balance(self):
    #     self.check_balance = 

class Ussd(Bank):
    def __init__(self):
        super().__init__()

        
    def dial(self):
        while True:
            self.press = input('Dial *202# to start your USSD Banking>>> ')
            if self.press == '*202#':
                self.ussd_home()
                break
            else:
                print('You have entered an invalid USSD number')

    def ussd_home(self):
        print('''
                    1. Buy Airtime
                    2. Buy Data
                    3. Transfers
                    4. Check Balance
            ''')
        
        while True:
            self.prompt_user = input('Enter the number of the operation you want to perform>>> ')
            if self.prompt_user == '1':
                self.check_number()
                self.airtime()
            elif self.prompt_user == '2':
                pass
            elif self.prompt_user == '3':
                pass
            elif self.prompt_user == '4':
                pass
                break
            else:
                print('Invalid number')
                return self.ussd_home()
    
    def check_number(self):
        self.number = (input('Enter your number to continue USSD Banking>>> '))
        self.number_val = (f'{self.number}', )
        self.check = 'SELECT phonenum FROM register WHERE phonenum=%s'
        self.my_cursor.execute(self.check, self.number_val)
        self.user_number = self.my_cursor.fetchone()
        
        try:
            if self.user_number:
                self.pin()
            else:
                print('''
                            You do not have an account.
                    ''')
                self.register_account = input('Press 1 if you want to open an account>>> ')
                if self.register_account == '1':
                    return self.register()
                else:
                    print('You have entered an invalid number')
                    sys.exit()
        except sql.Error as e:
            print(f'Error: {e}')

    def pin(self):
        while True:
            try:
                self.pin_prompt = int(input('''
                                            Please enter your pin
                                                0. Back
                                '''))
                self.check_pin = 'SELECT phonenum, PIN FROM register where phonenum=%s AND PIN=%s'
                self.pin_val = (self.number, self.pin_prompt)
                self.my_cursor.execute(self.check_pin, self.pin_val)
                self.user_pin = self.my_cursor.fetchone()
                break
            except ValueError:
                print('You have entered an invalid PIN')
        
        try:
            if self.user_pin:
                pass
            else:
                print('Invalid PIN')
                return self.pin()
        except sql.Error as e:
            print(f'Error: {e}')

    def airtime(self):
        self.airtime_prompt = input('''
                            1. Airtime-Self
                            2. Airtime-Others
                        ''')
        if self.airtime_prompt == '1':
            self.airtime_amount()
        elif self.airtime_prompt == '2':
            pass
        else:
            return self.airtime()
        
    def airtime_amount(self):
        while True:
            try:
                self.airtimeAmount = int(input('''
                            Please enter amount (50 - 10000)
                            00. Back
                            0. Main
                        '''))
                if self.airtimeAmount == '00':
                    self.airtime()
                elif self.airtimeAmount == '0':
                    self.ussd_home()
                elif int(self.airtimeAmount) < 50 or int(self.airtimeAmount) > 10000:
                    self.wrong_airtimeAmount()
                else:
                    if self.airtimeAmount <= self.deposit_amount:
                        self.deposit_amount -= self.airtimeAmount
                        print(self.deposit_amount)
                        pass
                        break
                    else:
                        print('Insufficient funds')
            except ValueError:
                print('You have entered an invalid amount')

        


        try:
            self.query = "UPDATE register set balance=%s WHERE phonenum=%s"
            self.query_val = (self.deposit_amount, self.number, )
            self.my_cursor.execute(self.query, self.query_val)
            self.my_con.commit()
            print('balance updated successfully')
        except sql.Error as e:
            print(f'Error: {e}')
    
    def wrong_airtimeAmount(self):
        self.wrongAirtime = int(input('''
                                You have entered the wrong amount. Please enter values 
                                            from 50 to 10000
                        '''))
        if int(self.wrongAirtime) >= 50 or int(self.wrongAirtime) <= 10000:
            self.balance_airtime = self.deposit_amount - self.wrongAirtime
            if self.deposit_amount > self.wrongAirtime:
                pass
            else:
                print('Insufficient funds')
        else:
            return self.wrong_airtimeAmount()
            
        try:
            self.query = "UPDATE register set balance=%s WHERE phonenum=%s"
            self.query_val = (self.balance_airtime, self.number, )
            self.my_cursor.execute(self.query, self.query_val)
            self.my_con.commit()
            print('balance updated successfully')
        except sql.Error as e:
            print(f'Error: {e}')












bank_inst = Bank()
bank_inst.prompt()
