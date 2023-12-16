from DATABASE.connectDB import connection

def isAdminUser(userId: int) -> bool:
    cursor = connection.cursor()
    query = "SELECT isAdmin FROM usuario WHERE id = %s"
    cursor.execute(query,(userId,))

    res = cursor.fetchone()

    if res[0] == 1:
        return True
    else:
        return False
    