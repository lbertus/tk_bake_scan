from ttkthemes import ThemedTk
from tkinter import ttk
from tkinter import *
import datetime
import sqlite3
import time

class ScanToLog:

    def __init__(self, root):

        self.conn = sqlite3.connect('bake_scan_db.db')
        self.cur = self.conn.cursor()
#        self.cur.execute('''CREATE TABLE bake_scan (barcode text, in_out text, date_time timestamp)''')

        root.title("Tk Bake scan")
        root.geometry("800x480")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.resizable(0, 0)

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.scan_label = ttk.Label(mainframe, text="Scan or type here")
        self.scan_label.grid(column=1, row=1)

        self.buttons_label = ttk.Label(mainframe, text="In/out of oven, or clear")
        self.buttons_label.grid(column=2, row=1)

        self.log_label = ttk.Label(mainframe, text="Log")
        self.log_label.grid(column=3, row=1)

        self.scan_text = Text(mainframe, width=20, height=25)
        self.scan_text.grid(column=1, row=2, rowspan=3, sticky=(W, E, N, S), padx=5, pady=5)

        self.into_oven_button = ttk.Button(mainframe, text="Into Oven", command=self.log_into_oven)
        self.into_oven_button.grid(column=2, row=2, sticky=(W, E, N, S), padx=5, pady=5)

        self.out_oven_button = ttk.Button(mainframe, text="Out of Oven", command=self.log_out_of_oven)
        self.out_oven_button.grid(column=2, row=3, sticky=(W, E, N, S), padx=5, pady=5)

        self.clear_button = ttk.Button(mainframe, text="Clear", command=self.clear_scan_text)
        self.clear_button.grid(column=2, row=4, sticky=(W, E, N, S), padx=5, pady=5)

        self.log_text = Text(mainframe, width=55, height=25)
        self.log_text.grid(column=3, row=2, rowspan=3, sticky=(W, E, N, S), padx=5, pady=5)
        self.log_text['state'] = 'disabled'

        self.scan_text.focus()


    def log_into_oven(self, *args):
        print('into_oven_button pressed')
        try:
            self.log_text['state'] = 'normal'
            datetime_now = datetime.datetime.now().replace(microsecond=0)
            time_now = datetime_now.strftime("%d/%m/%Y, %H:%M:%S")
            serial_nrs = self.scan_text.get('1.0', 'end')
            serial_nrs_split = serial_nrs.split('\n')       # remove '\n' chars
            for serial_nr in serial_nrs_split:
                if serial_nr is not '':                     # after removing '\n', we are left with '' 
                    self.cur.execute('INSERT INTO bake_scan VALUES (?, ?, ?)', (serial_nr, 'into_baking', datetime_now))
                    self.conn.commit()
                    self.log_text.insert('1.0', serial_nr + ' - In  to oven - ' + time_now + '\n')
            self.scan_text.delete('1.0', 'end')
            self.scan_text.focus()
            self.log_text['state'] = 'disabled'
        except ValueError:
            pass

    def log_out_of_oven(self, *args):
        print('out_oven_button pressed')
        try:
            self.log_text['state'] = 'normal'
            datetime_now = datetime.datetime.now().replace(microsecond=0)
            time_now = datetime_now.strftime("%d/%m/%Y, %H:%M:%S")
            serial_nrs = self.scan_text.get('1.0', 'end')
            serial_nrs_split = serial_nrs.split('\n')
            for serial_nr in serial_nrs_split:
                if serial_nr is not '':
                    self.log_text.insert('1.0', serial_nr + ' - Out of oven - ' + time_now + '\n')
                    self.cur.execute('INSERT INTO bake_scan VALUES (?, ?, ?)', (serial_nr, 'out_of_baking', datetime_now))
                    self.conn.commit()
            self.scan_text.delete('1.0', 'end')
            self.scan_text.focus()
            self.log_text['state'] = 'disabled'
        except ValueError:
            pass

    def clear_scan_text(self, *args):
        print('clear_scan_text pressed')
        self.scan_text.delete('1.0', 'end')
        self.scan_text.focus()

root = Tk()
ScanToLog(root)
root.mainloop()

