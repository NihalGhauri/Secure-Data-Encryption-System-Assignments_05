import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import time
import pymongo
import os
from dotenv import load_dotenv
import base64

load_dotenv()

st.set_page_config(
    page_title="Secure Data Encryption System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Enhanced Professional Encryption App CSS */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Manrope:wght@300;400;500;600;700&display=swap');

:root {
  /* Color palette */
  --primary-color: #6366f1;
  --primary-light: #818cf8;
  --secondary-color: #06b6d4;
  --dark-bg: #0f172a;
  --card-bg: #1e293b;
  --light-bg: #334155;
  --light-text: #f8fafc;
  --muted-text: #94a3b8;
  --success-color: #10b981;
  --error-color: #ef4444;
  
  /* UI properties */
  --border-radius-sm: 6px;
  --border-radius: 12px;
  --shadow-sm: 0 2px 6px rgba(0, 0, 0, 0.15);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.2);
  --font-main: 'Plus Jakarta Sans', sans-serif;
  --font-heading: 'Manrope', sans-serif;
}

/* Base Styling */
body {
  font-family: var(--font-main);
  background-color: var(--dark-bg);
  color: var(--light-text);
  line-height: 1.6;
  letter-spacing: 0.2px;
}

/* Simplified scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: var(--dark-bg);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--primary-light);
}

/* Container styling */
.main .block-container {
  padding: 2rem;
  max-width: 1200px;
  background: var(--card-bg);
  border-radius: var(--border-radius);
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: var(--shadow-sm);
}

/* Typography */
h1 {
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 2rem;
  color: var(--light-text);
}

h2 {
  font-family: var(--font-heading);
  font-weight: 600;
  font-size: 1.75rem;
  color: var(--light-text);
  margin-bottom: 1.5rem;
}

h3 {
  font-family: var(--font-heading);
  font-weight: 500;
  font-size: 1.25rem;
  color: var(--light-text);
  margin-bottom: 1rem;
}

p {
  color: var(--muted-text);
  line-height: 1.7;
  margin-bottom: 1rem;
  font-weight: 300;
}

/* Card styling */
.data-card {
  background: var(--card-bg);
  border-radius: var(--border-radius);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-left: 4px solid var(--primary-color);
  transition: transform 0.2s ease;
}

.data-card:hover {
  transform: translateY(-3px);
}

/* Form styling */
.stForm {
  background: var(--card-bg);
  border-radius: var(--border-radius);
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.stTextInput input, .stTextArea textarea {
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius-sm);
  color: var(--light-text);
  padding: 0.75rem 1rem;
  font-family: var(--font-main);
}

/* Add spacing to placeholder text */
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
  padding-left: 0.5rem; /* Add spacing to the left of the placeholder text */
  word-spacing: 0.4 rem;
  color: var(--muted-text);
  opacity: 0.7; /* Slightly reduce opacity for better contrast */
}

.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: var(--primary-color);
  outline: none;
}

/* Password visibility toggle (eye icon) */
.stTextInput input[type="password"] + div {
  position: relative;
}

.stTextInput input[type="password"] + div::after {
  content: '👁️';
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--muted-text);
  cursor: pointer;
}

/* Button styling */
.stButton button {
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-weight: 500;
  font-family: var(--font-main);
  transition: background 0.2s ease;
}

.stButton button:hover {
  background: var(--primary-light);
}

/* Sidebar styling */
.sidebar .sidebar-content {
  background: var(--dark-bg);
  padding: 1.5rem;
  border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* User info styling */
.user-info {
  background: var(--card-bg);
  border-radius: var(--border-radius);
  padding: 1.25rem;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.user-info h3 {
  font-size: 1.25rem;
  margin: 0 0 0.5rem 0;
  color: var(--light-text);
}

.status {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  background: rgba(16, 185, 129, 0.15);
  color: var(--success-color);
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--success-color);
  margin-right: 8px;
}

/* Selectbox styling */
.stSelectbox [data-baseweb="select"] {
  background-color: var(--light-bg);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius-sm);
  color: var(--light-text);
}

.stSelectbox [data-baseweb="select"]:hover {
  border-color: var(--primary-color);
}

/* Login/Signup form styling */
#login_form, #signup_form {
  max-width: 480px;
  margin: 0 auto;
  padding: 2rem;
  background: var(--card-bg);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-md);
  border: 1px solid rgba(255, 255, 255, 0.05);
  position: relative;
}

#login_form::before, #signup_form::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
}

