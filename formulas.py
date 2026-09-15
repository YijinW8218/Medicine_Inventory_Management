"""core classes and methods on the backend"""
# I use WHO Model List of Essential Medicines - 24th List(2025) as a data source. 
# Highest title is called 'field', second title is called 'type', and they are assign to be the attribute of class. 
import copy
class PriorityQueue:  # a queue to store bataches into medicine
    def __init__(self,inventory):
        self.inventory = inventory
        self.queue = []

    def __str__(self):
        return str([(item.batch_number, priority, item.quantity) 
                 for item, priority in self.queue])

    def is_empty(self):
        return len(self.queue) == 0
    
    def insert_batch(self, batch, exp_date):
        self.queue.append((batch, exp_date))

    def highest_priority(self):
        if self.is_empty():
            raise IndexError("No batches for this medicine in the inventory now.")
        else:
            # closer date has higher priority
            max_index = 0
            max_date = self.inventory.relative_date(self.queue[0][1])
            for i in range(1,len(self.queue)):
                current_date = self.inventory.relative_date(self.queue[i][1])
                if current_date < max_date:
                    max_index = i
                    max_date = current_date
            return self.queue[max_index][0]
        
    def unqueue(self):
        # remove the highest priority object
        ob = self.highest_priority()
        self.queue.remove((ob,ob.exp_date))
        
    def get_med(self, amount):
        # take an amount of medicine from one or more batches
        while amount > 0:
            current_batch = self.highest_priority()
            current_amount = current_batch.quantity
            if current_amount > amount:
                current_batch.quantity = current_batch.quantity - amount
                break
            elif current_amount == amount:
                self.unqueue()
                break
            else:
                amount = amount - current_amount
                self.unqueue()
   

class StorableObject: 
    """Base class for all elements in the inventory system.""" 
    def __init__(self, parent_obj=None): 
        # link to the containing object 
        self.parent = parent_obj 
        
class Medicine(StorableObject): 
    def __init__(self,inventory,field, type, name, route, temp): 
        super().__init__() # med_obj will be roots, so parent is None
        self.inventory = inventory 
        self.field = field 
        self.type = type 
        self.name = name 
        self.route = route # how to take the medicine 
        self.temp = temp 
        inventory.medicines[self.name] = self # add the medicine to inventory when created 
        self.batches = PriorityQueue(self.inventory) # list to store batches of the medicine 
        
    def __str__(self): 
        return self.name 
    
        
class Batch(StorableObject): 
    def __init__(self, med_obj, batch_number, quantity, location, exp_date, supplier): 
        super().__init__(med_obj) # link to the medicine object 
        self.batch_number = batch_number 
        self.quantity = quantity 
        self.location = location 
        self.exp_date = exp_date 
        self.supplier = supplier 
        med_obj.batches.insert_batch(self, exp_date)

    def __str__(self):
        return f"{self.parent.name}({self.batch_number})"






