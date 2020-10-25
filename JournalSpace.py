import tkinter as tk
import os
from getpass import getuser
from pathlib import Path
from cryptography.fernet import Fernet
import hashlib
import random
from tkinter import messagebox
from datetime import datetime
import pickle

# *****************TODO***************
#
# create a short display of past entrys, and make it clickable
#
# look into using actual encryption for the data file. encoding at the least
#
#



#program to start the main user facing window
def startProgram():
    global data
#check if there is a data file. if it exists check how long it is, if it doesn't exist create a new data file
    if os.path.exists('C:\\Users\\Kyle\\Documents\\JournalSpace\\Data.dat'):
        data = pickle.load(open("C:\\Users\\Kyle\\Documents\\JournalSpace\\Data.dat", 'rb'))
    else:
        print('No database found, creating a new one')
        file = open('C:\\Users\\Kyle\\Documents\\JournalSpace\\Data.dat', 'w')
        file.close()
        data = []

    # print(data)
#create main window
    main = tk.Tk()
    datenow = str(datetime.now())
#if there is no past entrys just show a "new" button otherwise show date (in futere will show past entrys)
    if len(data) > 0:
        # dateLabel = tk.Label(main, text=datenow[0:10])
        # dateLabel.grid(row=0, column=0)
        entryDisplay = tk.Frame()
        entryDisplay.grid(row=0, column=0)
        for i in enumerate(data):
            displaytext = tk.Button(entryDisplay, text = i[1][1][0:50]).pack()
            # print(i[1][1][0:50])
        createButton = tk.Button(main, text='Create Entry', command=entryWindow)
        createButton.grid(row=1, column=0)
        # print('larger than 0')
    else:
        # dateLabel = tk.Label(main, text=datenow[0:10])
        # dateLabel.grid(row=0, column=0)
        createButton = tk.Button(main, text='Create Entry', command=entryWindow)
        createButton.grid(row=1, column=0)


#attempt to log in based on set password
def loginAttempt(x, entered, z):
#    #make a new container for a hex hash
    temp = hashlib.sha256()
#    #add the salt from login.sa (stored in first part of the saved string)
    temp.update(bytes(x[0], 'utf-8'))
#    #add user provided password to compare
    temp.update(bytes(entered, 'utf-8'))
#    # process all provided data to create a unique hex string
    temp = temp.hexdigest()
#    #test if our new hex string (temp) matches our target string (known password)
    if x[1] == temp:  #if we match the password we can destory the login window (x) and start the program
        z.destroy()
        startProgram()
    else:#if not, we let the user know and allow them to try again
        messagebox.showerror("Wrong Password", "The password entered isn't correct")


def login():
    file = open(userpath + '/Documents/JournalSpace/login.sa', 'r')
    temp = file.readline()
    file.close()
    password = temp.split(':')
    # print(password)
    loginWindow = tk.Tk()
    loginLabel = tk.Label(loginWindow, text='password')
    loginLabel.grid(row=0, column=0)
    loginEntry = tk.Entry(loginWindow, show='*')
    loginEntry.grid(row=0, column=1)
    loginEnter = tk.Button(loginWindow, text='Enter', command=lambda: loginAttempt(password, loginEntry.get(), loginWindow))
    loginEnter.grid(row=1, columnspan=2)


def setPassword():
    global userpath
    if pasEntry2.get() == pasEntry.get():
        rannum = random.random()
        rannum *= 1000000
        rannum = round(rannum)
        rannum = str(rannum)
        password = pasEntry.get()
        newpassword.destroy()
        passhash = hashlib.sha256()
        passhash.update(bytes(rannum, 'utf-8'))
        passhash.update(bytes(password, 'utf-8'))
        temp = passhash.hexdigest()
        writer = rannum + ":" + str(temp)
        file = open(userpath + '/Documents/JournalSpace/login.sa', 'w')
        file.write(writer)
        file.close()
        # login()
        startProgram()
    else:
        messagebox.showerror("No match", "The passwords entered don't match")


#function to save
def saveEntry(window):
    global tkVar
    global entrytext
    global data
    global entry

    temp = []
    thisdate = str(datetime.now())
    temp.append(thisdate[0:10])
    temp.append(entrytext.get("1.0", 'end'))
    data.append(temp)

    pickle.dump(data, open('C:\\Users\\Kyle\\Documents\\JournalSpace\\Data.dat', 'wb'))
    # print('entry saved')
    window.destroy()


# function for a new journal entry
def entryWindow():
    global tkVar
    global entrytext
    entry = tk.Tk()

    textFrame = tk.Frame(entry)
    textFrame.pack(side='top')

    entrytext = tk.Text(textFrame)
    entrytext.grid(row=0, column=0)

    optionFrame = tk.Frame(entry)
    optionFrame.pack(side='bottom')

    tkVar = []
    tkVar.append(tk.IntVar(optionFrame))
    tkVar.append(tk.IntVar(optionFrame))
    tkVar.append(tk.IntVar(optionFrame))
    tkVar.append(tk.IntVar(optionFrame))

    fightbox = tk.Checkbutton(optionFrame, text='fight', variable=tkVar[0])
    fightbox.pack(side = 'right')
    sleepbox = tk.Checkbutton(optionFrame, text='Low Sleep', variable=tkVar[1])
    sleepbox.pack(side='left')
    sexbox = tk.Checkbutton(optionFrame, text='Had Sex', variable=tkVar[2])
    sexbox.pack(side='left')
    eventbox = tk.Checkbutton(optionFrame, text='Stressful Event', variable=tkVar[3])
    eventbox.pack(side='right')
    tkbutton = tk.Button(optionFrame, text='Save', command=lambda: saveEntry(entry))
    tkbutton.pack(padx=115, side = 'bottom')

#check for the user path
userpath = os.path.expanduser('~')
#set the location of our password file login.sa
filename = Path(userpath + '/Documents/JournalSpace/login.sa')
#check to see if we have a folder in the Documents lybrary and create one if not. then go to login funciton
if not os.path.exists(userpath + '/Documents/JournalSpace'):
    os.mkdir(userpath + '/Documents/JournalSpace')
#check if a password has been set, set up one if not
if os.path.exists(filename):
    # print('file exists')
    login()
else:
    newpassword = tk.Tk()
    passlabel = tk.Label(newpassword, text="Password")
    passlabel.grid(row=0, column=0)
    passlabel2 = tk.Label(newpassword, text="Confirm Password")
    passlabel2.grid(row=1, column=0)
    pasEntry = tk.Entry(newpassword, show='*')
    pasEntry.grid(row=0, column=1)
    pasEntry2 = tk.Entry(newpassword, show='*')
    pasEntry2.grid(row=1, column=1)
    passwordButton = tk.Button(newpassword, text="submit", command= setPassword)
    passwordButton.grid(row=2, columnspan=2)

#as always update the program ;)
tk.mainloop()
