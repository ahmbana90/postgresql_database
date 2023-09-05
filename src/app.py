from datetime import date
from typing import Optional
from tabulate import tabulate
from collections import namedtuple
from src.schema import StatusEnum, CreateDataType, FetchByIdDataType
from src.database import insert_data, fetch_by_id, update_data

class MenuDisplay:

    @staticmethod
    def display_menu():
        print(
            '''
            WELCOME TO MY READ APP
            
            MENU
            ----------------
            1. DATA QUERY
            2. DATA MANIPULATION
            99. QUIT
            '''
        )
        
    @staticmethod
    def display_DM_menu():
        print(
            '''
            MENU > DATA MANIPULATION
            ----------------
            1. INSERT DATA 
            2. UPDATE DATA
            3. DELETE Data
            77. BACK TO MENU 
            99. QUIT
            '''
        )

    @staticmethod
    def display_DQ_menu():
        print(
            '''
            MENU > DATA QUERY
            ----------------
            1. HOW MANY BOOKS WERE READ COMPLETELY DURING A SPECIFIC PERIOD OF TIME?
            2. HOW MANY BOOKS DO WE HAVE PENDING?
            3. SEARCH BOOKS BY TITLE
            77. BACK TO MENU 
            99. QUIT
            '''
        )

class InputOption():
    
    @staticmethod
    def input_option_dm_insert() -> CreateDataType:
        # FIXME: add login feature and extract the username from there
        username= "ahmed"
        print("Please provide the following details: ")
        book_title: str = input("Book title: ")
        book_desc: str = input("(Optional) Describe the book: ")
        status: StatusEnum = input("(Optional) What is your current read status(pending,reading,complete): ")
        pct_read: int = input("(Optional) What is the reading percentage: ")
        if pct_read:
            pct_read= int(pct_read)
        start_read_date: str = input("(Optional) Start reading date(YYYY-MM-DD): ")
        if start_read_date:
            start_read_date: date = date.fromisoformat(start_read_date)
        end_read_date: str = input("(Optional) End reading date(YYYY-MM-DD): ")
        if end_read_date:
            end_read_date: date = date.fromisoformat(end_read_date)
        
        return {
            "username": username,
            "book_title": book_title,
            "book_desc": book_desc if len(book_desc)>1 else None,
            "status": status if status else "pending",
            "pct_read": pct_read if pct_read else 0,
            "start_read_date": start_read_date if start_read_date else None,
            "end_read_date": end_read_date if end_read_date else None
        }
    
    @staticmethod
    def input_option_dm_update():
        while True:
            id_to_update: int = int(input("Input a book id to update: "))
            book: Optional[FetchByIdDataType] = fetch_by_id(id_to_update)
            if book is None:
                print("Book does not exist!, please try again")
                continue
            else:
                # display the book info in a table
                print("Book info: ")
                InputOption.generate_table(book)
                print("""
                      Fields to update?
                      1. Book Title
                      2. Description
                      3. Status
                      4. Pct Read
                      5. Start Date
                      6. End Date
                      """)
                field_option= int(input("Choose field to change: "))
                UpdatedInfo= namedtuple("UpdatedInfo", "book_id column value")
                if field_option == 1:
                    book_title= input("Enter a new title: ")
                    updated_info= UpdatedInfo(book_id=id_to_update, column="title", value=book_title)
                    return updated_info
                    
    @staticmethod
    def generate_table(data):
        table= [
            [
                "title",
                "des",
                "status",
                "pct read",
                "start date",
                "end date"
            ],
            data,
        ]
        print(tabulate(
            table,
            headers="firstrow",
            tablefmt="fancy_grid"
        ))
        
    
def main():
    while True:
        MenuDisplay.display_menu()
        option: int = int(input("Choose an option to continue: "))
        if option==1:
            MenuDisplay.display_DQ_menu()
        elif option==2:
            while True:
                MenuDisplay.display_DM_menu()
                option: int = int(input("Choose an option to continue: "))
                if option==1:
                    data: CreateDataType = InputOption.input_option_dm_insert()
                    # insert data to database 
                    id= insert_data(data)
                # update
                elif option==2:
                    updated_data= InputOption.input_option_dm_update()
                    updated_id= update_data(updated_data.book_id, updated_data.column, updated_data.value)
                    if updated_id is not None:
                        print(f"Record with id: {updated_id}, updated successfully")
                    else:
                        print("Update failed!")
        elif option==99:
            break
        else:
            print("Option not recognized, please try again!")

if __name__=='__main__':
    main()