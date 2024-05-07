import argon2, pyaes, os, time

hasher = argon2.PasswordHasher()





# Сгенерировать новый токен аутентификации (user_auth) из пароля и рандомной соли
def generate_new_auth(password):
    return str(hasher.hash(password))

# Проверить пароль на соответствие существующему токену аутентификации 
def check_existing_auth(auth, password):
    try:
        return hasher.verify(auth, password)
    except argon2.exceptions.VerifyMismatchError:
        return False





# Сгенерировать новую сессию: ключ сессии, время истечения, зашифрованные данные сессии
def generate_new_session(id, password, client, period):
    cypher = os.urandom(64).hex()
    expires = time.time() + period
    key = bytearray.fromhex(cypher[:64])
    iv = int(cypher[64:], 16)
    crypt = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    return (cypher, expires, crypt.encrypt(password), crypt.encrypt(client))

# Расшифровать существующую сессию
def check_existing_session(cypher, expires, session_password, session_client):
    if expires < time.time():
        return None
    key = bytearray.fromhex(cypher[:64])
    iv = int(cypher[64:], 16)
    crypt = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    try:
        password = crypt.decrypt(session_password).decode('ascii')
        client = crypt.decrypt(session_client).decode('ascii')
        return (password, client)
    except UnicodeDecodeError:
        return None