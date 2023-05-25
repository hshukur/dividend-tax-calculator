# importing necessary modules
import tkinter
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
from error_handling import ErrorChecker
from data_processing import DataProcessor

# defining constants
FONT_TYPE = "Verdana"
BG_COLOR = "#FCFCFC"

# root window setup
root = ThemedTk(theme="breeze")
root.title("Dividend Tax Calculator")
root.minsize(width=700, height=550)

# defining frames within root window
first_frame = tkinter.Frame(root, width=700, height=100)
first_frame.grid(column=0, row=0, pady=10)

second_frame = tkinter.Frame(root, width=700, height=200)
second_frame.grid(column=0, row=1, pady=4)

third_frame = tkinter.Frame(root, width=700, height=100)
third_frame.grid(column=0, row=2, pady=4)

forth_frame = tkinter.Frame(root, width=700, height=100)
forth_frame.grid(column=0, row=3, pady=6)

fifth_frame = tkinter.Frame(root, width=700, height=100)
fifth_frame.grid(column=0, row=4, pady=8)

# configuration of the first_frame
welcome_text = "Welcome to the dividend tax calculator!"
welcome_label = tkinter.Label(first_frame, text=welcome_text, font=(FONT_TYPE, 14), width=58)
welcome_label.grid(column=0, row=0)

# configuration of the second frame
div_number_text = "Please select how many times have you received: "
div_number_label = tkinter.Label(second_frame, text=div_number_text, font=(FONT_TYPE, 12), width=42)
div_number_label.grid(column=0, row=0, padx=5)

# this dictionary is used to store and access widgets of the third frame
dictionary_for_widgets = {}

def submit_btn_clicked():
    """
    Invoked when submit_button is clicked
    Calculates the tax amount based on the values provided
    Prints results in the fifth_frame
    """
    indexer = 0
    sum_gain = 0
    sum_total_tax = 0
    sum_tax_paid = 0
    sum_tax_to_be_paid = 0
    final_text_to_be_displayed = "Amounts shown are in PLN\n" \
                                 "Per entry calculation:\n"
    for each_key in dictionary_for_widgets:
        # extracting values from the dictionary
        # the index values are [2] and [5] here to extract Entry widgets from the list
        row_number = list(dictionary_for_widgets.keys())[indexer]
        div_amount = dictionary_for_widgets[each_key][2].get()
        transaction_date = dictionary_for_widgets[each_key][5].get()

        # error-check
        value_checker = ErrorChecker(div_amount, transaction_date)
        if value_checker.check_div_amount() or value_checker.check_txn_date():
            tkinter.messagebox.showwarning("Error", "The data provided is not valid")
        else:
            # calculate 19%
            nineteen_percent_tax = float(div_amount) * 0.19

            # calculate 15%
            fifteen_percent_tax = float(div_amount) * 0.15

            # calculate 4%
            four_percent_tax = float(div_amount) * 0.04

            # get FX rate
            data_proc = DataProcessor(transaction_date)
            usd_fx_rate = float(data_proc.get_data_from_nbp())

            # calculate gain in PLN
            gain_per_entry = round((float(div_amount) * usd_fx_rate), 2)

            # calculate 19% in PLN
            total_tax_per_entry = round((nineteen_percent_tax * usd_fx_rate), 2)

            # calculate 15% in PLN
            tax_paid_per_entry = round((fifteen_percent_tax * usd_fx_rate), 2)

            # calculate 4% in PLN
            tax_to_be_paid_per_entry = round((four_percent_tax * usd_fx_rate), 2)

            # text entry for each row
            tax_amount_per_entry = f"{row_number}. " \
                                   f"Gain: {gain_per_entry:.2f}  |  " \
                                   f"Total tax: {total_tax_per_entry:.2f}  |  " \
                                   f"Tax paid in USA {tax_paid_per_entry:.2f}  |  " \
                                   f"Tax to be paid {tax_to_be_paid_per_entry:.2f}\n"
            final_text_to_be_displayed += tax_amount_per_entry

            # accumulating the tax value and text
            sum_gain += gain_per_entry
            sum_total_tax += total_tax_per_entry
            sum_tax_paid += tax_paid_per_entry
            sum_tax_to_be_paid += tax_to_be_paid_per_entry

            # adding +1 to the indexer to get the next row number
            indexer += 1

    # the sum_tax_to_be_paid can be zero if ValueError is triggered
    if sum_tax_to_be_paid != 0:
        sum_tax_text = f"\nTotal calculation:\n" \
                       f"Gain: {round(sum_gain, 2)}  |  " \
                       f"Tax paid in USA {round(sum_tax_paid, 2)}  |  " \
                       f"Tax to be paid {round(sum_tax_to_be_paid, 2)}\n"
        final_text_to_be_displayed += sum_tax_text

        # putting the final text into the widget
        result_widget = tkinter.Text(fifth_frame, height=10, width=70, font=(FONT_TYPE, 9), padx=8, pady=5, bg=BG_COLOR)
        result_widget.insert(tkinter.END, final_text_to_be_displayed)
        result_widget.config(state="disabled")
        result_widget.grid(column=0, row=indexer + 1)

