from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client.bank_db

accounts_col = db.accounts
transactions_col = db.transactions
