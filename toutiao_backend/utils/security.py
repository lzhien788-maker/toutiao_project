import bcrypt

# 不要用passlib了，passlib的bcrypt坑很多，直接原生bcrypt
def get_hash_password(password: str):
    # 先转bytes，截断前72字节
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")

def verify_password(plain_pwd: str, hashed_pwd: str):
    pwd_bytes = plain_pwd.encode("utf-8")[:72]
    return bcrypt.checkpw(pwd_bytes, hashed_pwd.encode("utf-8"))





