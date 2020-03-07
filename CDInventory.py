#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# MList, 2020-Mar-01, Fixed error in function read_file() as script crashes when no CDInventory.txt is present
# MList, 2020-Mar-01, Completed TODOs when 'a' is called and created functions append_cd_inventory_memory_list() + IO.cd_user_input()
# MList, 2020-Mar-01, Completed TODO for delete function, created delete_CD() and tested functionality
# MList, 2020-Mar-01, Completed TODO for saving function, build out shell function for write_file()
# MList, 2020-Mar-01, Ensured proper commenting in main body of script
# MList, 2020-Mar-01, Added docstrings for newly written functions
# MList, 2020-Mar-06, Changed CDInventory.txt to CDInventory.dat and changed file accesses from text to binary
# Mlist, 2020-Mar-07, Added exceptions for user interactions, type casting (string to int) and file access operations where needed. Updated docstrings
#------------------------------------------#
import pickle
# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # dictionary of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:

    @staticmethod
    #result is assinged to local variable table which is referencing the same variable as the global lstTbl
    def append_cd_inventory_memory_list(intID, strTitle, strArtist, table):
        """Function to append new user entry as a dictionary within a 2D list

        Uses passed arguements of CD information to create a new CD entry as a dictionary and adds dictionary as a new line to global 2D table

        Args:
            intID (integer): Requested ID of CD the user would like to add
            strTitle (string): Requested CD Title the user would like to add
            strArtist (string): Requested Artist of CD the user would like to add
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        table.append(dicRow)


    @staticmethod
    def delete_CD(ID, table):
        """Function to delete CD from 2D list based on ID match

        User defines the ID of a CD the user would like to remove. ID gets passed to this function is used to identify a match in global 2D table.
        If match is identified by matching value of ID key, entry dictionary will be removed from global 2D table.

        Args:
            ID (integer): Requested ID of CD the user would like to delete. Casted into integer prior function call
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == ID:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')

class FileProcessor:
    """Processing the data to and from text file"""
    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a global 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.
        Catches IOError in case the file does not exist.

        Args:
            file_name (string): name of file used to read the data from
        Returns:
            None.
        """
        table = []
        try:
            with open(file_name, 'rb') as objFile:
                table = pickle.load(objFile)
        except IOError: 
            print('\nThere is currently no existing inventory file\n')
        return table

    @staticmethod
    def write_file(file_name, table):
        """Function to write added data to a binary file

        Reads the data of dictionaries stored in 2D table. 
        Saves data as a binary file with pickle

        Args:
            file_name (string): name of file used to read the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """

        with open(file_name, 'wb') as objFile:
            pickle.dump(table, objFile)

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        
    @staticmethod
    def cd_user_input():
        """Gets user input to add new CD
        
        Catches ValueError in case the entered ID for the CD is not an integer. 
        If this exception is caught the program keeps asking the user to enter a numerical ID
        until an integer has been entered.

        Args:
            None.

        Returns:
            intID, strTitle, strArtist (tuple): Returns tuple with the 3 variables: ID, Title and Artist

        """
        flag = True
        while flag == True:
            try:
                strID = input('Enter a numerical ID: ').strip()
                intID = int(strID)
                flag = False
            except ValueError:
                print ('The entered ID is not an integer. Please enter a number')
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return intID, strTitle, strArtist


# 1. When program starts, read in the currently saved Inventory
lstTbl = FileProcessor.read_file(strFileName)
# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist and unpacking return tuple
        strIDGlobal, strTitleGlobal, strArtistGlobal = IO.cd_user_input()
        # 3.3.2 Add item to the table
        DataProcessor.append_cd_inventory_memory_list(strIDGlobal, strTitleGlobal, strArtistGlobal, lstTbl)
        # 3.3.3 Displaying current inventory
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
            # 3.5.2 search thru table and delete CD
            # 3.5.2.1 delete entry
            DataProcessor.delete_CD(intIDDel, lstTbl)
            # 3.5.2.2 display Inventory to user
            IO.show_inventory(lstTbl)
        except ValueError:
                print ('Faulty input: The entered ID is not a number (integer)\n')
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower() #No Error handling required
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')