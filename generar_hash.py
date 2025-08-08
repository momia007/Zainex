import bcrypt
import getpass

def generar_hash():
    print("🔒 Generador de hash bcrypt para Zainex\n")
    # Pedir contraseña sin que se vea mientras se escribe
    password = getpass.getpass("👉 Ingresá la contraseña para superadmin: ")

    # Convertir a bytes y generar el hash
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    print("\n✅ Hash generado con éxito:")
    print(hashed.decode())

if __name__ == "__main__":
    generar_hash()
