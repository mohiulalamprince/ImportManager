import os
import csv

class ImportManager():
    before_data_file_path = None
    after_data_file_path = None
    before_data = None
    after_data = None
    id_by_data_before = None
    id_by_data_after = None

    def __init__(self, before_data_file_path, after_data_file_path):
        self.before_data_file_path = before_data_file_path
        self.after_data_file_path = after_data_file_path

    def load_file(self, path):
        ret_list = []
        counter = 0
        with open(path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                ret_list.append((dict(row)))
        return ret_list

    def get_ids(self, data_list):
        return [x['id'] for x in data_list]
    
    def mapped_id_by_data(self, datas):
        return {data['id'] : data for data in datas}

    def is_file_exists(self, path):
        if os.path.exists(path):
            print ("Data file Exist => PATH=" + path)
        else:
            print ("Data file not found => PATH=", path)
            exit(0)

    def load(self):
        self.is_file_exists(self.before_data_file_path)
        self.is_file_exists(self.after_data_file_path)

        #load the data
        self.before_data = self.load_file(self.before_data_file_path)
        self.after_data = self.load_file(self.after_data_file_path)
        
        #mapping product data by id to check / retrieve the product very quickly
        self.id_by_data_before = self.mapped_id_by_data(self.before_data)
        self.id_by_data_after = self.mapped_id_by_data(self.after_data)

    def find_created_ids(self):
        before_ids = list(set(self.get_ids(self.before_data)))
        after_ids = list(set(self.get_ids(self.after_data)))

        mapped_before_ids = {x : True for x in before_ids}

        return [id for id in after_ids if mapped_before_ids.get(id) is not True]

    def find_deleted_ids(self):
        before_ids = list(set(self.get_ids(self.before_data)))
        after_ids = list(set(self.get_ids(self.after_data)))

        mapped_after_ids = {id : True for id in after_ids}

        return [id for id in before_ids if mapped_after_ids.get(id) is not True]
    
    def create_operation(self):
        created_ids = self.find_created_ids()
        created_data = [self.id_by_data_after.get(id) for id in created_ids]
        return created_data

    def delete_operation(self):
        deleted_ids = self.find_deleted_ids()
        return deleted_ids

    def update_operation(self):
        created_ids = set(self.find_created_ids())
        deleted_ids = set(self.find_deleted_ids())

        before_ids = set(self.get_ids(self.before_data))
        after_ids = set(self.get_ids(self.after_data))

        updatedOrUnchanged_before_ids = before_ids - deleted_ids
        updatedOrUnchanged_after_ids = after_ids - created_ids

        id_by_hash_data_before = {id : self.get_hash_value(self.id_by_data_before.get(id)) \
                                    for id in updatedOrUnchanged_before_ids}
        
        unchanged_data = set([ id \
                            for id in updatedOrUnchanged_after_ids \
                                if id_by_hash_data_before.get(id) == self.get_hash_value(self.id_by_data_after.get(id))])
        updated_data_ids = updatedOrUnchanged_after_ids - unchanged_data
        updated_data = [self.id_by_data_after.get(id) for id in updated_data_ids]

        return updated_data

    def get_hash_value(self, data):
        hash_value = ""
        try:
            data_str= "" + str(data['id']) \
                    + str(data['title']) \
                    + str(data['description']) \
                    + str(data['product_category']) \
                    + str(data['link'])\
                    + str(data['price']) \
                    + str(data['brand']) \
                    + str(data['color']) \
                    + str(data['gtin']) \
                    + str(data['image_link']) \
                    + str(data['item_group_id']) \
                    + str(data['additional_imagelinks']) \
                    + str(data['sale_price']) \
                    + str(data['shipping.country']) \
                    + str(data['shipping.price']) \
                    + str(data['size']) \
                    + str(data['stock'])
            hash_value = hash(data_str)
        except Exception:
            print ("Parsing Error in get_hash_value function")
        return hash_value

def main(path_to_before_csv, path_to_after_csv):
    import_manager = ImportManager(path_to_before_csv, path_to_after_csv)
    import_manager.load()
    import_manager.delete_operation()
    import_manager.create_operation()
    import_manager.update_operation()

if __name__ == '__main__':
    BASE_PATH = "/Users/prince/Downloads/csv/"
    main(BASE_PATH + "product_inventory_before.csv", BASE_PATH + "product_inventory_after.csv")
