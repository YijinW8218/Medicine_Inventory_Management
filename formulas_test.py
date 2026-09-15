import unittest
import formulas as du3

class Test(unittest.TestCase):

    def setUp(self):
        # reset inventory before each test
        self.inv = du3.InventorySystem()
        self.med = du3.Medicine(self.inv,
                                'ANAESTHETICS, PREOPERATIVE MEDICINES AND MEDICAL GASES',
                                'General anaesthetics and oxygen',
                                'isoflurane',
                                'Inhalation',
                                'Room temperature')

    def test_medicine_creation(self):
        """Test that creat Medicine object correctly."""
        self.assertIn('isoflurane',self.inv.medicines.keys())
        self.assertEqual(self.med.name, 'isoflurane')
        self.assertEqual(self.med.route, 'Inhalation')
        self.assertEqual(self.med.field, 'ANAESTHETICS, PREOPERATIVE MEDICINES AND MEDICAL GASES')
        self.assertEqual(self.med.temp, 'Room temperature')

    def test_inventory_add(self):
        """Test that medicine is added to inventory when created."""
        self.assertIn(self.med.name, self.inv.medicines.keys())
        self.assertIn(self.med, self.inv.medicines.values())
        self.assertEqual(len(self.inv.medicines), 1)

    def test_batch_creation(self):
        """Test that creat Batch object correctly."""
        # create a batch
        batch = du3.Batch(self.med, '001', 100, 'first floor', '11/23/2025', 'Starfish')
        # test the batch
        self.assertEqual(batch.batch_number, '001')
        self.assertEqual(batch.quantity, 100)
        self.assertEqual(batch.location, 'first floor')
        self.assertEqual(batch.exp_date, '11/23/2025')
        self.assertEqual(batch.supplier, 'Starfish')
        # test link to parent object
        self.assertIs(batch.parent, self.med)
        # test if batch is added to medicine when created
        self.assertIn((batch, '11/23/2025'), self.med.batches.queue)
        self.assertEqual(len(self.med.batches.queue), 1)

    def test_Med_str(self):
        """Test that Medicine str override is correct."""
        self.assertEqual(str(self.med), 'isoflurane')

    def test_Batch_str(self):
        """"Test that Batch str override is correct"""
        batch = du3.Batch(self.med, '001', 100, 'first floor', '11/23/2025', 'Starfish')
        self.assertEqual(str(batch),"isoflurane(001)")


    def test_qu_str(self):
        """Test that PriorityQueue str override is correct."""
        batch = du3.Batch(self.med, '001', 100, 'first floor', '11/23/2025', 'Starfish')
        self.assertEqual(str(self.med.batches),str([(batch.batch_number,batch.exp_date,batch.quantity)]))

    def test_highest_priority(self):
        """Test that this function find the highest priority correctly"""
        batch1 = du3.Batch(self.med, '001', 100, 'first floor', '11/23/2025', 'Starfish')
        batch2 = du3.Batch(self.med, '002', 50, 'first floor', '10/10/2025', 'Starfish')
        batch3 = du3.Batch(self.med, '003', 100, 'first floor', '1/15/2026', 'Starfish')
        hi1 = self.med.batches.highest_priority()
        self.assertEqual(hi1,batch2)
        self.med.batches.queue.remove((hi1,hi1.exp_date))
        hi2 = self.med.batches.highest_priority()
        self.assertEqual(hi2,batch1)
        self.med.batches.queue.remove((hi2,hi2.exp_date))
        hi3 = self.med.batches.highest_priority()
        self.assertEqual(hi3,batch3)
        self.med.batches.queue.remove((hi3,hi3.exp_date))
        self.assertEqual(len(self.med.batches.queue),0)

    def test_unqueue(self):
        """Test that unqueue remove highest priority item from queue correctly"""
        batch1 = du3.Batch(self.med, '001', 100, 'first floor', '11/23/2025', 'Starfish')
        batch2 = du3.Batch(self.med, '002', 50, 'first floor', '10/10/2025', 'Starfish')
        batch3 = du3.Batch(self.med, '003', 100, 'first floor', '1/15/2026', 'Starfish')
        self.med.batches.unqueue()
        hi_new = self.med.batches.highest_priority()
        self.assertEqual(hi_new,batch1)

    def test_get_med(self):
        """Test that get medicine from one or more bratch correctly."""
        batch1 = du3.Batch(self.med, '001', 100, 'first floor', '11/23/2025', 'Starfish')
        batch2 = du3.Batch(self.med, '002', 50, 'first floor', '10/10/2025', 'Starfish')
        batch3 = du3.Batch(self.med, '003', 100, 'first floor', '1/15/2026', 'Starfish')
        self.med.batches.get_med(70)
        self.assertEqual(str(self.med.batches),str([('001','11/23/2025',80),('003','1/15/2026',100)]))
        
    # unit tests for program out-class function
    def test_relative_date(self):
        """Test that this function caculate date correctly."""
        days = self.inv.relative_date('11/22/2025')
        self.assertEqual(days, 2150)

    def test_new(self):
        """Test that creat new medicine and batches correctly"""
        new_medicine = self.inv.new_med("ANAESTHETICS, PREOPERATIVE MEDICINES AND MEDICAL GASES",
                                   "Local anaesthetics",
                                   "bupivacaine",
                                   "Injection",
                                   "cold")
        new_batch = self.inv.new_batch(new_medicine,'001',100,'basement','5/5/2027','Starfish')
        self.assertEqual(str(new_batch), "bupivacaine(001)")

    def test_remove(self):
        """Test that remove medicine and batch from inventory correctly"""
        new_medicine = self.inv.new_med("ANAESTHETICS, PREOPERATIVE MEDICINES AND MEDICAL GASES",
                                   "Local anaesthetics",
                                   "bupivacaine",
                                   "Injection",
                                   "cold")
        batch1 = du3.Batch(self.med, '001', 100, 'first floor', '11/23/2025', 'Starfish')
        batch2 = du3.Batch(self.med, '002', 50, 'first floor', '10/10/2025', 'Starfish')
        self.inv.remove_med(new_medicine.name)
        self.assertIn(self.med.name,self.inv.medicines.keys())
        self.inv.remove_batch(self.med,'002')
        self.assertEqual(str(self.med.batches),str([('001','11/23/2025',100)]))

    def test_get_medicine(self):
        """Test that get medicine from one or more bratch correctly."""
        batch1 = du3.Batch(self.med, '001', 100, 'first floor', '11/23/2025', 'Starfish')
        batch2 = du3.Batch(self.med, '002', 50, 'first floor', '10/10/2025', 'Starfish')
        batch3 = du3.Batch(self.med, '003', 100, 'first floor', '1/15/2026', 'Starfish')
        self.inv.get_medicine(self.med, 70)
        self.assertEqual(str(self.med.batches),str([('001','11/23/2025',80),('003','1/15/2026',100)]))

    def test_search_medicine(self):
        """Test that search medicine object from inventory(a list)"""
        # test search by field
        result = self.inv.search_medicine("field","ANAESTHETICS, PREOPERATIVE MEDICINES AND MEDICAL GASES")
        self.assertEqual([self.med],result)
        # test search by type
        result = self.inv.search_medicine("type","General anaesthetics and oxygen")
        self.assertEqual([self.med],result)
        # test search by name
        result = self.inv.search_medicine("name","isoflurane")
        self.assertEqual([self.med],result)
        # test search by route
        result = self.inv.search_medicine("route","Inhalation")
        self.assertEqual([self.med],result)
        # test search by temp
        result = self.inv.search_medicine("temp","Room temperature")
        self.assertEqual([self.med],result)
        

    def test_search_batch(self):
        """Test that search batch object from medicine.batches(a PriorityQueue)"""
        batch1 = du3.Batch(self.med, '001', 100, 'first floor', '11/23/2025', 'Starfish')
        batch2 = du3.Batch(self.med, '002', 50, 'first floor', '10/10/2025', 'Starfish')
        # test search by batch number
        result = self.inv.search_batch(self.med,"batch_number","002")
        self.assertEqual([batch2],result)
        # test search by quantity
        result = self.inv.search_batch(self.med,"quantity",100)
        self.assertEqual([batch1],result)
        # test search by location
        result = self.inv.search_batch(self.med,"location","first floor")
        self.assertEqual([batch1,batch2],result)
        # test search by exp_date
        result = self.inv.search_batch(self.med,"exp_date","11/23/2025")
        self.assertEqual([batch1],result)
        # test search by supplier
        result = self.inv.search_batch(self.med,"supplier","Starfish")
        self.assertEqual([batch1,batch2],result)

    def test_edit_batch(self):
        """Test that edit batch object attribute correctly"""
        batch1 = du3.Batch(self.med, '001', 100, 'first floor', '11/23/2025', 'Starfish')
        self.inv.edit_batch(batch1,"quantity",150)
        self.assertEqual(batch1.quantity,150)

    def test_edit_medicine(self):
        """Test that edit medicine object attribute correctly"""
        self.inv.edit_medicine(self.med,"temp","cold")
        self.assertEqual(self.med.temp,"cold")
        self.inv.edit_medicine(self.med,"temp","Room temperature")
    
    def test_print_inventory(self):
        """Test that print inventory function works correctly"""
        new_medicine = self.inv.new_med("ANAESTHETICS, PREOPERATIVE MEDICINES AND MEDICAL GASES",
                                   "Local anaesthetics",
                                   "bupivacaine",
                                   "Injection",
                                   "cold")
        inv_str = self.inv.print_inventory()
        self.assertEqual(inv_str,"\n\tisoflurane\n\tbupivacaine")
    
    def test_print_batches(self):
        """Test that print batches function works correctly"""
        batch1 = du3.Batch(self.med, '001', 100, 'first floor', '11/23/2025', 'Starfish')
        batch2 = du3.Batch(self.med, '002', 50, 'first floor', '10/10/2025', 'Starfish')
        bat_str = self.inv.print_medicine_batches(self.med)
        self.assertEqual(bat_str,"\n\tBatch Number: 002, Quantity: 50, Location: first floor, Expiry Date: 10/10/2025, Supplier: Starfish\n\tBatch Number: 001, Quantity: 100, Location: first floor, Expiry Date: 11/23/2025, Supplier: Starfish")

        


if __name__ == "__main__":
    unittest.main()
        


        
        
