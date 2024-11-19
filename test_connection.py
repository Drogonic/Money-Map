from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi

uri = "mongodb+srv://jesusdiaz1403:b1mRAtZw3MK5Q5eO@moneymap.mpksh.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(
        uri,
        server_api=ServerApi('1'),
        tls=True,
        tlsCAFile=certifi.where()  # Use certifi for CA validation
    )
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"Connection failed: {e}")