def rdb_used():
    """
    Invoked when new_rdb_1, new_rdb_2, new_rdb_3, or new_rdb_4 is selected
    Checks if there are already widgets in third_frame
    There might be widgets already in third_frame if the radiobutton selection changes
        If any widget is present at the time of selection, destroys everything
    """
    # getting the value of the radiobutton selected
    selected_rdb = new_rdb_state.get()

    # dividends information label
    div_data_req_text = "Please provide information here:"
    div_data_req_label = ttk.Label(third_frame, text=div_data_req_text, font=(FONT_TYPE, 12))
    div_data_req_label.grid(column=0, row=0, columnspan=6, pady=8)

    row_number = 1

    # checking if dictionary is empty or not
    if bool(dictionary_for_widgets):
        for each_key in dictionary_for_widgets.copy():
            for each_index in range(len(dictionary_for_widgets[each_key])):
                dictionary_for_widgets[each_key][each_index].destroy()
            dictionary_for_widgets.pop(each_key)

    # removes widgets from fifth_frame to refresh the window
    for each_wid in fifth_frame.winfo_children():
        each_wid.destroy()

    # initializes the nesessary amount of rows with widgets based on radiobutton selection
    for each in range(1, selected_rdb + 1):
        # a list to store all widgets within each row
        list_for_widgets = []

        # row number label
        row_num_label = ttk.Label(third_frame, text=f"{each}.", font=(FONT_TYPE, 10))
        row_num_label.grid(column=0, row=row_number, padx=2, pady=6)
        list_for_widgets.append(row_num_label)

        # dividend amount label
        div_amount_label = ttk.Label(third_frame, text="Dividend amount in USD", font=(FONT_TYPE, 10))
        div_amount_label.grid(column=1, row=row_number, padx=3)
        list_for_widgets.append(div_amount_label)

        # dividend amount entry
        div_amount_entry = ttk.Entry(third_frame, width=6, font=(FONT_TYPE, 10))
        div_amount_entry.insert(tkinter.END, string="10.0")
        div_amount_entry.grid(column=2, row=row_number)
        list_for_widgets.append(div_amount_entry)

        # space label
        space_label = ttk.Label(third_frame, text="   ", font=(FONT_TYPE, 10))
        space_label.grid(column=3, row=row_number)
        list_for_widgets.append(space_label)

        # transaction date label
        txn_date_label = ttk.Label(third_frame, text="Transaction date", font=(FONT_TYPE, 10))
        txn_date_label.grid(column=4, row=row_number, padx=3)
        list_for_widgets.append(txn_date_label)

        # transaction date entry
        txn_date_entry = ttk.Entry(third_frame, width=20, font=(FONT_TYPE, 10))
        txn_date_entry.insert(tkinter.END, string="YYYY-MM-DD format")
        txn_date_entry.grid(column=5, row=row_number)
        list_for_widgets.append(txn_date_entry)

        # adding each row as a key:value pair to dictionary_for_widgets
        dictionary_for_widgets[each] = list_for_widgets

        # next row
        row_number += 1

    # submit button
    submit_button = ttk.Button(forth_frame, text="Submit", command=submit_btn_clicked)
    submit_button.grid(column=0, row=0)

# setting up radiobuttons
new_rdb_state = tkinter.IntVar()
new_rdb_1 = ttk.Radiobutton(second_frame, text="1", value=1, variable=new_rdb_state, command=rdb_used)
new_rdb_2 = ttk.Radiobutton(second_frame, text="2", value=2, variable=new_rdb_state, command=rdb_used)
new_rdb_3 = ttk.Radiobutton(second_frame, text="3", value=3, variable=new_rdb_state, command=rdb_used)
new_rdb_4 = ttk.Radiobutton(second_frame, text="4", value=4, variable=new_rdb_state, command=rdb_used)
new_rdb_1.grid(column=1, row=0, pady=5)
new_rdb_2.grid(column=2, row=0, pady=5)
new_rdb_3.grid(column=3, row=0, pady=5)
new_rdb_4.grid(column=4, row=0, pady=5)


root.mainloop()
