from tkinter import *
import formulas
inv = formulas.InventorySystem()
import file_manager as fm




# input validation
def validate_input(value, expected_type, name=None):
    """Validate that 'value' type is expected_type"""
    # Normalize expected_type into a tuple of types
    if isinstance(expected_type, (list, tuple)):
        types_tuple = tuple(expected_type)
    elif isinstance(expected_type, str):
        _type_map = {
            'int': int, 'float': float, 'str': str,
            'bool': bool, 'list': list, 'dict': dict
        }
        try:
            types_tuple = (_type_map[expected_type.lower()],)
        except KeyError:
            raise ValueError(f"Unknown expected_type string: {expected_type!r}")
    elif isinstance(expected_type, type):
        types_tuple = (expected_type,)
    else:
        raise TypeError("expected_type must be a type, tuple/list of types, or a type-name string")

    if not isinstance(value, types_tuple):
        name_str = f" '{name}'" if name else ""
        expected_names = ", ".join(t.__name__ for t in types_tuple)
        raise TypeError(f"Invalid type for{name_str}: expected {expected_names}, got {type(value).__name__}")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Create_Medicine(missing_label,success_label,field_entry,type_entry,name_entry,route_entry,temp_listbox):
    if missing_label.winfo_ismapped():
        missing_label.place_forget()
    if success_label.winfo_ismapped():
        success_label.place_forget()
    field = field_entry.get()
    type_ = type_entry.get()
    name = name_entry.get()
    route = route_entry.get()
    temp_selected = temp_listbox.curselection()
    # validate input
    for i, j in {"field": field, "type_": type_, "name": name, "route": route}.items():
        validate_input(j, str, i)
    # validate pass
    if any(not x.strip() for x in (field, type_, name, route)) or not temp_selected:  # check missing
        # missing label
        if not missing_label.winfo_ismapped():
            missing_label.place(x=550,y=630)
    else:
        temp = temp_listbox.get(temp_selected[0])
        inv.new_med(field, type_, name, route, temp)  # create medicine
        # update dataframe
        global med_sheet
        med_sheet = fm.new_med(med_sheet, {
                                            "Medicine Field": field,
                                            "Medicine Type": type_,
                                            "Medicine Name": name,
                                            "Route": route,
                                            "Temperature": temp})
        # success label
        if missing_label.winfo_ismapped():
            missing_label.place_forget()
        success_label.place(x=500,y=630)
        # clear entries
        field_entry.delete(0,END)
        type_entry.delete(0,END)    
        name_entry.delete(0,END)
        route_entry.delete(0,END)
        temp_listbox.selection_clear(0,END)

