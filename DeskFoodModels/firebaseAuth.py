import pyrebase

# Firebase Config - Required info to connect to Firebase
firebaseConfig = {
    'apiKey': "AIzaSyDU0ygdrujK-vkCQb7fRtkv2hGVbxV6A6I",
    'authDomain': "deskfoodapp.firebaseapp.com",
    'databaseURL': "https://deskfoodapp-default-rtdb.firebaseio.com",
    'projectId': "deskfoodapp",
    'storageBucket': "deskfoodapp.appspot.com",
    'messagingSenderId': "42027451518",
    'appId': "1:42027451518:web:69bb99b1689fafe5b2042f",
    'measurementId': "G-9M9EJD2HSH"
}

# Initializes connection to Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# Function to login to Firebase
def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except:
        return None

# Function to logout from Firebase
def logout():
    auth.logout()

# Function to create a new user in Firebase
# password must be at least 6 characters long
def register(email, password, username):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        db.child("Users").child(user['localId']).child("username").set(username)
        return user
    except:
        return None

#print(register("AnotherNewTest@sol.com", "askdfhvkd", "rocketMan")['localId'])