
from phase4 import connectDB
from dummy_data import dummy_data
from pymongo import errors
from bson import ObjectId

def createCollection(db, collection_name):
    try:
        # If the collection doesn't exist, create it
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created.")
        elif collection_name in db.list_collection_names():
            print("Collection already exists")
    except Exception as e:
        print("An error occured: ", e)


def insert_into_collection(db, collection_name, data):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Insert the data into the collection
        result = collection.insert_one(data)

        # Print the inserted document ID
        print("Insertion successfully completed")
        print(f"Inserted document ID: {result.inserted_id}")

    except Exception as e:
        print(f"An error occurred: {e}")


def read_all_data(collection):
    try:
        # Access the specified collection
        # Use the find method to retrieve all documents
        result = collection.find()

        # Iterate through the documents and print them
        for document in result:
            print(document)

    except Exception as e:
        print(f"An error occurred: {e}")
def pick_data_fields(collection):
    try:
        field_names = collection.find_one().keys()
        print("All Data Fields:")
        for i, field in enumerate(field_names, start=1):
            print(i, field)
        
        picked_num=int(input("pick data field: "))

        return list(field_names)[picked_num-1]
    except Exception as e:
        print(f"An error occurred: {e}")


def find_orders_containing_item(collection,field_name, item_name):
    try:
        # Define the query to find orders containing the specified item
        query = {str(field_name):str(item_name)}

        # Use the find method to retrieve matching documents
        cursor = collection.find(query)

        # Convert your cursor to a list to freely operate over it
        result = list(cursor)

        # Print the matching documents
        for document in result:
            print(document)

        # Return the whole result list
        return result

    except Exception as e:
        print(f"An error occurred: {e}")


def delete_record_by_id(db, collection_name, record_id):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Define the query to find the document by its ID
        query = {"_id": record_id}

        # Use the delete_one method to delete the document
        result = collection.delete_one(query)

        # Check if the deletion was successful
        if result.deleted_count == 1:
            print(f"Successfully deleted record with ID {record_id}")
        else:
            print(f"No record found with ID {record_id}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")


def update_order_list_by_id(db, collection_name, record_id, new_order_list):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Define the query to find the document by its ID
        query = {"_id": record_id}

        # Use the update_one method to update the specific field (order_list)
        result = collection.update_one(query, {"$set": {"order_items": new_order_list}})

        # Check if the update was successful
        if result.matched_count == 1:
            print(f"Successfully updated order_list for record with ID {record_id}")
        else:
            print(f"No record found with ID {record_id}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")
def expect_field_names(collection):
    print("please enter the data fields")
    try:
        sample_document = collection.find_one()

        if sample_document:
            fields = fields = sample_document.keys()
            new_field_values = {}  # Dictionary to store updated values for each field

            for field in fields:
                new_field_val = input(f"{field}: ")
                new_field_values[field] = new_field_val

    #  Create new document
        collection.insert_one(new_field_values)

        print("The new document was successfully inserted!")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")
def expect_field_names_id(collection,document_id):
    print("please enter the data fields")
    try:
        obj_id = ObjectId(document_id)
        # Retrieve a sample document to get its keys (field names)
        sample_document = collection.find_one({"_id": obj_id})
        
        if sample_document:
            fields = sample_document.keys()

            existing_document = collection.find_one({"_id": obj_id})

            if existing_document:
                new_field_values = {}  # Dictionary to store updated values for each field

                for field in fields:
                    if field!="_id":
                        new_field_val = input(f"{field} (current value: {existing_document[field]}): ")
                        new_field_values[field] = new_field_val

                # Update the specific document with new values
                update_query = {"$set": new_field_values}
                collection.update_one({"_id": obj_id}, update_query)

                print("The document was successfully updated!")
            else:
                print(f"No document found with ID: {document_id}")
        else:
            print(f"No sample document found for ID: {document_id}")

    except Exception as e:
        print(f"An error occurred: {e}")

def delete_record_by_item(collection,picked_field,item):
    try:

        # Define the query to find the document by its ID
        query = {picked_field : item}

        # Use the delete_one method to delete the document
        result = collection.delete_many(query)

        # Check if the deletion was successful
        if result.deleted_count >= 1:
            print(
                f"Successfully deleted {result.deleted_count} record that contains {item}"
            )
        else:
            print(f"No record found with {item}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # First create a connection
    db = connectDB()
    usr_id=input("Welcome to Review Portal!\nPlease enter your user id:")

    choice=input("Please pick the option that you want to proceed.\n1- Create a collection.\n2- Read all data in a collection\n3- Read some part of the data while filtering.\n4- Insert data.\n5- Delete data.\n6- Update data.\n")
    if choice == "1":
        collection_name = input("Enter the collection name: ")
        db.create_collection(collection_name)
        print(f"Collection '{collection_name}' created successfully.")


    # # Insert some dummy data into your collection
    #for item in dummy_data:
    #    insert_into_collection(db, "feedback", item)

    elif choice == "2":
        available_collections = db.list_collection_names()
        print("Available collections:\n")
        a=1
        for collection_name in available_collections:
            print(a,"-",collection_name)
            a=a+1

        collection_name = input("Enter the collection name you want to enter: ")
        collection = db[collection_name]
        read_all_data(collection)
        

    elif choice == "3":
        available_collections = db.list_collection_names()
        print("Available collections:\n")
        b=1
        for collection_name in available_collections:
            print(b,"-",collection_name)
            b=b+1
        collection_name = input("Enter the collection name you want to enter: ")
        collection = db[collection_name]
        picked_field=pick_data_fields(collection)
        query1=input("Enter the name you want to match with picked field: ")
        found_doc=find_orders_containing_item(collection,picked_field,query1)
        
    # # Delete the first record which has a pizza in its order list
    elif choice == "5":
        available_collections = db.list_collection_names()
        print("Available collections:\n")
        c=1
        for collection_name in available_collections:
            print(c,"-",collection_name)
            c=c+1
        collection_name = input("Enter the collection name you want to query: ")
        collection = db[collection_name]
        picked_field=pick_data_fields(collection)
        query1=input("Enter the name you want to match with picked field to delete: ")
        found_doc=delete_record_by_item(collection,picked_field,query1)
    ##insert data    
    elif choice == "4":
        available_collections = db.list_collection_names()
        print("Available collections:\n")
        d=1
        for collection_name in available_collections:
            print(d,"-",collection_name)
            d=d+1
        collection_name = input("Enter the collection name you want to insert data: ")
        collection = db[collection_name]
        expect_field_names(collection)
    elif choice == "6":
        available_collections = db.list_collection_names()
        print("Available collections:\n")
        d=1
        for collection_name in available_collections:
            print(d,"-",collection_name)
            d=d+1
        collection_name = input("Enter the collection name you want to update: ")
        collection = db[collection_name]

        document_id = input("Enter the ID of the document to update: ")
            
        expect_field_names_id(collection,document_id)

    # # Update the next item
    # id_to_update = found_documents[0]["_id"]
    # new_order_list = (
    #     [
    #         {"item_name": "Hamburger", "quantity": 1},
    #         {"item_name": "Fries", "quantity": 1},
    #         {"item_name": "Iced Tea", "quantity": 2},
    #     ],
    # )
    # update_order_list_by_id(db, "orders", id_to_update, new_order_list)
        







