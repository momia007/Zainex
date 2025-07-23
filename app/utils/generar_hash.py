import bcrypt

# Escribí acá la contraseña que querés encriptar
contrasena_plana = "02chi08"

# Generar el hash
hash_generado = bcrypt.hashpw(contrasena_plana.encode(), bcrypt.gensalt())

# Mostrar el resultado para pegarlo en el INSERT
print("Hash generado:")
print(hash_generado.decode())