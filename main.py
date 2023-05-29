import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from datetime import datetime

# Fetch movie IDs from database
from sql import cursor, cnx


# Function to fetch all movie IDs
def refresh_movie_ids():
    cursor.execute("SELECT ID FROM MarvelMovies")
    return [item[0] for item in cursor.fetchall()]


# Function to add movie
def add_movie():
    movie_name = simpledialog.askstring("Input", "Enter movie name")
    movie_date = simpledialog.askstring("Input", "Enter movie date (Format: MonthDay,Year)")
    movie_phase = simpledialog.askstring("Input", "Enter MCU phase")

    if movie_name and movie_date and movie_phase:  # Ensure none of these are empty
        try:
            formatted_date = datetime.strptime(movie_date, '%B%d,%Y').date()
        except ValueError:
            messagebox.showerror("Invalid date", "The date you entered is not valid.")
            return  # Stop executing this function

        insert_query = "INSERT INTO MarvelMovies (MOVIE, DATE, MCU_PHASE) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (movie_name, formatted_date, movie_phase))
        cnx.commit()

        refresh_dropdown()


# Function to list all movies
def list_all_movies():
    cursor.execute("SELECT * FROM MarvelMovies")
    all_movies = cursor.fetchall()

    textbox.delete('1.0', tk.END)
    for movie in all_movies:
        textbox.insert(tk.END, f"{movie[0]} {movie[1]} {movie[2]} {movie[3]}\n")


# Function to update textbox
def update_textbox():
    selected_id = dropdown.get()
    if selected_id:  # Ensure the dropdown isn't empty
        cursor.execute(f"SELECT * FROM MarvelMovies WHERE ID={selected_id}")
        movie = cursor.fetchone()

        textbox.delete('1.0', tk.END)
        textbox.insert(tk.END, f"{movie[0]} {movie[1]} {movie[2]} {movie[3]}\n")


# Function to refresh dropdown values
def refresh_dropdown():
    movie_ids = refresh_movie_ids()
    dropdown['values'] = movie_ids


# Create the main window
root = tk.Tk()

# Create widgets
textbox = tk.Text(root)
dropdown = ttk.Combobox(root, postcommand=update_textbox)
button_add = tk.Button(root, text="Add", command=add_movie)
button_list_all = tk.Button(root, text="LIST ALL", command=list_all_movies)

# Place widgets
dropdown.pack()
textbox.pack()
button_add.pack()
button_list_all.pack()

# Refresh dropdown values
refresh_dropdown()

# Start main loop
root.mainloop()

# Close cursor and connection
cursor.close()
cnx.close()
