import tkinter
from tkinter import *
from tkinter import messagebox, Toplevel
import ast
from tkinter import ttk
import sqlite3


root=Tk()
root.title("Car Sales")
root.geometry("780x430")
root.resizable(height=False,width=False)
root.configure(bg="#383949")
#car image
def resize_image(image_path, width, height):
    original_image = PhotoImage(file=image_path)
    original_width = original_image.width()
    original_height = original_image.height()

    aspect_ratio = original_width / original_height

    if original_width > width:
        new_width = width
        new_height = int(new_width / aspect_ratio)
    elif original_height > height:
        new_height = height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = original_width
        new_height = original_height

    resized_image = original_image.subsample(int(original_width / new_width), int(original_height / new_height))

    return resized_image
resized_car_image=resize_image("Car.png",130,100)

image_label = Label(root, image=resized_car_image, bg="#bfefff")
image_label.grid(row=0, column=0, padx=20, pady=20, sticky="nw")



def signin():
    username=user.get()
    password=code.get()

    file=open('data.txt', 'r')
    d=file.read()
    r=ast.literal_eval(d)
    file.close()


    if username in r.keys() and password==r[username]:
        import tkinter as tk
        from tkinter import ttk
        import sqlite3

        class CarDatabase:
            def __init__(self, db_path='cars.db'):
                self.conn = sqlite3.connect(db_path)
                self.cursor = self.conn.cursor()

                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cars (
                        id INTEGER PRIMARY KEY,
                        make TEXT,
                        model TEXT,
                        year INTEGER,
                        price REAL
                    )
                ''')
                self.conn.commit()

            def add_car(self, make, model, year, price):
                self.cursor.execute('''
                    INSERT INTO cars (make, model, year, price)
                    VALUES (?, ?, ?, ?)
                ''', (make, model, year, price))
                self.conn.commit()

            def delete_car(self, car_id):
                self.cursor.execute('DELETE FROM cars WHERE id = ?', (car_id,))
                self.conn.commit()

            def get_all_cars(self):
                self.cursor.execute('SELECT * FROM cars')
                return self.cursor.fetchall()

            def search_cars(self, make, model, year, price):
                query = '''
                    SELECT * FROM cars
                    WHERE make LIKE ? AND model LIKE ? AND year LIKE ? AND price LIKE ?
                '''
                params = ('%' + make + '%', '%' + model + '%', '%' + year + '%', '%' + price + '%')
                self.cursor.execute(query, params)
                return self.cursor.fetchall()

            def close_connection(self):
                self.conn.close()

        class CarSalesApp:
            def __init__(self, root):
                self.root = root
                self.root.title("Car Sales Application")
                self.root.configure(bg="#383949")
                self.root.resizable(False, False)

                self.make_label = ttk.Label(root, text="Name:")
                self.make_entry = ttk.Entry(root)

                self.model_label = ttk.Label(root, text="Model:")
                self.model_entry = ttk.Entry(root)

                self.year_label = ttk.Label(root, text="Year:")
                self.year_entry = ttk.Entry(root)

                self.price_label = ttk.Label(root, text="Price:")
                self.price_entry = ttk.Entry(root)

                self.add_button = ttk.Button(root, text="Add Car", command=self.add_car)
                self.delete_button = ttk.Button(root, text="Delete Car", command=self.delete_car)
                self.search_button = ttk.Button(root, text="Search", command=self.search_cars)

                self.tree = ttk.Treeview(root, columns=('ID', 'Name', 'Model', 'Year', 'Price'), show='headings')

                self.tree.heading('ID', text='ID')
                self.tree.heading('Name', text='Name')
                self.tree.heading('Model', text='Model')
                self.tree.heading('Year', text='Year')
                self.tree.heading('Price', text='Price')

                self.make_label.pack()
                self.make_entry.pack()

                self.model_label.pack()
                self.model_entry.pack()

                self.year_label.pack()
                self.year_entry.pack()

                self.price_label.pack()
                self.price_entry.pack()

                self.add_button.pack()
                self.delete_button.pack()
                self.search_button.pack()

                self.tree.pack()

                self.db = CarDatabase()

                self.load_cars()

            def add_car(self):
                name = self.make_entry.get()
                model = self.model_entry.get()
                year = self.year_entry.get()
                price = self.price_entry.get()

                self.db.add_car(name, model, year, price)

                self.make_entry.delete(0, 'end')
                self.model_entry.delete(0, 'end')
                self.year_entry.delete(0, 'end')
                self.price_entry.delete(0, 'end')

                self.load_cars()

            def delete_car(self):
                selected_item = self.tree.selection()

                if not selected_item:
                    return

                car_id = self.tree.item(selected_item, 'values')[0]

                self.db.delete_car(car_id)

                self.load_cars()

            def search_cars(self):
                make = self.make_entry.get()
                model = self.model_entry.get()
                year = self.year_entry.get()
                price = self.price_entry.get()

                results = self.db.search_cars(make, model, year, price)

                for item in self.tree.get_children():
                    self.tree.delete(item)

                for car in results:
                    self.tree.insert('', 'end', values=car)

            def load_cars(self):
                for item in self.tree.get_children():
                    self.tree.delete(item)

                cars = self.db.get_all_cars()

                for car in cars:
                    self.tree.insert('', 'end', values=car)

            def __del__(self):
                self.db.close_connection()

        if __name__ == "__main__":
            root = tk.Tk()
            app = CarSalesApp(root)
            root.mainloop()


    else:
        messagebox.showerror('invalid', 'Wrong Password or Email')



def signup_command():
    win = Toplevel(root)

    win.title("Car Sales")
    win.geometry('780x430')
    win.configure(bg="#383949")
    win.resizable(False, False)

    def signup():
        username = user.get()
        password = code.get()
        conform_password = conform_code.get()

        if password == conform_password:
            try:
                file = open('data.txt', 'r+')
                d = file.read()
                r = ast.literal_eval(d)

                dict2 = {username: password}
                r.update(dict2)
                file.truncate(0)
                file.close()

                file = open('data.txt', 'w')
                w = file.write(str(r))

                messagebox.showinfo('Signup', 'Registration completed succsesfully')

            except:
                file = open('data.txt', 'w')
                pp = str({'Username': 'password'})
                file.write(pp)
                file.close()

        else:
            messagebox.showerror('Invalid', 'Both password should be the same')

    def sign():
        win.destroy()


    frame = Frame(win, width=350, height=390, bg="#383949")
    frame.place(x=190, y=50)

    heading = Label(frame, text="Registration", fg="white", bg="#383949", font=("Arial", 23, "bold"))
    heading.place(x=100, y=5)

    ########-სახელი
    def on_entry(e):
        user.delete(0, "end")

    def on_leave(e):
        name = user.get()
        if name == "":
            user.insert(0, 'Email')

    user = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Arial", 10))
    user.place(x=102, y=85)
    user.insert(0, "Email")
    user.bind("<FocusIn>", on_entry)
    user.bind("<FocusOut>", on_leave)


    ########-პაროლი
    def on_entry(e):
        code.delete(0, "end")

    def on_leave(e):
        if code.get() == "":
            code.insert(0, 'Password')

    code = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Arial", 10))
    code.place(x=102, y=120)
    code.insert(0, "Password")
    code.bind("<FocusIn>", on_entry)
    code.bind("<FocusOut>", on_leave)


    def on_entry(e):
        conform_code.delete(0, "end")

    def on_leave(e):
        if conform_code.get() == "":
            conform_code.insert(0, 'Repeat Password')

    conform_code = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Arial", 10))
    conform_code.place(x=102, y=155)
    conform_code.insert(0, "Repeat Password")
    conform_code.bind("<FocusIn>", on_entry)
    conform_code.bind("<FocusOut>", on_leave)




    Button(frame, width=39, pady=7, text="Registration", bg="#4267B2", fg="white", border=0, command=signup).place(x=35,y=210)
    Label1 = Label(frame, text="Already have an account?", fg="black", bg="#383949", font=("arial", 9))
    Label1.place(x=28, y=250)

    sign_up = Button(frame, width=16, text="Login", border=0, bg="#4267B2", cursor="hand2", fg="white",command=sign)
    sign_up.place(x=195, y=250)

    win.mainloop()



frame = Frame(root, width=350, height=350, bg="#383949")
frame.place(x=230, y=100)

heading = Label(root, text="Welcome to Car Sales", fg="white", bg="#383949", font=("Helvetica", 40,))
heading.grid(row=0, column=1, padx=20, pady=20, sticky="w")

horizontal_line_canvas = Canvas(root, width=780, height=2, bg="blue")
horizontal_line_canvas.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="sw")



def on_entry(e):
    user.delete(0, "end")


def on_leave(e):
    name = user.get()
    if name == "":
        user.insert(0, 'Email')




user = Entry(frame, width=20, fg="black", border=0, bg="white", font=("Arial", 10))
user.place(x=80, y=90)
user.insert(0, "Email")
user.bind("<FocusIn>", on_entry)
user.bind("<FocusOut>", on_leave)



def on_entry(e):
    code.delete(0, "end")


def on_leave(e):
    name = user.get()
    if name == "":
        code.insert(0, 'Password')


code = Entry(frame, width=20, fg="black", border=0, bg="white", font=("Arial", 10))
code.place(x=80, y=120)
code.insert(0, "Password")
code.bind("<FocusIn>", on_entry)
code.bind("<FocusOut>", on_leave)


Button(frame, width=10, pady=7, text="Login", bg="#4267B2", fg="white", border=0, command=signin).place(x=80, y=150)

sign_up = Button(frame, width=10, pady=7, text="Registration", border=0, bg="#4267B2", cursor="hand2", fg="white",
                 command=signup_command, )
sign_up.place(x=80, y=190)
root.mainloop()