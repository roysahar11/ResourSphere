from ..authentication import  get_password_hash
password = input("Enter a password: ")
pass_hash = get_password_hash(password)
print("Hash: ")
print(hash)