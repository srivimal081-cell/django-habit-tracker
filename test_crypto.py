from crypto_utils import generate_key, load_key, encrypt_file, decrypt_file
from cryptography.fernet import Fernet

correct_key = load_key()


encrypt_file("storage.json", "storage_encrypted.bin", correct_key)


wrong_key = Fernet.generate_key()   


decrypt_file("storage_encrypted.bin", "fail.json", wrong_key)