# create Create_Medicine window
def open_Create_Medicine_window(menu_window):
    create_med_window = Toplevel(menu_window)
    create_med_window.geometry("1000x800")
    create_med_window.title("Medicine Inventory Management System(Create Medicine)")
    create_med_window.config(bg="#E8E5DB")

    # title label
    title_label = Label(create_med_window,
                        text="Create a New Medicine",font=('Arial',45,'bold'),bg="#A42423",fg="#E8E5DB")
    title_label.place(x=250,y=80)

    # labels for attributes
    field_label = Label(create_med_window,text="Field:",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    type_label = Label(create_med_window,text="Type:",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    name_label = Label(create_med_window,text="Name:",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    route_label = Label(create_med_window,text="Route:",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    temp_label = Label(create_med_window,text="Storage Temperature:",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    labels = [field_label, type_label, name_label, route_label, temp_label]
    # display labels
    label_top = 200
    for i in labels:
        i.place(x=200,y=label_top)
        label_top += 60
    # entries for attributes
    field_entry = Entry(create_med_window,font=('Arial',18))
    field_entry.place(x=260,y=200,width=400,height=35)
    type_entry = Entry(create_med_window,font=('Arial',18))
    type_entry.place(x=260,y=260,width=400,height=35)
    name_entry = Entry(create_med_window,font=('Arial',18))
    name_entry.place(x=270,y=320,width=400,height=35)
    route_entry = Entry(create_med_window,font=('Arial',18))
    route_entry.place(x=270,y=380,width=400,height=35)
    temp_listbox = Listbox(create_med_window,
                           font=('Arial',18,'bold'),
                           selectmode=SINGLE,
                           bg="#FFFFFF",
                           fg="#111111")
    temp_listbox.place(x=410, y=440, width=280)
    temp_listbox.insert(END,'Room temperature(20-25°C)')
    temp_listbox.insert(END,'Cool place(8-15°C)')
    temp_listbox.insert(END,'Refrigerated(2-8°C)')
    temp_listbox.insert(END,'Frozen(-25 to -10°C)')
    temp_listbox.config(height=temp_listbox.size())
    # allert label
    missing_label = Label(create_med_window,text="Attribute(s) missing!!!",font=('Arial',12),bg="#E8E5DB",fg="#FD0000")
    success_label = Label(create_med_window,text="Medicine created successfully!",font=('Arial',12),bg="#E8E5DB",fg="#00AA00")
    # submit button
    submit_button = Button(create_med_window,text="Submit",font=('Arial',18,'bold'),fg="#A42423")
    submit_button.place(x=550,y=650,width=100,height=40)
    submit_button.config(command=lambda: Create_Medicine(missing_label, success_label, field_entry,type_entry,name_entry,route_entry,temp_listbox))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Create_Batch(missing_label,not_found_label,success_label,  med_name_entry,batch_number_entry,quantity_entry,location_entry,exp_date_entry,supplier_entry):
    if missing_label.winfo_ismapped():
        missing_label.place_forget()
    if not_found_label.winfo_ismapped():
        not_found_label.place_forget()
    if success_label.winfo_ismapped():
        success_label.place_forget()
    med_name = med_name_entry.get()
    batch_number = batch_number_entry.get()
    quantity = quantity_entry.get()
    location = location_entry.get()
    exp_date = exp_date_entry.get()
    supplier = supplier_entry.get()
    # validate input
    for i,j in {"med_name": med_name,"batch_number": batch_number,"quantity": quantity,"location": location,"exp_date": exp_date,"supplier": supplier}.items():
        validate_input(j, str, i)
    # validate pass
    if any(not x.strip() for x in (med_name, batch_number, quantity, location, exp_date, supplier)):  # check missing
        # missing label
        if not missing_label.winfo_ismapped():
            missing_label.place(x=700,y=560)
    else:
        # find medicine object
        med_objs = inv.search_medicine("name", med_name)  # function return a list
        if not med_objs:  # medicine not found
            if not not_found_label.winfo_ismapped():
                not_found_label.place(x=200,y=180)
        else:
            med_obj = med_objs[0]  # medicine name is unique
            inv.new_batch(med_obj, batch_number, int(quantity), location, exp_date, supplier)  # create batch
            # update dataframe
            global batch_sheet
            batch_sheet = fm.new_batch(batch_sheet,{
                                        "Medicine Name": med_name,
                                        "Batch Number": batch_number,
                                        "Quantity": quantity,
                                        "Location": location,
                                        "Expire Date": exp_date,
                                        "Supplier": supplier})
            # success label
            if missing_label.winfo_ismapped():
                missing_label.place_forget()  
            if not_found_label.winfo_ismapped():
                not_found_label.place_forget()
            success_label.place(x=700,y=560)
            # clear entries
            med_name_entry.delete(0,END)
            batch_number_entry.delete(0,END)    
            quantity_entry.delete(0,END)
            location_entry.delete(0,END)
            exp_date_entry.delete(0,END)
            supplier_entry.delete(0,END)

# create Create_Batch window
def open_Create_Batch_window(menu_window):
    create_batch_window = Toplevel(menu_window)
    create_batch_window.geometry("1000x800")
    create_batch_window.title("Medicine Inventory Management System(Create Batch)")
    create_batch_window.config(bg="#E8E5DB")

    # title label
    title_label = Label(create_batch_window,
                        text="Store a New Batch",font=('Arial',45,'bold'),bg="#A42423",fg="#E8E5DB")
    title_label.place(x=250,y=80)

    # labels for attributes
    med_name_label = Label(create_batch_window,text="Medicine Name:",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    batch_number_label = Label(create_batch_window,text="Batch Number:",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    quantity_label = Label(create_batch_window,text="Quantity(boxes):",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    location_label = Label(create_batch_window,text="Location:",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    exp_date_label = Label(create_batch_window,text="Expiration Date(MM/DD/YYYY):",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    supplier_label = Label(create_batch_window,text="Supplier:",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    labels = [med_name_label, batch_number_label, quantity_label, location_label, exp_date_label, supplier_label]
    # display labels
    label_top = 200
    for i in labels:
        i.place(x=200,y=label_top)
        label_top += 60
    # entries for attributes
    med_name_entry = Entry(create_batch_window,font=('Arial',18))
    med_name_entry.place(x=355,y=200,width=400,height=35)
    batch_number_entry = Entry(create_batch_window,font=('Arial',18)) 
    batch_number_entry.place(x=345,y=260,width=400,height=35)
    quantity_entry = Entry(create_batch_window,font=('Arial',18))
    quantity_entry.place(x=355,y=320,width=400,height=35)
    location_entry = Entry(create_batch_window,font=('Arial',18))
    location_entry.place(x=295,y=380,width=400,height=35)
    exp_date_entry = Entry(create_batch_window,font=('Arial',18))
    exp_date_entry.place(x=495,y=440,width=200,height=35)
    supplier_entry = Entry(create_batch_window,font=('Arial',18))
    supplier_entry.place(x=295,y=500,width=400,height=35)
    # allert label
    missing_label = Label(create_batch_window,text="Attribute(s) missing!!!",font=('Arial',12),bg="#E8E5DB",fg="#FD0000")
    not_found_label = Label(create_batch_window,text="Medicine not found!!!",font=('Arial',12),bg="#E8E5DB",fg="#FD0000")
    success_label = Label(create_batch_window,text="Batch created successfully!",font=('Arial',12),bg="#E8E5DB",fg="#00AA00")
    # submit button
    submit_button = Button(create_batch_window,text="Submit",font=('Arial',18,'bold'),fg="#A42423")
    submit_button.place(x=700,y=580,width=100,height=40)
    submit_button.config(command=lambda: Create_Batch(missing_label,not_found_label,success_label, med_name_entry,batch_number_entry,quantity_entry,location_entry,exp_date_entry,supplier_entry))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Remove_Medicine(med_name_entry,missing_label,not_found_label,success_label):
    if missing_label.winfo_ismapped():
        missing_label.place_forget()
    if not_found_label.winfo_ismapped():
        not_found_label.place_forget()
    if success_label.winfo_ismapped():
        success_label.place_forget()
    med_name = med_name_entry.get()
    # validate input
    validate_input(med_name, str, "med_name")
    # validate pass
    if not med_name.strip():  # check missing
        # missing label
        if not missing_label.winfo_ismapped():
            missing_label.place(x=505,y=275)
    else:
        # find medicine object
        med_objs = inv.search_medicine("name", med_name)  # function return a list
        if not med_objs:  # medicine not found
            if not not_found_label.winfo_ismapped():
                not_found_label.place(x=350,y=245)
        else:
            med_obj = med_objs[0]  # medicine name is unique
            inv.remove_med(med_name)  # remove medicine
            # update dataframe
            global med_sheet, batch_sheet
            med_sheet, batch_sheet = fm.remove_med(med_sheet, batch_sheet,str(med_name))
            # success label
            if missing_label.winfo_ismapped():
                missing_label.place_forget()  
            if not_found_label.winfo_ismapped():
                not_found_label.place_forget() 
            success_label.place(x=295,y=270)
            # clear entry
            med_name_entry.delete(0,END)

    
# create Remove_Medicine window
def open_Remove_Medicine_window(menu_window):
    remove_med_window = Toplevel(menu_window)
    remove_med_window.geometry("1000x800")
    remove_med_window.title("Medicine Inventory Management System(Remove Medicine)")
    remove_med_window.config(bg="#E8E5DB")

    # title label
    title_label = Label(remove_med_window,
                        text="Remove a Medicine",font=('Arial',45,'bold'),bg="#A42423",fg="#E8E5DB")
    title_label.place(x=250,y=80)
    # labels for attributes
    med_name_label = Label(remove_med_window,text="Medicine Name:",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    med_name_label.place(x=200,y=200)
    # entry for attribute
    med_name_entry = Entry(remove_med_window,font=('Arial',18))
    med_name_entry.place(x=355,y=200,width=400,height=35)
    # allert label
    missing_label = Label(remove_med_window,text="Medicine Name missing!",font=('Arial',12),bg="#E8E5DB",fg="#FD0000")
    not_found_label = Label(remove_med_window,text="Medicine not found!!!",font=('Arial',12),bg="#E8E5DB",fg="#FD0000")
    success_label = Label(remove_med_window,text="Medicine removed successfully!",font=('Arial',12),bg="#E8E5DB",fg="#00AA00")
    # submit button
    submit_button = Button(remove_med_window,text="Click and Delete This Medicine.",font=('Arial',18,'bold'),fg="#A42423")
    submit_button.place(x=500,y=300,width=300,height=40)
    submit_button.config(command=lambda: Remove_Medicine(med_name_entry,missing_label,not_found_label,success_label))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Get_Medicine(med_name_entry,amount_entry,missing_label,not_found_label,success_label):
    if missing_label.winfo_ismapped():
        missing_label.place_forget()
    if not_found_label.winfo_ismapped():
        not_found_label.place_forget()
    if success_label.winfo_ismapped():
        success_label.place_forget()
    med_name = med_name_entry.get()
    amount = int(amount_entry.get())
    # validate input
    validate_input(med_name, str, "med_name")
    validate_input(amount, int, "input amount")
    # validate pass
    if not med_name.strip() or not amount:  # check missing
        # missing label
        if not missing_label.winfo_ismapped():
            missing_label.place(x=505,y=335)
    else:
        # find medicine object
        med_objs = inv.search_medicine("name", med_name)  # function return a list
        if not med_objs:  # medicine not found
            if not not_found_label.winfo_ismapped():
                not_found_label.place(x=355,y=180)
        else:
            med_obj = med_objs[0]  # medicine name is unique
            print("!!!!!!!!!!!!!!!!!!!!!!!:",med_obj.batches,'\n',[med.batches.queue for med in inv.medicines.values()])
            inv.get_medicine(med_obj,int(amount))  # get medicine
            print("After getting medicine, batches are:",med_obj.batches,'\n',[med.batches.queue for med in inv.medicines.values()])
            # update dataframe
            global batch_sheet
            batch_sheet = fm.get_med(batch_sheet, med_name, amount)
            # success label
            if missing_label.winfo_ismapped():
                missing_label.place_forget()  
            if not_found_label.winfo_ismapped():
                not_found_label.place_forget() 
            success_label.place(x=295,y=330)
            # clear entry
            med_name_entry.delete(0,END)
            amount_entry.delete(0,END)

# create Get_Medicine window
def open_Get_Medicine_window(menu_window):
    get_med_window = Toplevel(menu_window)
    get_med_window.geometry("1000x800")
    get_med_window.title("Medicine Inventory Management System(Get Medicine)")
    get_med_window.config(bg="#E8E5DB")

    # title label
    title_label = Label(get_med_window,
                        text="Get Medicine from Inventory",font=('Arial',45,'bold'),bg="#A42423",fg="#E8E5DB")
    title_label.place(x=150,y=80)
    # labels for attributes
    med_name_label = Label(get_med_window,text="Medicine Name:",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    med_name_label.place(x=200,y=200)
    amount_label = Label(get_med_window,text="Amount(boxes):",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    amount_label.place(x=200,y=260)
    # entry for attribute
    med_name_entry = Entry(get_med_window,font=('Arial',18))
    med_name_entry.place(x=355,y=200,width=400,height=35)
    amount_entry = Entry(get_med_window,font=('Arial',18))
    amount_entry.place(x=355,y=260,width=400,height=35)
    # allert label
    missing_label = Label(get_med_window,text="Attribute(s) missing!",font=('Arial',12),bg="#E8E5DB",fg="#FD0000")
    not_found_label = Label(get_med_window,text="Medicine not found!!!",font=('Arial',12),bg="#E8E5DB",fg="#FD0000")
    success_label = Label(get_med_window,text="Got Medicine successfully!",font=('Arial',12),bg="#E8E5DB",fg="#00AA00")
    # submit button
    submit_button = Button(get_med_window,text="Click and Get The Medicine.",font=('Arial',18,'bold'),fg="#A42423")
    submit_button.place(x=500,y=360,width=300,height=40)
    submit_button.config(command=lambda: Get_Medicine(med_name_entry,amount_entry,missing_label,not_found_label,success_label))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def open_Search_Med_window(menu_window,by_attribute):
    search_med_window = Toplevel(menu_window)
    search_med_window.geometry("1000x800")
    search_med_window.title("Search(Search Medicine)")
    search_med_window.config(bg="#E8E5DB")

    # title label
    title_text = f"Search Medicine by {by_attribute}"
    title_label = Label(search_med_window,
                        text=title_text,font=('Arial',45,'bold'),bg="#A42423",fg="#E8E5DB")
    title_label.place(x=150,y=80)
    # label for attributes
    attribute_text = f"{by_attribute}:"
    attribute_label = Label(search_med_window,text=attribute_text,font=('Arial',25,'bold'),bg="#E8E5DB",fg="#A42423")
    attribute_label.place(x=200,y=200)
    # entry for attributes
    attribute_entry = Entry(search_med_window,font=('Arial',18))
    attribute_entry.place(x=355,y=260,width=400,height=35)
    # text to display searching result
    result_text = Text(search_med_window,font=('Arial',18),state=DISABLED)
    result_text.place(x=150,y=400,width=550,height=250)

    # search function
    def search_function(by_attribute,attribute_entry,result_text):
        # normalize
        if by_attribute == "store temperature":
            by_attribute = "temp"
        attribute_val = attribute_entry.get()
        # search
        result_meds = inv.search_medicine(by_attribute, attribute_val)
        if not result_meds:
            text = "No matching medicine found."
        else:
            text = ""
            for i in result_meds:
                text += f"{i.name}\n"
        # display result
        result_text.config(state="normal")  # start to write in
        result_text.delete(1.0, END)         # clear old content
        result_text.insert(1.0, text)            # write in
        result_text.config(state="disabled")  # write in finished

    # search button
    search_button = Button(search_med_window,text="Search",font=('Arial',18,'bold'),fg="#A42423")
    search_button.place(x=500,y=320,width=300,height=40)
    search_button.config(command=lambda: search_function(by_attribute,attribute_entry,result_text))

def open_Search_Batch_window(menu_window,by_attribute):
    search_batch_window = Toplevel(menu_window)
    search_batch_window.geometry("1000x800")
    search_batch_window.title("Search(Search Medicine)")
    search_batch_window.config(bg="#E8E5DB")

    # title label
    title_text = f"Search Batch by {by_attribute}"
    title_label = Label(search_batch_window,
                        text=title_text,font=('Arial',45,'bold'),bg="#A42423",fg="#E8E5DB")
    title_label.place(x=150,y=80)
    # label for attributes
    med_name_label = Label(search_batch_window,text="Medicine Name:",font=('Arial',25,'bold'),bg="#E8E5DB",fg="#A42423")
    med_name_label.place(x=200,y=170)
    attribute_text = f"{by_attribute}:"
    attribute_label = Label(search_batch_window,text=attribute_text,font=('Arial',25,'bold'),bg="#E8E5DB",fg="#A42423")
    attribute_label.place(x=200,y=200)
    # entry for attributes
    med_name_entry = Entry(search_batch_window,font=('Arial',18))
    med_name_entry.place(x=404,y=170,width=400,height=35)
    attribute_entry = Entry(search_batch_window,font=('Arial',18))
    attribute_entry.place(x=405,y=200,width=400,height=35)
    # text to display searching result
    result_text = Text(search_batch_window,font=('Arial',18),state=DISABLED)
    result_text.place(x=150,y=400,width=550,height=250)

    # search function
    def search_function(by_attribute,med_name_entry,attribute_entry,result_text):
        # normalize
        if by_attribute == "batch number":
            by_attribute = "batch_number"
        elif by_attribute == "quantity(boxes)":
            by_attribute = "quantity"
        elif by_attribute == "expire date":
            by_attribute = "exp_date"
        med_name = med_name_entry.get()
        attribute_val = attribute_entry.get()
        # search
        med_objs = inv.search_medicine("name", med_name)  # function return a list
        if not med_objs:  # medicine not found
            text = "Medicine not found."
            # display result
            result_text.config(state="normal")  # start to write in
            result_text.delete(1.0, END)         # clear old content
            result_text.insert(1.0, text)            # write in
            result_text.config(state="disabled")  # write in finished
            return
        med_obj = med_objs[0]  # medicine name is unique
        print(f"DEBUG: seaching batch find med_obj:{med_obj}\nby_attribute:{by_attribute}\nattribute_val:{attribute_val}")
        result_batchs = inv.search_batch(med_obj,by_attribute, attribute_val)
        print(f"DEBUG: seaching batch find result_batchs:{result_batchs}")
        if not result_batchs:
            text = "No matching batch found."
        else:
            text = ""
            for batch in result_batchs:
                text += f"Batch Number: {batch.batch_number},Quantity: {batch.quantity}, Location: {batch.location}, Expiry Date: {batch.exp_date}, Supplier: {batch.supplier}\n"
        # display result
        result_text.config(state="normal")  # start to write in
        result_text.delete(1.0, END)         # clear old content
        result_text.insert(1.0, text)            # write in
        result_text.config(state="disabled")  # write in finished

        

    # search button
    search_button = Button(search_batch_window,text="Search",font=('Arial',18,'bold'),fg="#A42423")
    search_button.place(x=500,y=320,width=300,height=40)
    search_button.config(command=lambda: search_function(by_attribute,med_name_entry,attribute_entry,result_text))




def Search_Medicine_Batch(menu_window,x,by_what_listbox,missing_label):
    if missing_label.winfo_ismapped():
        missing_label.place_forget()
    # get value
    search_item_index = x.get()
    by_attribute_selected = by_what_listbox.curselection()
    if by_attribute_selected==():
        # missing label
        if not missing_label.winfo_ismapped():
            missing_label.place(x=700,y=380)
    else:
        # get value
        if search_item_index == 0:
            search_item = "Medicine"
        elif search_item_index == 1:
            search_item = "Batch"
        by_attribute = by_what_listbox.get(by_attribute_selected[0])


        if search_item == "Medicine":
            open_Search_Med_window(menu_window,by_attribute)
        elif search_item == "Batch":
            open_Search_Batch_window(menu_window,by_attribute)

# create Search window
def open_Search_window(menu_window):
    search_window = Toplevel(menu_window)
    search_window.geometry("1000x800")
    search_window.title("Medicine Inventory Management System(Search)")
    search_window.config(bg="#E8E5DB")

    # title label
    title_label = Label(search_window,
                        text="Search for Medicine or Batch",font=('Arial',45,'bold'),bg="#A42423",fg="#E8E5DB")
    title_label.place(x=150,y=80)
    # attributes label
    search_what_label = Label(search_window,text="Search:",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    search_what_label.place(x=200,y=200)
    by_what_label = Label(search_window,text="Search by:",font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    by_what_label.place(x=200,y=260)
    # search what input
    x = IntVar()
    radiobuttonMed = Radiobutton(search_window,
                                 text="Medicine",
                                 font=('Arial',15,'bold'),
                                 variable=x,
                                 value=0)
    radiobuttonMed.place(x=355,y=200)
    radiobuttonBatch = Radiobutton(search_window,
                                   text="Batch",
                                   font=('Arial',15,'bold'),
                                   variable=x,
                                   value=1)
    radiobuttonBatch.place(x=500,y=200)
    # search by input
    by_what_listbox = Listbox(search_window,
                              font=('Arial',18,'bold'),
                              selectmode=SINGLE,
                              bg="#FFFFFF",
                              fg="#111111")
    by_what_listbox.place(x=355, y=260, width=280)
    by_what_listbox.config(height=by_what_listbox.size())
    def listbox_med_attributes():
        by_what_listbox.insert(END,'field')
        by_what_listbox.insert(END,'type')
        by_what_listbox.insert(END,'name')
        by_what_listbox.insert(END,'route')
        by_what_listbox.insert(END,'store temperature')
    def listbox_batch_attributes():
        by_what_listbox.insert(END,'batch number')
        by_what_listbox.insert(END,'quantity(boxes)')
        by_what_listbox.insert(END,'location')
        by_what_listbox.insert(END,'expire date')
        by_what_listbox.insert(END,'supplier')
    def show_attribute(x):
        by_what_listbox.delete(0,END)
        if x.get()==0:  # choosed medicine
            listbox_med_attributes()
        else:  # choosed batch
            listbox_batch_attributes()
    # allert label
    missing_label = Label(search_window,text="Attribute(s) missing!",font=('Arial',12),bg="#E8E5DB",fg="#FD0000")
    # submit button
    submit_button = Button(search_window,text="submit",font=('Arial',18,'bold'),fg="#A42423")
    submit_button.place(x=600,y=200,width=80,height=30)
    submit_button.config(command=lambda: show_attribute(x))
    confirm_button = Button(search_window,text="confirm",font=('Arial',18,'bold'),fg="#A42423")
    confirm_button.place(x=700,y=400,width=80,height=30)
    confirm_button.config(command=lambda:Search_Medicine_Batch(menu_window,x,by_what_listbox,missing_label))


# create Report window
def open_Report_window(menu_window):
    report_window = Toplevel(menu_window)
    report_window.geometry("1000x800")
    report_window.title("Medicine Inventory Management System(Report)")
    report_window.config(bg="#E8E5DB")

    # title label
    title_label = Label(report_window,
                        text="Inventory Report",font=('Arial',45,'bold'),bg="#A42423",fg="#E8E5DB")
    title_label.place(x=300,y=80)
    # text to display report
    report_text = Text(report_window,font=('Arial',18),state=DISABLED)
    report_text.place(x=100,y=200,width=800,height=500)
    text = "Inventory Report:\n"
    # print medicines
    medicine_names = inv.print_inventory()
    text += f"Medicines in Inventory: {medicine_names}\n"
    # print batches for each medicine
    for i in inv.medicines.values():
        batches_info = inv.print_medicine_batches(i)
        text += f"Batches for Medicine {i.name}: {batches_info}\n"
    # display report
    report_text.config(state="normal")  # start to write in
    report_text.delete(1.0, END)         # clear old content
    report_text.insert(1.0, text)            # write in
    report_text.config(state="disabled")  # write in finished




# create the menu window to choose action
def open_menu_window():  # this window is opened in welcom window
    menu_window = Tk()
    menu_window.geometry("1000x800")
    menu_window.title("Medicine Inventory Management System(Menu)")
    menu_window.config(bg="#E8E5DB")

    # title label
    title_label = Label(menu_window,
                        text="Click And Choose One Action",font=('Arial',45,'bold'),bg="#A42423",fg="#E8E5DB")
    title_label.place(x=180,y=80)

    # button for different action
    CreateMedicine = Button(menu_window, text="Create a New Medicine", font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    CreateBatch = Button(menu_window, text="Store a New Batch", font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    RemoveMedicine = Button(menu_window, text="Remove a Medicine", font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    GetMedicine = Button(menu_window, text="Get an Amount of Medicine", font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    Search = Button(menu_window, text="Search for Medicine or Batch", font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    Report = Button(menu_window, text="Generate Inventory Report", font=('Arial',20),bg="#E8E5DB",fg="#A42423")
    buttons = [CreateMedicine,CreateBatch, RemoveMedicine, GetMedicine, Search, Report]

    # display buttons
    button_top = 200
    for i in buttons:
        i.place(x=300,y=button_top,width=400,height=50)
        button_top += 80

    # click button to go to next window
    CreateMedicine.config(command=lambda: open_Create_Medicine_window(menu_window))
    CreateBatch.config(command=lambda: open_Create_Batch_window(menu_window))
    RemoveMedicine.config(command=lambda: open_Remove_Medicine_window(menu_window))
    GetMedicine.config(command=lambda: open_Get_Medicine_window(menu_window))
    Search.config(command=lambda: open_Search_window(menu_window))
    Report.config(command=lambda: open_Report_window(menu_window))

    # save on close
    menu_window.protocol("WM_DELETE_WINDOW", lambda: on_menu_close(menu_window, med_sheet, batch_sheet))

    menu_window.mainloop()

def on_menu_close(menu_window,med_sheet, batch_sheet):
    print("DEBUG: to_excel")
    fm.save_file(med_sheet, batch_sheet)  # to excel
    menu_window.destroy()
    



def open_welcome_window():
    # create welcome window to ask for password
    welcom_window = Tk()
    welcom_window.geometry("1000x800")
    welcom_window.title("Medicine Inventory Management System")
    welcom_window.config(bg="#E8E5DB")



    # password page
    # init text
    passwordlabel = Label(welcom_window,
                        text="Welcome to Medicine Inventory Management System!\nPlease enter password:",font=('Arial',20))
    passwordlabel.config(fg="#A42423")
    passwordlabel.place(x=200,y=200)
    # init password entry
    passwordentry = Entry(welcom_window)
    passwordentry.config(font=('Arial',20),show='*')
    passwordentry.config(fg="#A42423")
    passwordentry.place(x=200,y=300)
    # init wrong password label
    wrong_pw = Label(welcom_window,text="Wrong password, please try again.",font=('Arial',10))
    wrong_pw.config(fg="#A42423")
    def show_wrong_pw():
        if not wrong_pw.winfo_ismapped():
            wrong_pw.place(x=200,y=280)
    # submit and check password
    def submit_password(event,welcome_window=welcom_window):
        password = passwordentry.get()
        status = formulas.welcome(password)
        if status:
            welcome_window.destroy()
            open_menu_window()
        else:
            show_wrong_pw()
    passwordentry.bind("<Return>", submit_password)

    welcom_window.mainloop()

def main():
    global med_sheet, batch_sheet
    med_sheet, batch_sheet = fm.open_file()
    open_welcome_window()  # this window open menu window

if __name__ ==  "__main__":
    main()
    
