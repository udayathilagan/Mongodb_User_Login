import pymongo

# MongoDB connection details

mongo_client = pymongo.MongoClient("mongodb+srv://<user>:<passcode>@cluster0.8tbow.mongodb.net/?retryWrites=true&w=majority")#replace your string
#Create a new db and collection else use your existing collection 
db = mongo_client["user"]
users_collection = db["userdata"]

def validate_credentials(username, password):
    user = users_collection.find_one({"username": username, "password": password})
    return user is not None

if __name__ == "__main__":
    while True:
        input_username = input("Enter your username: ")
        input_password = input("Enter your password: ")

        if validate_credentials(input_username, input_password):
            print("Login successful!")
            break
        else:
            print("Invalid credentials. Please try again.")
