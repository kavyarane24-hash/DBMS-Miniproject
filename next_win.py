from tkinter import *


win = None
frame = None


def show_records(parent, conn, table, columns, headings):

    global win, frame

    if win is None or not win.winfo_exists():
        win = Toplevel(parent)
        win.geometry("1100x400")

    win.title("Records of " + table)

    if frame is not None and frame.winfo_exists():
        frame.destroy()

    frame = Frame(win)
    frame.pack(fill=BOTH, expand=True)

    print("----------View records of " + table + "-----------")

    # HEADINGS
    for j in range(len(headings)):

        e = Entry(frame, width=16, fg='blue')

        e.grid(
            row=0,
            column=j,
            padx=2,
            pady=2
        )

        e.insert(END, headings[j])
        e.config(state='readonly')

    try:

        # Create cursor from the SAME connection
        # used by the main program
        cursor = conn.cursor()

        cursor.execute(
            "SELECT " + ",".join(columns) + " FROM `" + table + "` ORDER BY " + columns[0]
        )

        records = cursor.fetchall()

        cursor.close()

        if len(records) == 0:

            Label(
                frame,
                text="No records found in " + table
            ).grid(
                row=1,
                column=0,
                columnspan=len(headings)
            )

        else:

            for i, d in enumerate(records, start=1):

                for j in range(len(d)):

                    e = Entry(
                        frame,
                        width=16,
                        fg='green'
                    )

                    e.grid(
                        row=i,
                        column=j,
                        padx=2,
                        pady=2
                    )

                    e.insert(
                        END,
                        str(d[j])
                    )

                    e.config(state='readonly')

    except Exception as err:
        print("Error:", err)

    win.lift()
