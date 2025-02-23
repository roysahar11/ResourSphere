import secrets

# Generate a 256-bit (32-byte) secret key for HS256
jwt_secret = secrets.token_hex(32)  # 64-character hex string (32 bytes)
print(jwt_secret)