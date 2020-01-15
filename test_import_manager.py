import unittest
import json
from import_manager import ImportManager

class TestImportManager(unittest.TestCase):
    import_manager = None
    partial_sample_data = None
    created_expected_output = None
    updated_expected_output = None
    
    ONE = None
    FOUR = None

    def setUp(self):
        self.import_manager = ImportManager("", "")
        self.partial_sample_data = {'title': 'Knot So Bad boys T-shirt World Music', 'description': "Very tough shiny boys winter coat in shades of brown and anthracite Tumble 'n Dry. The hood is lined yellow ocher. On the brown zipper is a metal clasp with an additional snap closure about it. The beautiful finished flap pockets have metal buttons and the inclined bag top is a yellow label on the zipper. At the bottom and on the sleeves are brown and gray elastic cuffs. The nice soft lining is black and there is a handy inside pocket. Washable at 30 degrees. Jacket: 100% polyester / 100% cotton, lining and paddin 100% polyester, lined hood and sleeves: 100% nylon. Brand: Tumble 'n Dry, model: Thermalito, color: Major Brown.", 'product_category': 'boys/t-shirts', 'link': 'http://example.channable.com/boys/t-shirts-long-sleeve/knot-so-bad/knot-so-bad-boys-t-shirt-world-music-11098.html', 'brand': 'Knot so bad', 'color': 'grey', 'gtin': '8773833664651', 'image_link': 'http://www.codedsolutions.nl/demo/k-008812-a-f.jpg', 'item_group_id': '008812-05', 'additional_imagelinks': '', 'sale_price': '', 'shipping.country': 'UK', 'shipping.price': '2.95 GBP', 'size': '134', 'stock': '12'}
        before_data = [
                {"id" : 1, "price" : 10}, 
                {"id" : 2, "price" : 20}, 
                {"id": 3, "price" : 5}, 
                {"id" : 4, "price" : 60}]
        after_data = [
                {"id" : 1, "price" : 10}, 
                {"id" : 2, "price" : 20}, 
                {'id' : 3, "price" : 40}, 
                {"id" : 6, "price" : 70}]

        self.import_manager.before_data = [{ **self.partial_sample_data, **item} for item in before_data]
        self.import_manager.after_data = [{ **self.partial_sample_data, **item} for item in after_data]
       
        self.import_manager.id_by_data_before = self.import_manager.mapped_id_by_data(
                self.import_manager.before_data)
        self.import_manager.id_by_data_after = self.import_manager.mapped_id_by_data(
                self.import_manager.after_data)
        
        self.created_expected_output = {"id" : 6, "price" : 70}
        self.created_expected_output.update(self.partial_sample_data)
        
        self.updated_expected_output = {"id" : 3, "price": 40}
        self.updated_expected_output.update(self.partial_sample_data)

        self.ONE = 1
        self.FOUR = 4
    
    def test_find_created_ids(self):
        created_ids = self.import_manager.find_created_ids()
        self.assertEqual(self.ONE, len(created_ids))

    def test_find_deleted_ids(self):
        deleted_ids = self.import_manager.find_deleted_ids()
        self.assertTrue(self.FOUR in deleted_ids)

    def test_create_operation(self):
        
        created_data = self.import_manager.create_operation()

        self.assertEqual([self.created_expected_output], created_data)
    
    def test_delete_operation(self):
        deleted_ids = self.import_manager.delete_operation()

        self.assertEqual([self.FOUR], deleted_ids)

    def test_update_operation(self):

        updated_data = self.import_manager.update_operation()
        
        self.assertEqual(self.ONE, len(updated_data))
        self.assertEqual([self.updated_expected_output], updated_data)

if __name__ == '__main__':
    unittest.main()
