from tkinter import *
from tkinter import messagebox
import mysql.connector
import next_win

conn = mysql.connector.connect(
    user='root',
    password='pass@123',
    host='localhost',
    database='kanan20'
)

cursor = conn.cursor()

# ----------------------------------------------------------
# table name : ( [column names], [heading shown in GUI] )
# The FIRST column of each table is the primary key.
# It is used to find the record for Update and Delete.
# ----------------------------------------------------------
tables = {
    "Supplier": (
        ["s_id", "s_name", "s_category", "s_quantity", "e_id"],
        ["Supplier ID", "Supplier Name", "Supplier Category", "Supplier Quantity", "Employee ID"]),

    "Employee": (
        ["e_id", "f_name", "e_exp", "l_name", "e_sal", "e_design"],
        ["Employee ID", "First Name", "Experience", "Last Name", "Salary", "Designation"]),

    "Customer": (
        ["c_id", "c_name", "c_contact", "c_pass", "c_add"],
        ["Customer ID", "Customer Name", "Customer Contact", "Customer Password", "Customer Address"]),

    "Offers": (
        ["o_no", "o_type", "o_date", "o_amount", "p_id", "e_id"],
        ["Offer No", "Offer Type", "Offer Date", "Offer Amount", "Product ID", "Employee ID"]),

    "Products": (
        ["p_id", "p_quantity", "p_name", "p_price", "c_id", "s_id", "d_no"],
        ["Product ID", "Product Quantity", "Product Name", "Product Price", "Customer ID", "Supplier ID", "Delivery No"]),

    "Invoice": (
        ["i_id", "i_totalamt", "i_date", "e_id", "t_id"],
        ["Invoice ID", "Total Amount", "Invoice Date", "Employee ID", "Transaction ID"]),

    "Transaction": (
        ["t_id", "t_amt", "t_date", "t_mode", "i_id", "c_id", "e_id"],
        ["Transaction ID", "Amount", "Date", "Mode", "Invoice ID", "Customer ID", "Employee ID"]),

    "Recommendation": (
        ["r_id", "r_type", "e_id", "c_id", "p_name", "p_id"],
        ["Recommendation ID", "Type", "Employee ID", "Customer ID", "Product Name", "Product ID"]),

    "Delivery": (
        ["d_no", "d_date", "d_time", "d_location", "c_id", "p_id"],
        ["Delivery No", "Delivery Date", "Delivery Time", "Location", "Customer ID", "Product ID"]),

    "Reviews": (
        ["re_no", "re_rating", "c_id"],
        ["Review No", "Rating", "Customer ID"]),

    "Chatbot": (
        ["b_questions", "b_answers", "c_id"],
        ["Question", "Answer", "Customer ID"]),

    "offline": (
        ["cash"],
        ["Cash"])
}

# tables whose first column is text (not an integer)
text_key_tables = ["Chatbot"]