/* Feature card styling */
.feature-card {
  text-align: center;
  background: var(--card-bg);
  border-radius: var(--border-radius);
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: transform 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card .icon {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.feature-card h4 {
  font-weight: 600;
  color: var(--light-text);
  margin-bottom: 0.75rem;
}

.feature-card p {
  color: var(--muted-text);
  font-size: 0.9rem;
}

/* Enhanced tabs styling */
.stTabs [data-baseweb="tab-list"] {
  display: flex;
  justify-content: center; /* Center the tabs */
  align-items: center;
  gap: 0; /* Remove gap between tabs */
  margin-bottom: 1.5rem;
  background-color: transparent; /* Remove background to match the image */
  padding: 0;
  border: none;
}

.stTabs [data-baseweb="tab"] {
  flex: 0 0 50%; /* Each tab takes 50% of the container width */
  background-color: var(--card-bg);
  border-radius: 0; /* Remove border radius for seamless connection */
  padding: 0.75rem 1rem;
  color: var(--light-text);
  border: 1px solid rgba(255, 255, 255, 0.05);
  font-family: var(--font-main);
  font-weight: 500;
  font-size: 1rem;
  text-align: center;
  transition: all 0.2s ease;
  position: relative;
}



.stTabs [data-baseweb="tab"]:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: var(--light-text);
}

.stTabs [aria-selected="true"] {
  background: var(--primary-color);
  color: var(--light-text);
  border: 1px solid var(--primary-color);
  box-shadow: var(--shadow-sm);
}

/* Remove the "L60" pseudo-element */
.stTabs [data-baseweb="tab-list"]::before {
  content: none; /* Remove the "L60" text */
}

/* Remove the order adjustments since "L60" is removed */
.stTabs [data-baseweb="tab-list"] {
  display: flex;
  flex-wrap: nowrap;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  h1 {
    font-size: 2rem;
  }
  
  h2 {
    font-size: 1.5rem;
  }
  
  .data-card, .feature-card {
    padding: 1.25rem;
  }
  
  .main .block-container {
    padding: 1.25rem;
  }

  .stTabs [data-baseweb="tab"] {
    padding: 0.5rem 0.75rem;
    font-size: 0.9rem;
  }
}
            </style>

""", unsafe_allow_html=True)

def get_database():
    try:
        connection_string = os.getenv("MONGODB_URI")
        if not connection_string:
            st.error("MongoDB connection string not found in environment variables")
            try:
                connection_string = "mongodb+srv://shelby42202:sZs2w5MNmG0duDsk@cluster0.jqyqlmx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
            except:
                connection_string = "mongodb+srv://yourusername:yourpassword@cluster0.mongodb.net/"
                st.error("Please set up your MongoDB connection string in .env file or Streamlit secrets")
        client = pymongo.MongoClient(connection_string)
        return client['secure_encryption_db']
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        return None

db = get_database()

def initialize_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if 'current_user' not in st.session_state:
        st.session_state.current_user = None

    if 'failed_attempts' not in st.session_state:
        st.session_state.failed_attempts = 0

    if 'locked_until' not in st.session_state:
        st.session_state.locked_until = 0


    if 'page' not in st.session_state:
        st.session_state.page = "login"


initialize_session_state()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_key_from_passkey(passkey):
    key_bytes = hashlib.sha256(passkey.encode()).digest()
    return base64.urlsafe_b64encode(key_bytes)

def encrypt_data(text, passkey):
    key = generate_key_from_passkey(passkey)
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text, passkey):
    try:
        key = generate_key_from_passkey(passkey)
        f = Fernet(key)
        return f.decrypt(encrypted_text.encode()).decode()
    except Exception:
        st.session_state.failed_attempts += 1
        return None

def signup(username, password, confirm_password):
    if db is None:
        return False, "Database connection error"
    
    users_collection = db['users']
    existing_user = users_collection.find_one({"username": username})
    if existing_user is not None:
        return False, "Username already exists"
    
    if password != confirm_password:
        return False, "Passwords do not match"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    user_data = {
        "username": username,
        "password": hash_password(password),
        "created_at": time.time()
    }
    
    users_collection.insert_one(user_data)
    data_collection = db['user_data']
    data_collection.insert_one({
        "username": username,
        "items": {}
    })
    
    return True, "Signup successful. Please login."

def login(username, password):
    if db is None:
        return False, "Database connection error"
    
    users_collection = db['users']
    user = users_collection.find_one({"username": username})
    
    if user is None:
        return False, "Username does not exist"
    
    if user["password"] != hash_password(password):
        return False, "Incorrect password"
    
    return True, "Login successful"

def store_user_data(username, data_label, data_content, passkey):
    if db is None:
        return None
    
    data_collection = db['user_data']
    user_data = data_collection.find_one({"username": username})
    
    if user_data is None:
        user_data = {
            "username": username,
            "items": {}
        }
        data_collection.insert_one(user_data)
        user_data = data_collection.find_one({"username": username})
    
    encrypted_text = encrypt_data(data_content, passkey)
    encrypted_passkey = hash_password(passkey)
    
    item_id = f"item_{int(time.time())}"
    items = user_data.get("items", {})
    items[item_id] = {
        "label": data_label,
        "encrypted_text": encrypted_text,
        "passkey_hash": encrypted_passkey,
        "created_at": time.time()
    }
    
    data_collection.update_one(
        {"username": username},
        {"$set": {"items": items}}
    )
    
    return encrypted_text

def get_user_data(username):
    if db is None:
        return {}
    
    data_collection = db['user_data']
    user_data = data_collection.find_one({"username": username})
    
    if user_data is None:
        return {}
    
    return user_data.get("items", {})

def decrypt_user_data(username, encrypted_text, passkey, item_id):
    if db is None:
        return None
    
    data_collection = db['user_data']
    user_data = data_collection.find_one({"username": username})
    if not user_data or item_id not in user_data.get("items", {}):
        return None
    
    stored_passkey_hash = user_data["items"][item_id]["passkey_hash"]
    provided_passkey_hash = hash_password(passkey)
    
    if stored_passkey_hash != provided_passkey_hash:
        st.session_state.failed_attempts += 1
        return None
    
    try:
        decrypted_text = decrypt_data(encrypted_text, passkey)
        st.session_state.failed_attempts = 0
        return decrypted_text
    except Exception:
        st.session_state.failed_attempts += 1
        return None

def main():
    current_time = time.time()
    if st.session_state.locked_until > current_time:
        with st.container():
            st.error(f"⚠️ System locked. Try again in {int(st.session_state.locked_until - current_time)} seconds.")
        return

    if db is None:
        st.error("Database connection failed")
        st.info("Continuing in demo mode with limited functionality")

    if not st.session_state.authenticated:
        show_auth_page()
    else:
        show_app_pages()

    st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center; margin-top: 5rem; font-size: 20px;">
        Made with ❤️ by Nihal Khan Ghauri
    </div>
    """,
    unsafe_allow_html=True
)

