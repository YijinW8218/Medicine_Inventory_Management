"""read and edit storage files using datas from gui"""
# initialize
import pandas as pd
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_STORE_PATH = PROJECT_DIR / "store.xlsx"

# basic functions
def open_file(path=DEFAULT_STORE_PATH):
    # read excel file and assaign the sheets
    # remeber to call in the begining of 'main.py'
    df = pd.read_excel(path,sheet_name=['Medicine','Batch'],header=0)  # data frame
    med_sheet = df['Medicine']
    batch_sheet = df['Batch']

    # normalize the column names
    med_sheet.columns = med_sheet.columns.str.strip()
    batch_sheet.columns = batch_sheet.columns.str.strip()

    return med_sheet, batch_sheet


def save_file(med_sheet, batch_sheet, path=DEFAULT_STORE_PATH):
    # sort rows by columns
    med_sheet = med_sheet.sort_values(by=['Medicine Field','Medicine Type', 'Medicine Name'], ascending=[True,True,True])
    batch_sheet = batch_sheet.sort_values(by=['Expire Date','Medicine Name'],ascending=[True,True])
    # update to orginal file
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        med_sheet.to_excel(writer, sheet_name="Medicine", index=False)
        batch_sheet.to_excel(writer, sheet_name="Batch", index=False)





## med_sheet functions
def new_med(med_sheet, new_med_info):
    print(f"DEBUG:new_med:{new_med_info}")
    field, type_, name, route, temp = list(new_med_info.values())
    new_row = {
        "Medicine Field": field,
        "Medicine Type": type_,
        "Medicine Name": name,
        "Route": route,
        "Temperature": temp}
    # data frame append
    med_sheet = pd.concat([med_sheet, pd.DataFrame([new_row])], ignore_index=True)
    return med_sheet

def remove_med(med_sheet, batch_sheet,med_name):
    print(f"DEBUG:remove_med:{med_name}")
    med_sheet = med_sheet[med_sheet["Medicine Name"] != med_name]
    # remove related batch
    batch_sheet = batch_sheet[batch_sheet["Medicine Name"].str.strip().str.lower() != med_name.strip().lower()]

    return med_sheet, batch_sheet

## batch_sheet functions
def new_batch(batch_sheet, new_batch_info):
    print(f"DEBUG:new_batch:{new_batch_info}")
    med_name, batch_number, quantity, location, exp_date, supplier = list(new_batch_info.values())
    new_row = {
        "Medicine Name": med_name,
        "Batch Number": batch_number,
        "Quantity": quantity,
        "Location": location,
        "Expire Date": exp_date,
        "Supplier": supplier}
    # data frame append
    batch_sheet = pd.concat([batch_sheet, pd.DataFrame([new_row])], ignore_index=True)
    return batch_sheet

def get_med(batch_sheet, med_name, amount):
    print(f"DEBUG:get_med:", med_name)
    ori_quantity = int(batch_sheet.loc[batch_sheet["Medicine Name"]==med_name, "Quantity"].iloc[0])
    if ori_quantity > amount:  # more than enough
        batch_sheet.loc[batch_sheet["Medicine Name"]==med_name, "Quantity"] = ori_quantity - amount
    elif ori_quantity == int(med_name[name]):  # just enough
        batch_sheet = batch_sheet[batch_sheet["Medicine Name"] != med_name]  # remove the batch
    else:  # not enough
        print(f"WARNING: Not enough {name} in storage. Available: {ori_quantity}, Requested: {med_name[name]}")
    return batch_sheet




    




