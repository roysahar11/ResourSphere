import os
import yaml

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(f"{CURRENT_DIR}/config/security.yml", "r") as security_conf_file:
    security_config = yaml.safe_load(security_conf_file)

ACCESS_TOKEN_EXPIRATION_MINUTES = security_config.get("access_token_expiration_minutes")
JWT_ALGORITHM = security_config.get("jwt_algorithm")

def load_jwt_secret_key():
    with open(f"{CURRENT_DIR}/config/secrets.yml", "r") as secrets:
        return yaml.safe_load(secrets).get("jwt_secret_key")