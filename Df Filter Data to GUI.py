import customtkinter
import pandas as pd

NSE_FO_URL = "https://public.fyers.in/sym_details/NSE_FO.csv"

FutureOptionDF = pd.read_csv(NSE_FO_URL, header=None)
Symbol = FutureOptionDF[13].unique()
sorted_future_symbols = sorted(list(Symbol))


# Assuming FutureOptionDF and sorted_future_symbols are defined somewhere in your code

def getstrikedata(event=None):
    SelectedSymbol = IndexSymbolOption.get()
    
    # Clear previous data in the second ComboBox
    second_combobox.set("")
    
    InnerListdf = FutureOptionDF[FutureOptionDF[9].str.startswith(f"NSE:{SelectedSymbol}") & FutureOptionDF[9].str.endswith("FUT")]
    FutureStrikeList = InnerListdf[9].tolist()
    
    # Show the new list in the second ComboBox
    second_combobox.configure(values=FutureStrikeList)

# Assuming CTkComboBox is a valid class or function in your customtkinter library
app = customtkinter.CTk()
app.geometry("600x500")
app.title("CTk example")

# Define IndexSymbolOption before using it in getstrikedata
IndexSymbolOption = customtkinter.CTkComboBox(app, values=sorted_future_symbols, command=getstrikedata)
IndexSymbolOption.set("")
IndexSymbolOption.grid(row=1, column=0, padx=5, pady=5)

# Define second_combobox
second_combobox = customtkinter.CTkComboBox(app)
second_combobox.set("")
second_combobox.grid(row=2, column=0, padx=5, pady=5, ipadx=5)

app.mainloop()
