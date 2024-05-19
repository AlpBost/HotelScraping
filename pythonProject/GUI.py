import tkinter as tk
from tkinter import ttk
from tkinter import font
import pandas as pd
from datetime import datetime


import Scrapping

main_window = tk.Tk()

city = tk.StringVar(main_window)
check_in = tk.StringVar(main_window)
check_out = tk.StringVar(main_window)
currency = tk.StringVar(main_window, value="TL")


def run():
    global main_window, city, check_in, check_out, currency
    main_window.title("Search Hotels")
    main_window.geometry("1200x900")


    cities = ["Paris",
              "London",
              "Athens",
              "Berlin",
              "Barcelona",
              "Warsaw",
              "Amsterdam",
              "Madrid",
              "Vienna",
              "Lisbon"]



    #-------------------------------------------------------------------------Creating text labels--------------------------------------------
    box_font = font.Font(family="Comic Sans MS", size=12, weight="bold")
    title_font = font.Font(family="Comic Sans MS", size=20, weight="bold",slant="italic")

    title_label = tk.Label(main_window, text="Best Hotel For You", font=title_font, fg="Black")
    title_label.pack(pady=20)

    input_frame = tk.Frame(main_window, bg="#b2dfdb", padx=20, pady=20, bd=2)
    input_frame.pack(pady=10)

    city_text = tk.Label(input_frame, text="Select City:", font=box_font, bg="#b2dfdb")
    city_text.grid(row=0, column=0, padx=20, pady=10, sticky=tk.W)

    city_dropdown = ttk.Combobox(input_frame, textvariable=city, values=cities, font=box_font, state='readonly')
    city_dropdown.grid(row=0, column=1, padx=20, pady=10)

    check_in_text = tk.Label(input_frame, text="Check-in Date:", font=box_font, bg="#b2dfdb")
    check_in_text.grid(row=1, column=0, padx=20, pady=10, sticky=tk.W)

    check_in_entry = tk.Entry(input_frame, textvariable=check_in, font=box_font)
    check_in_entry.grid(row=1, column=1, padx=20, pady=10)

    check_out_text = tk.Label(input_frame, text="Check-out Date:", font=box_font, bg="#b2dfdb")
    check_out_text.grid(row=2, column=0, padx=20, pady=10, sticky=tk.W)

    check_out_entry = tk.Entry(input_frame, textvariable=check_out, font=box_font)
    check_out_entry.grid(row=2, column=1, padx=20, pady=10)

    currency_text = tk.Label(input_frame, text="Currency:", font=box_font, bg="#b2dfdb")
    currency_text.grid(row=3, column=0, padx=20, pady=10, sticky=tk.W)

    euro_button = tk.Radiobutton(input_frame, text="Euro", font=box_font, variable=currency, value="Euro", bg="#b2dfdb")
    euro_button.grid(row=3, column=1, padx=5, pady=10, sticky=tk.W)

    tl_button = tk.Radiobutton(input_frame, text="TL", font=box_font, variable=currency, value="TL", bg="#b2dfdb")
    tl_button.grid(row=3, column=1, padx=120, pady=10, sticky=tk.W)

    search_box_font = font.Font(family="Comic Sans MS", size=13)
    search_button = tk.Button(main_window, text="Search", font=search_box_font, command=search, width=8, height=1, bg="#00796b", fg="white")
    search_button.place(x=740,y=265)

    # ---------------------------------------------------------------------Starting line-------------------------------------------------
    main_window.mainloop()


search_result_labels = []
def check_date(date_string):
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        current_date = datetime.now()

        if date_obj < current_date:
            return False
        else:
            return True
    except ValueError:
        return False

exception_font = font.Font(family="Comic Sans MS", size=12, weight="bold")
info_label = tk.Label(main_window, text="Please Select City And Enter Dates In (YYYY-MM-DD) Format",font=exception_font,fg="red")

def search():
    global selected_city, check_in_date, check_out_date, selected_currency, city, main_window, check_in, check_out, currency, search_result_labels
    selected_city = city.get()
    check_in_date = check_in.get()
    check_out_date = check_out.get()
    selected_currency = currency.get()

    #----------------------------------------------------------------Exception part----------------------------------------------------------
    if selected_city == "" or not check_date(check_in_date) or not check_date(check_out_date):
        info_label.config(text="Please select a city and enter valid dates (YYYY-MM-DD)!", fg="red")
        info_label.place(x=390, y=500)
    elif check_in_date == check_out_date:
        info_label.config(text="Check-in and Check-out dates cannot be the same.", fg="red")
        info_label.place(x=390, y=500)
    elif check_in_date > check_out_date:
        info_label.config(text="Check-out date cannot be before Check-in date.", fg="red")
        info_label.place(x=390, y=500)
    else:
        info_label.place_forget()
        for labels in search_result_labels:
            for label in labels:
                label.destroy()
        search_result_labels.clear()

        #-------------------------------------------------Calling Scrapping class method and collect infos in "hotel_info"-----------------
        Scrapping.scrap_hotel(selected_city, check_in_date, check_out_date)
        hotel_info = Scrapping.hotels_data

        #------------------------------------------------------------Checking connection---------------------------------------------------
        if hotel_info[0]['Name'] == "Connection Error":
            info_label.config(text="CONNECTION ERROR!!", fg="red")
            info_label.place(x=490, y=500)
            return

        #--------------------------------------------------------------Calculating TL to Euro-----------------------------------------------
        for hotel in hotel_info:
            price_str = str(hotel.get("Price")).replace(',', '')
            price_int_tr = int(price_str)
            price_int_eu = int(int(price_str) / 30)
            if selected_currency == "TL":
                hotel["Price"] = price_int_tr
            else:
                hotel["Price"] = price_int_eu

        #---------------------------------------------------------Sorting by looking Ratings of hotels -------------------------------------------
        #reverse true is essential to sort highest to lowest
        hotel_info_sorted = sorted(hotel_info, key=lambda x: float(x['Rating'].split()[1]) if 'Rating' in x and x['Rating'] != 'NOT GIVEN' else -1, reverse=True)

        name_labels = []
        address_labels = []
        distance_labels = []
        rating_labels = []
        price_labels = []

        # -------------------------------------------------------------'Search Result' maker------------------------------------------------
        box_font = font.Font(family="Comic Sans MS", size=12, weight="bold")
        tk.Label(main_window, text="Search Results", font=box_font).place(x=20, y=320)

        #---------------------------------------------------------------Showing Results to The User-------------------------------------------
        result_text = tk.Text(main_window, width=130, height=25, wrap=tk.WORD,font=("Courier", 12))
        result_text.place(x=10, y=350)

        # Count hotel number
        counter = 1

        for hotel in hotel_info_sorted[:5]:
            result_text.insert(tk.END, f"Hotel Number: {counter}\n")
            result_text.insert(tk.END, f"Name: {hotel.get('Name')}\n")
            result_text.insert(tk.END, f"Address: {hotel.get('Address')}\n")
            result_text.insert(tk.END, f"Distance to center: {hotel.get('Distance')}\n")
            result_text.insert(tk.END, f"Rating: {hotel.get('Rating')}\n")
            result_text.insert(tk.END, f"Price: {hotel.get('Price')}\n")
            result_text.insert(tk.END, "\n")
            counter += 1

        hotels_df = pd.DataFrame(hotel_info_sorted)[:5]
        hotels_df.to_csv('test_hotels.csv', header=True,index=False)

        search_result_labels = [name_labels, distance_labels, address_labels, rating_labels, price_labels]