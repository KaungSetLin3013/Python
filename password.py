import os
import hashlib
import base64
import json
from getpass import getpass

def xor_encrypt_decrypt(text, key):
    """Basic XOR encryption/decryption"""
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(text, key * len(text)))

def derive_key(password, salt):
    """Simple key derivation using SHA-256"""
    return hashlib.sha256((password + salt).encode()).hexdigest()

def save_to_key_file(master_hash, data, filename="key.txt"):
    """Save encrypted data to key.txt"""
    salt = os.urandom(16).hex()
    key = derive_key(master_hash, salt)
    encrypted_data = xor_encrypt_decrypt(data, key)
    with open(filename, "w") as f:
        f.write(f"{salt}\n{base64.b64encode(encrypted_data.encode()).decode()}")

def load_from_key_file(master_hash, filename="key.txt"):
    """Load and decrypt data from key.txt"""
    try:
        with open(filename, "r") as f:
            salt = f.readline().strip()
            encrypted_data = base64.b64decode(f.readline().strip()).decode()
        key = derive_key(master_hash, salt)
        return xor_encrypt_decrypt(encrypted_data, key)
    except:
        return None

def authenticate():
    """Handle master password authentication"""
    attempts = 3
    
    if os.path.exists("key.txt"):
        with open("key.txt", "r") as f:
            first_line = f.readline().strip()
            if not first_line:
                print("Corrupted key.txt file detected. Creating new one.")
                os.remove("key.txt")
                return authenticate()
    
    while attempts > 0:
        password = getpass("Enter master password: ")
        current_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if os.path.exists("key.txt"):
            decrypted_data = load_from_key_file(current_hash)
            if decrypted_data:
                return password, decrypted_data
            attempts -= 1
            print(f"Invalid password. {attempts} attempts remaining.")
        else:
            # First run - create new key.txt
            return password, "{}"
    
    print("Too many failed attempts. Exiting.")
    return None, None

def add_password(data, service, username, password):
    """Add a new password entry"""
    try:
        passwords = json.loads(data)
    except:
        passwords = {}
    passwords[service] = {"username": username, "password": password}
    return json.dumps(passwords)

def get_password(data, service):
    """Retrieve a password entry"""
    try:
        passwords = json.loads(data)
        return passwords.get(service)
    except:
        return None

def delete_service(data, service):
    """Delete a service entry"""
    try:
        passwords = json.loads(data)
        if service in passwords:
            del passwords[service]
            return True, json.dumps(passwords)
        return False, data
    except:
        return False, data

def show_all_services(data):
    """Display all stored services"""
    try:
        passwords = json.loads(data)
        if not passwords:
            print("\nNo services stored yet.")
            return False
        
        print("\nAll Stored Services:")
        print("-" * 40)
        for i, (service, details) in enumerate(passwords.items(), 1):
            print(f"{i}. {service.ljust(20)} | Username: {details['username']}")
        print("-" * 40)
        return True
    except:
        print("\nError reading stored services.")
        return False

def main():
    print("\n" + "="*40)
    print("PYTHON PASSWORD MANAGER".center(40))
    print("="*40)
    print("All data stored securely in key.txt")
    
    master_password, password_data = authenticate()
    if not master_password:
        return
    
    while True:
        print("\nMAIN MENU:")
        print("1. Store new password")
        print("2. Retrieve password")
        print("3. Show all services")
        print("4. Delete service")
        print("5. Exit")
        
        choice = input("\nChoose an option (1-5): ")
        
        if choice == "1":
            print("\nADD NEW PASSWORD")
            print("-"*20)
            service = input("Service name (e.g. Gmail): ")
            username = input("Username/Email: ")
            password = getpass("Password: ")
            password_data = add_password(password_data, service, username, password)
            save_to_key_file(hashlib.sha256(master_password.encode()).hexdigest(), password_data)
            print(f"\n[✓] Password for {service} saved successfully!")
        
        elif choice == "2":
            print("\nRETRIEVE PASSWORD")
            print("-"*20)
            service = input("Enter service name: ")
            entry = get_password(password_data, service)
            if entry:
                print(f"\nService:    {service}")
                print(f"Username:   {entry['username']}")
                print(f"Password:   {entry['password']}")
            else:
                print("\n[!] No entry found for that service.")
        
        elif choice == "3":
            print("\nSTORED SERVICES")
            print("-"*20)
            show_all_services(password_data)
        
        elif choice == "4":
            print("\nDELETE SERVICE")
            print("-"*20)
            if show_all_services(password_data):
                service = input("\nEnter service name to delete: ")
                success, password_data = delete_service(password_data, service)
                if success:
                    save_to_key_file(hashlib.sha256(master_password.encode()).hexdigest(), password_data)
                    print(f"\n[✓] Service '{service}' deleted successfully!")
                else:
                    print(f"\n[!] Service '{service}' not found.")
        
        elif choice == "5":
            print("\nExiting... Thank you for using the Password Manager!")
            break
        
        else:
            print("\n[!] Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Program terminated by user.")
    except Exception as e:
        print(f"\n\n[!] An error occurred: {str(e)}")