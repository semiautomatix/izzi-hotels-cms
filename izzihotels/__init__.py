
# firebase
import firebase_admin
from firebase_admin import credentials

# firebase credentials
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)  