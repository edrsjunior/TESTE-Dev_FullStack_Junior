import bcrypt 
salt = bcrypt.gensalt()

def encryptPass(senha: str) -> str:
    securePass = bcrypt.hashpw(senha.encode("utf-8"),salt)
    # print(securePass)
    return securePass.decode("utf-8")

def descriptPass(senhaUser: str, senhaBD: str) -> bool:
    # print( len(senhaUser), len(senhaBD))
    result = bcrypt.checkpw(senhaUser.encode("utf-8"),senhaBD.encode("utf-8"))
    return result
    