# Class to store all datas and functions
class InventorySystem:
    def __init__(self):
        self.medicines = {} # dictionary to store all medicines



    def relative_date(self,exp_date):
        """calculate how many days from 1/1/2020"""
        days = 0
        # get datas
        sp = exp_date.split('/')
        month, day, year = int(sp[0]), int(sp[1]), int(sp[2])
        # calculate years
        if year > 2020:
            days += (year - 2020) * 365
        # calculate monthsr
        day_difference = [31,28,31,30,31,30,31,31,30,31,30]
        months = month - 1
        for i in range(months):
            days += day_difference[i]
        # calculate days
        days = days + day - 1
        return days

    ## create new obj function
    ### create new medicine
    def new_med(self, field, type, name, route, temp):
        new_medicine = Medicine(self,field, type, name, route, temp)
        return new_medicine
    ### create new batch
    def new_batch(self,med_obj, batch_number, quantity, location, exp_date, supplier):
        print("DEBUG: med_obj id:", id(med_obj))
        print("DEBUG: med_obj.batches id:", id(med_obj.batches))
        print("DEBUG: queue before:", med_obj.batches.queue)
        new_batch = Batch(med_obj, batch_number, quantity, location, exp_date, supplier)
        print("DEBUG: queue after:", med_obj.batches.queue)
        return new_batch
    ## remove
    ### remove medicine from inventory
    def remove_med(self,med_name):
        del self.medicines[med_name]
    ### remove batch from medicine
    def remove_batch(self,med_obj, batch_number):
        for i in self.search_batch(med_obj, "batch_number", batch_number):
            batch_obj = i  # batch number is unique
        med_obj.batches.queue.remove((batch_obj, batch_obj.exp_date))
    ### take out medicine from one for more batches
    def get_medicine(self,med_obj, amount):
        med_obj.batches.get_med(amount)



    # search
    ## search Medicine obj
    def search_medicine(self,attribute_name,attribute_val):
        """input:str,str
        resturn:list"""
        result = []
        if attribute_name == "field":
            for med in self.medicines.values():
                if med.field == attribute_val:
                    result.append(med)
        elif attribute_name == "type":
            for med in self.medicines.values():
                if med.type == attribute_val:
                    result.append(med)
        elif attribute_name == "name":
            for med_name in self.medicines.keys():
                if med_name == attribute_val:
                    result.append(self.medicines[med_name])
        elif attribute_name == "route":
            for med in self.medicines.values():
                if med.route == attribute_val:
                    result.append(med)
        elif attribute_name == "temp":
            for med in self.medicines.values():
                if med.temp == attribute_val:
                    result.append(med)
        return result
    ## search Batch obj
    def search_batch(self,med_obj,attribute_name,attribute_val):
        """input:Medicine obj,str,str
        resturn:list"""
        result = []
        for batch, _ in med_obj.batches.queue:
            if attribute_name == "batch_number":
                if batch.batch_number == attribute_val:
                    result.append(batch)
            elif attribute_name == "quantity":
                if batch.quantity == attribute_val:
                    result.append(batch)
            elif attribute_name == "location":
                if batch.location == attribute_val:
                    result.append(batch)
            elif attribute_name == "exp_date":
                if batch.exp_date == attribute_val:
                    result.append(batch)
            elif attribute_name == "supplier":
                if batch.supplier == attribute_val:
                    result.append(batch)
        return result

    ## edit
    ### edit batch's attribute
    def edit_batch(self,batch_obj,attribute_name,new_value):
        """to edit normal attribute. notice: parent link can't be edited. such mistake need to delete the old batch and add new batch to new parent
        return:None"""
        if attribute_name == "batch_number":
            batch_obj.batch_number = new_value
        elif attribute_name == "quantity":
            batch_obj.quantity = new_value
        elif attribute_name == "location":
            batch_obj.location = new_value
        elif attribute_name == "exp_date":
            batch_obj.exp_date = new_value
        elif attribute_name == "supplier":
            batch_obj.supplier = new_value

    def edit_medicine(self,med_obj,attribute_name,new_value):
        """return:None"""
        if attribute_name == "field":
            med_obj.field = new_value
        elif attribute_name == "type":
            med_obj.type = new_value
        elif attribute_name == "name":
            med_obj.name = new_value
        elif attribute_name == "route":
            med_obj.route = new_value
        elif attribute_name == "temp":
            med_obj.temp = new_value

    ## inventory output
    def print_inventory(self,):
        """all medicines_name
        return:str"""
        s = ""
        if len(self.medicines) == 1:
            key = next(iter(self.medicines))
            s = f"{key}"
        else:
            for med in self.medicines.values():
                s += f"\n\t{med.name}"
        return s

    def print_medicine_batches(self,med_obj):
        """all batches of one medicine
        return:str(in order)"""
        s = ""
        copy_obj = copy.deepcopy(med_obj)
        for i in range(len(copy_obj.batches.queue)):
            current_batch = copy_obj.batches.highest_priority()
            s += f"\n\tBatch Number: {current_batch.batch_number}, Quantity: {current_batch.quantity}, Location: {current_batch.location}, Expiry Date: {current_batch.exp_date}, Supplier: {current_batch.supplier}"
            self.remove_batch(copy_obj, current_batch.batch_number)
        return s

# inventory = InventorySystem()

## menu output
def welcome(password):
    if password == '123456':
        return True
    
