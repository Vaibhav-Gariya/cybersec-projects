import hashlib
import os
import json

def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None

def save_hash(file_path, hash_value, db_file="hash_db.json"):
    data = {}
    if os.path.exists(db_file):
        with open(db_file, "r") as f:
            data = json.load(f)
    data[file_path] = hash_value
    with open(db_file, "w") as f:
        json.dump(data, f, indent=4)
    print("✅ Hash saved.")

def check_integrity(file_path, db_file="hash_db.json"):
    if not os.path.exists(db_file):
        print("⚠️ Hash database not found. Please save the hash first.")
        return
    with open(db_file, "r") as f:
        saved_hashes = json.load(f)
    current_hash = calculate_hash(file_path)
    saved_hash = saved_hashes.get(file_path)

    if current_hash == saved_hash:
        print("✅ File is intact. No changes detected.")
    else:
        print("⚠️ File has been modified!")

def menu():
    print("\n--- File Integrity Checker ---")
    print("1. Calculate and save hash")
    print("2. Verify file integrity")
    print("3. Exit")

    while True:
        choice = input("Enter choice (1/2/3): ")
        if choice == '1':
            path = input("Enter file path to hash and save: ")
            hash_value = calculate_hash(path)
            if hash_value:
                save_hash(path, hash_value)
        elif choice == '2':
            path = input("Enter file path to verify: ")
            check_integrity(path)
        elif choice == '3':
            print("👋 Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()