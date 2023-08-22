import re
import pymongo
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# MongoDB connection details
mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017/app")#replace with your Mongodb connection details
db = mongo_client["user_db"]
users_collection = db["users"]

def is_valid_email(email):
    # Basic email validation using regular expression
    pattern = r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
    return re.match(pattern, email)

def send_otp_email(email, otp_code):
    sender_email = "human@gmail.com"  # Replace with your actual email
    sender_password = "youknowwhattodo"  # Replace with your actual email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "OTP Verification"

    message = f"Your OTP code is: {otp_code}"
    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

def generate_otp():
    return str(random.randint(1000, 9999))

def register_user(username, email, password):
    if users_collection.find_one({"username": username}):
        print("Username already taken")
        return True
    if users_collection.find_one({"email": email}):
        print("This mail id  already registered")
        return True
    if not is_valid_email(email):
        print("Invalid email format")
        return False
    
    otp = generate_otp()
    if send_otp_email(email, otp):
        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "otp": otp,
            "status":False
        }
        print("\nOTP sent for verification")
        for i in range(0,4):
            otp_in = input("\nEnter the OTP: ")
            if otp_in==otp:
                users_collection.insert_one(user_data)
                print("verification successful")
                return True
            else :
                print("\n you have entered a wrong OTP")
    else:
        print("Error sending OTP email")
        return False

if __name__ == "__main__":
    print("Account Registration")
    username = input("Enter a username: ")
    email = input("Enter your email: ")
    password = input("Enter a password: ")
    result = register_user(username, email, password)
    if result:
        print("You can call your main function here")