class First:

    def __init__(self, root, table_name):
        self.root = root
        self.table = table_name
        self.columns = tables[table_name][0]
        self.headings = tables[table_name][1]

        n = len(self.columns)

        self.f = Frame(root, height=120 + 35 * n, width=500)
        self.f.pack()

        # create one Label and one Entry for every column
        self.entries = []
        for i in range(n):
            l = Label(self.f, text=self.headings[i])
            e = Entry(self.f, width=18)
            l.place(x=50, y=30 + i * 35)
            e.place(x=200, y=30 + i * 35)
            self.entries.append(e)

        self.b1 = Button(self.f, text="Submit", command=self.display)
        self.b2 = Button(self.f, text="Update", command=self.update)
        self.b3 = Button(self.f, text="Delete", command=self.delete)
        self.b4 = Button(self.f, text="Show", command=self.show)

        y = 50 + n * 35
        self.b1.place(x=50, y=y)
        self.b2.place(x=130, y=y)
        self.b3.place(x=210, y=y)
        self.b4.place(x=290, y=y)

        # show the records as soon as the window opens
        self.show()

    # read all the Entry boxes
    def get_values(self):
        values = []
        for e in self.entries:
            values.append(e.get().strip())
        return values

    # SUBMIT (INSERT)
    def display(self):
        try:
            values = self.get_values()

            if values[0] == "":
                messagebox.showwarning("Warning", self.headings[0] + " cannot be empty")
                return

            if self.table not in text_key_tables:
                int(values[0])      # gives ValueError if it is not a number

            # use only the filled boxes (empty ones become NULL / default value)
            col_list = []
            val_list = []
            for i in range(len(self.columns)):
                if values[i] != "":
                    col_list.append(self.columns[i])
                    val_list.append(values[i])

            sql = "INSERT INTO `" + self.table + "`(" + ",".join(col_list) + ") VALUES(" + ",".join(["%s"] * len(val_list)) + ")"

            cursor.execute(sql, val_list)
            conn.commit()

            print("Data Inserted")
            messagebox.showinfo("Message", "Record inserted successfully")
            self.show()

        except ValueError:
            messagebox.showerror("Error", self.headings[0] + " must be an integer")

        except mysql.connector.Error as err:
            conn.rollback()
            print("Error:", err)
            messagebox.showerror("Error", str(err))

    # UPDATE
    def update(self):
        try:
            values = self.get_values()

            if values[0] == "":
                messagebox.showwarning("Warning", "Enter " + self.headings[0] + " of the record to update")
                return

            if self.table not in text_key_tables:
                int(values[0])

            # SET part is made from the other filled boxes
            set_list = []
            val_list = []
            for i in range(1, len(self.columns)):
                if values[i] != "":
                    set_list.append(self.columns[i] + "=%s")
                    val_list.append(values[i])

            if len(set_list) == 0:
                messagebox.showwarning("Warning", "Enter at least one new value to update")
                return

            sql = "UPDATE `" + self.table + "` SET " + ",".join(set_list) + " WHERE " + self.columns[0] + "=%s"
            val_list.append(values[0])

            cursor.execute(sql, val_list)
            conn.commit()

            if cursor.rowcount > 0:
                print("Data Updated")
                messagebox.showinfo("Message", "Record updated successfully")
            else:
                print("ID Not Found")
                messagebox.showinfo("Message", self.headings[0] + " not found (or no change in data)")

            self.show()

        except ValueError:
            messagebox.showerror("Error", self.headings[0] + " must be an integer")

        except mysql.connector.Error as err:
            conn.rollback()
            print("Error:", err)
            messagebox.showerror("Error", str(err))

    # DELETE
    def delete(self):

        delete_win = Toplevel(self.root)
        delete_win.title("Delete " + self.table)
        delete_win.geometry("300x150")

        Label(delete_win, text="Enter " + self.headings[0]).pack(pady=10)

        e = Entry(delete_win, width=20)
        e.pack()

        def delete_record():
            try:
                key = e.get().strip()

                if key == "":
                    messagebox.showwarning("Warning", self.headings[0] + " cannot be empty")
                    return

                if self.table not in text_key_tables:
                    int(key)

                sql = "DELETE FROM `" + self.table + "` WHERE " + self.columns[0] + "=%s"

                cursor.execute(sql, (key,))
                conn.commit()

                if cursor.rowcount > 0:
                    print("Data Deleted")
                    messagebox.showinfo("Message", "Record deleted successfully")
                    delete_win.destroy()

                    # Refresh Show window
                    self.show()

                else:
                    print("ID Not Found")
                    messagebox.showinfo("Message", self.headings[0] + " not found")

            except ValueError:
                messagebox.showerror("Error", self.headings[0] + " must be an integer")

            except mysql.connector.Error as err:
                conn.rollback()
                print("Error:", err)
                messagebox.showerror("Error", str(err))

        Button(
            delete_win,
            text="Delete",
            command=delete_record
        ).pack(pady=10)

    # SHOW
    def show(self):
        next_win.show_records(self.root, conn, self.table, self.columns, self.headings)


# ----------------------------------------------------------
# Main menu: one button for every table
# ----------------------------------------------------------
def open_table(name):
    table_win = Toplevel(root)
    table_win.title(name + " Table")
    First(table_win, name)


root = Tk()
root.title("Welcome To Tkinter GUI Programme")
root.geometry("450x250")

Label(root, text="Select a table").grid(row=0, column=0, columnspan=3, pady=10)

r = 1
c = 0
for name in tables:
    # n=name makes each button remember its own table name
    Button(root, text=name, width=14, command=lambda n=name: open_table(n)).grid(row=r, column=c, padx=8, pady=8)
    c = c + 1
    if c == 3:
        c = 0
        r = r + 1

root.mainloop()
