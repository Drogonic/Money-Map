from pymongo import MongoClient


client = MongoClient("mongodb+srv://jesusdiaz1403:b1mRAtZw3MK5Q5eO@moneymap.mpksh.mongodb.net/")

db = client["MoneyMap"]

userInfo = db["User"]

def userData():
    user_info = {}
    user_info["MonthlyIncome"] = float(input("Enter your monthly income: "))
    user_info["MonthlyExpenses"] = float(input("Enter your monthly expenses: "))
    user_info["Checking"] = float(input("Enter your checking account balance: "))
    user_info["Savings"] = float(input("Enter your savings account balance: "))
    user_info["CreditCard"] = float(input("Enter your credit card balance: "))
    user_info["Loans"] = float(input("Enter your loan balance: "))

def saveUser(userData):
    userInfo.insert_one(userData)
    print("User Info Updated!")

def get_user(user_id):
    user = userInfo.find_one({"_id": user_id}, ["MonthlyIncome", "MonthlyExpenses", "Checking", "Savings", "CreditCard", "Loans"])
    if user:
        return {
            "MonthlyIncome": user["MonthlyIncome"],
            "MonthlyExpenses": user["MonthlyExpenses"],
            "Checking": user["Checking"],
            "Savings": user["Savings"],
            "CreditCard": user["CreditCard"],
            "Loans": user["Loans"]
        }
    else:
        print("User not found")
        return None

    

