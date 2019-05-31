#!/usr/bin/env python3
from collections import OrderedDict
import datetime
from time import sleep
import os 
import sys
import re 

import logging 



logging.basicConfig(filename='employee.log', level=logging.INFO, 
    format='%(asctime)s:%(levelname)s:%(message)s')


logging.basicConfig(filename='test.log', level=logging.DEBUG, 
    format='%(asctime)s:%(levelname)s:%(message)s')
#Capture data when program debugged and saved in test.log

from peewee import *

db = SqliteDatabase('entry.db')

clear = lambda:os.system('cls')






class Entry(Model):
    employee_name = CharField(max_length = 100)
    task_name = CharField(max_length  = 100)
    date = DateTimeField(default = datetime.datetime.now)
    time_spent = TimeField()
    notes = TextField(default=None)
  
    class Meta:
        database = db

class Employee: 
    def __init__(self, first, last, *args):
        self.first = first
        self.last = last

    def fullname(self):
        fullname = self.first + self.last
        return fullname

    def __repr__(self):
        return "Welcome  {} {} to your worklog".format(self.first, self.last)
    

    def email(self):
        return "{}.{}@hotmail.com".format(self.first, self.last)




class Worklog(): 

    def menu_loop():
        from datetime import datetime 
        choice = None
        while choice != 'q': 
            timestamp = datetime.now()
            print(timestamp.strftime("%A %B %d, %Y %I:%M%p"))
            print("="*20)
            print("\n")
            print("Press 'q' if you would like to stop")
            for letter, value in menu_options.items(): 
                print(" Press {}  to {}".format(letter, value.__doc__))
                
            choice = input("Action: ").lower().strip()

            if choice in menu_options: 
                menu_options[choice]()




    
    def add_entry(): 
        "add an entry"
        task, date, time, notes = Worklog.task_name(), Worklog.date(), Worklog.time_spent(), Worklog.task_comments()
        clear()
        entries = [task, date, time, notes]
        print("Enter your entry. Press ctrl+d when finished")
        
        for value, entry in enumerate(entries): 
            print('{}: {}'.format(value+1, entry))

        print(6*"\n")
        data = input("Save entry?  [Yn]: ").lower()

        if data != 'n':
            Entry.create(employee_name=emp1.first,  task_name=task, date=date, time_spent=time, notes=notes )
            print("Saved succesfully!")
            sleep(2)
            clear()

        elif data == 'n': 
            print("Entries not saved! ")
            sleep(2)
            clear()
            return 


    def search_entries(): 
        """ search by entry """
        clear()
        print("You can search by:  ")
        search = [("Employee", 'e'), ("date", 'd'), ("time spent",'s'), ("term", 't')]
        for string, letter in search: 
            print("if you want search by {} press {} below".format(string, letter))

        choice = input("> ").lower().strip()

        
        
        if choice == "t":
            clear()
            my_choice = search.pop(len(search)-1)
            Worklog.view_entries(input("Search query: "), my_choice)
        
        elif choice == "e": 
            clear()
            my_choice = search.pop(0)
            Worklog.view_entries(input("Search query: "), my_choice)
        
        elif choice == "s": 
            clear()
            my_choice = search.pop(2)
            print("You search by minutes spent on task.")
            Worklog.view_entries(input("Search query: "), my_choice)
        
        elif choice == "d": 
            clear()
            my_choice = search.pop(1)
            Worklog.view_entries(input("Search query: "), my_choice)







    def view_entries(search_query=None, *args): 
        """ view entries"""
        entries = Entry.select().order_by(Entry.date.desc())
        clear()
     

        if search_query != None:
            if "t" in args[0][1]: 
                entries = entries.where(Entry.task_name.contains(search_query))
            if "e" in args[0][1]: 
                entries = entries.where(Entry.employee_name.contains(search_query))
            if "s" in args[0][1]: 
                entries = entries.where(Entry.time_spent.contains(search_query))
            if "d" in args[0][1]: 
                entries = entries.where(Entry.date.contains(search_query))
            
          

        for entry in entries: 
            printed_entries = [entry.employee_name, entry.task_name, entry.date, entry.time_spent, entry.notes]
            entries = ["employee","task", "date", "time spent", "notes"]
            for i, j in zip(entries, printed_entries):
                print("{}: {}".format(i, j))
            print("="*20)
            print("\n")
            print('N) next entry ')
            print('Q) return to main menu')

            next_action = input("Action: [nq]:  ").lower().strip()
            clear()
            if next_action == 'q': 
                clear()
                break

    def task_name(): 
        while True: 
            clear()
            task = input("Please enter the task you have done:  ")
            if task == None: 
                print("Please, you must enter something to continue")
                continue
            return task


    def task_comments():
        clear()
        print("Fill in notes but this is optional")
        comments = input("> ")

        if comments == None: 
            comments = "Nothing"
        return comments
        

    def date():
        """Asks for date and validates it"""
        while True:
            clear()
            task_date = input("When was this task performed? Date format: dd-mm-yyyy \n > ").strip()
            try:
                task_date = datetime.datetime.strptime(task_date, "%d-%m-%Y")
                if task_date.date() > datetime.datetime.today().date():

                    input(" Sorry, date can't be later than today's date. Press enter and provide a correct date ")
                    continue

            except ValueError:
                input(" Sorry, not a valid date. Press enter and provide a correct date... ")
                continue

            except Exception: 
                raise("Something went wrong.")
                input("Press enter to continue...")
                continue 

            else:
                return task_date.strftime("%d-%m-%Y")

    def time_spent():
        while True:
            clear()
            time_spent = input("\n Time spent? Please enter like this: hh:mm \n> ").strip()
            if not re.match(r'^\d{1,2}:\d{2}$', time_spent):
                input(" Invalid duration. Your duration must be in the format hh:mm. Press enter to continue... ")
                continue
            elif re.match(r'^\d{1,2}:\d{2}$', time_spent):
                time_spent_split = time_spent.split(':')
                # check to see if duration is not 0
                if (int(time_spent_split[0]) < 1) and (int(time_spent_split[1]) < 1):
                    input(" Time spent cannot be of 0 hour and 0 minute. Press enter to continue... ")
                    continue
                    # check to see if hour part of time is not more than 24
                elif int(time_spent_split[0]) > 24:
                    input(" Time spent cannot be more than 24 hours. Press enter to continue... ")
                    continue
                    # check to see if duration is not more than 24
                elif (int(time_spent_split[0]) == 24) and (int(time_spent_split[1]) > 0):
                    input(" Time spent cannot be more than 24 hours. Press enter to continue... ")
                    continue
                    # check to see if duration is not more than 24
                elif (int(time_spent_split[0]) == 23) and (int(time_spent_split[1]) > 60):
                    input(" Time spent cannot be more than 24 hours. Press enter to continue... ")
                    continue
                else:
                    time_spent = (int(time_spent_split[0]) * 60) + (int(time_spent_split[1]))
                    return time_spent

def initialize(): 
    db.connect()
    db.create_tables([Entry], safe=True)


menu_options = OrderedDict([('a', Worklog.add_entry),
    ('v', Worklog.view_entries), 
    ('s', Worklog.search_entries)])


if __name__ == '__main__':
    initialize()
    firstname = input("What is your firstname: ")
    lastname = input("What is your lastname: ")
    emp1 = Employee(firstname, lastname) 
    print(repr(emp1))
    sleep(2)
    clear()

    Worklog.menu_loop()