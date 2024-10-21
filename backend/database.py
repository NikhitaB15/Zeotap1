import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

client = pymongo.MongoClient(os.getenv('MONGO_URI'))
db = client['rule_engine']

def save_rule(rule_ast):
    db.rules.insert_one({"rule": rule_ast})

def get_all_rules(rule_ids):
    return list(db.rules.find({"_id": {"$in": rule_ids}}))
