from cryptography.fernet import Fernet
from cryptography.fernet import Fernet, InvalidToken
from django.http import JsonResponse



def generate_key(filename="secret.key"):
    key = Fernet.generate_key()

    with open(filename, "wb") as key_file:
        key_file.write(key)

    print("Key generated and saved to", filename)



def load_key(filename="secret.key"):
    with open(filename, "rb") as key_file:
        return key_file.read()



def encrypt_file(input_file, output_file, key):
    f = Fernet(key)

    with open(input_file, "rb") as file:
        data = file.read()

    encrypted_data = f.encrypt(data)

    with open(output_file, "wb") as file:
        file.write(encrypted_data)

    print("File encrypted:", output_file)


def decrypt_file(input_file, output_file, key):

    try:
        f = Fernet(key)  

        with open(input_file, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = f.decrypt(encrypted_data)

        with open(output_file, "wb") as file:
            file.write(decrypted_data)

        print("File decrypted:", output_file)

    except InvalidToken:
        print("Error: Invalid key! Decryption failed.")
