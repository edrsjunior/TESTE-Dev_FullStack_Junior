import bcrypt 

def encryptPass(senha: str) -> str:
    securePass = bcrypt.hashpw(senha.encode("utf-8"),bcrypt.gensalt())

    return securePass.decode("utf-8")

def descripPass(senhaBD: str, senhaUser: str) -> bool:
    return bcrypt.checkpw(senhaUser.encode("utf-8"),senhaBD.encode("utf-8"))