def show_auth_page():
    with st.container():
        st.markdown("<h1 style='text-align: center;'>🛡️ Secure Data Encryption System</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "SignUp"])
        
        with tab1:
            show_login_page()
        
        with tab2:
            show_signup_page()

def show_login_page():
    st.markdown("<h2 style='text-align: center;'>Welcome Back</h2>", unsafe_allow_html=True)
    
    with st.form(key='login_form'):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username and password:
                with st.spinner("Authenticating..."):
                    success, message = login(username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.current_user = username
                        st.success(message)
                        st.session_state.page = "home"
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.error("Please fill in all fields")

def show_signup_page():
    st.markdown("<h2 style='text-align: center;'>Join Now</h2>", unsafe_allow_html=True)
    
    with st.form(key='signup_form'):
        username = st.text_input("Username", placeholder="Choose a username")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        submit_button = st.form_submit_button("Sign Up")
        
        if submit_button:
            if username and password and confirm_password:
                with st.spinner("Creating account..."):
                    success, message = signup(username, password, confirm_password)
                    if success:
                        st.success(message)
                        time.sleep(1)
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.error("Please fill in all fields")

def show_app_pages():
    with st.container():
        st.markdown("<h1>🛡️ Secure Data Encryption System</h1>", unsafe_allow_html=True)

        with st.sidebar:
            st.markdown(f"""
                    <div class='user-info'>
                        <h3>👤 {st.session_state.current_user}</h3>
                        <p class = status>Active Session</p>
                    </div> """, unsafe_allow_html=True)
            
            st.markdown("<h3>Navigation</h3>", unsafe_allow_html=True)
            menu = ["Home", "Store Data", "Retrieve Data", "My Data"]
            choice = st.selectbox("", menu, format_func=lambda x: f"📌 {x}")
            
            if st.button("Logout", key="logout"):
                st.session_state.authenticated = False
                st.session_state.current_user = None
                st.session_state.page = "login"
                st.rerun()

        st.session_state.page = choice.lower().replace(" ", "_")
        
        if choice == "Home":
            show_home_page()
        elif choice == "Store Data":
            show_store_data_page()
        elif choice == "Retrieve Data":
            show_retrieve_data_page()
        elif choice == "My Data":
            show_my_data_page()

def show_home_page():
    st.markdown("""
        <h2>Welcome</h2>
        <div class='data-card'>
            <h3>🛡️ Secure Data Encryption System</h3>
            <p>Store your sensitive data with unique passkeys for maximum security.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3>Features</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='data-card'>🔐 Unique Passkeys</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='data-card'>☁️ Cloud Storage</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='data-card'>🔒 User Authentication</div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='data-card'>📱 Secure Access</div>", unsafe_allow_html=True)

def show_store_data_page():
    st.markdown("<h2>📂 Store Data</h2>", unsafe_allow_html=True)
    
    with st.form(key='store_form'):
        data_label = st.text_input("Label", placeholder="e.g., 'Personal Notes'")
        user_data = st.text_area("Data", placeholder="Enter your sensitive information...", height=150)
        passkey = st.text_input("Passkey", type="password", placeholder="Enter a unique passkey")
        submit_button = st.form_submit_button("Encrypt & Store")
        
        if submit_button:
            if user_data and passkey:
                with st.spinner("Encrypting..."):
                    label = data_label if data_label else f"Data_{time.strftime('%Y%m%d_%H%M%S')}"
                    encrypted_text = store_user_data(
                        st.session_state.current_user,
                        label,
                        user_data,
                        passkey
                    )
                    if encrypted_text:
                        st.success("Data encrypted and stored successfully!")
                        st.code(encrypted_text, language="text")
                        st.info("Remember your passkey to decrypt this data later!")
                    else:
                        st.error("Failed to store data")
            else:
                st.error("Please provide both data and passkey")

def show_retrieve_data_page():
    st.markdown("<h2>🔍 Retrieve Data</h2>", unsafe_allow_html=True)
    user_items = get_user_data(st.session_state.current_user)
    
    if not user_items:
        st.info("No stored data found")
        return

    retrieval_method = st.radio("Method", ["Saved Items", "Manual Input"])
    
    if retrieval_method == "Saved Items":
        item_options = [f"{item['label']} - {time.strftime('%Y-%m-%d', time.localtime(item['created_at']))}" 
                       for item in user_items.values()]
        item_ids = list(user_items.keys())
        selected_item = st.selectbox("Select Item", item_options)
        selected_index = item_options.index(selected_item)
        selected_item_id = item_ids[selected_index]
        encrypted_text = user_items[selected_item_id]["encrypted_text"]
        st.code(encrypted_text, language="text")
    else:
        encrypted_text = st.text_area("Encrypted Text", height=150)
        selected_item_id = None

    passkey = st.text_input("Passkey", type="password", placeholder="Enter the passkey used to encrypt")

    if st.session_state.failed_attempts > 0:
        st.warning(f"Failed attempts: {st.session_state.failed_attempts}/3")

    if st.button("Decrypt"):
        if encrypted_text and passkey:
            with st.spinner("Decrypting..."):
                decrypted_text = decrypt_user_data(
                    st.session_state.current_user,
                    encrypted_text,
                    passkey,
                    selected_item_id if selected_item_id else "manual"
                )
                if decrypted_text:
                    st.success("Decrypted successfully!")
                    st.text_area("Decrypted Data", decrypted_text, height=200)
                else:
                    remaining = 3 - st.session_state.failed_attempts
                    st.error(f"Decryption failed! Wrong passkey. Attempts remaining: {remaining}")
                    if st.session_state.failed_attempts >= 3:
                        st.session_state.locked_until = time.time() + 30
                        st.session_state.failed_attempts = 0
                        st.rerun()
        else:
            st.error("Please provide both encrypted text and passkey")

def show_my_data_page():
    st.markdown("<h2>📋 My Data</h2>", unsafe_allow_html=True)
    user_items = get_user_data(st.session_state.current_user)
    
    if not user_items:
        st.info("No stored data found")
        return

    for item_id, item in user_items.items():
        with st.expander(f"{item['label']} - {time.strftime('%Y-%m-%d', time.localtime(item['created_at']))}", expanded=False):
            st.code(item["encrypted_text"], language="text")
            passkey = st.text_input(f"Passkey for {item['label']}", type="password", key=f"passkey_{item_id}")
            if st.button("Decrypt", key=f"decrypt_{item_id}"):
                if passkey:
                    with st.spinner("Decrypting..."):
                        decrypted_text = decrypt_user_data(
                            st.session_state.current_user,
                            item["encrypted_text"],
                            passkey,
                            item_id
                        )
                        if decrypted_text:
                            st.success("Decrypted successfully!")
                            st.text_area("Content", decrypted_text, height=150)
                        else:
                            st.error("Decryption failed - wrong passkey")
                else:
                    st.error("Please enter the passkey")

if __name__ == "__main__":
    main()













