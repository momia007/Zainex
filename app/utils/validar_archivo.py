# validar_archivo.py

def validar_archivo(file_storage):
    """
    Valida si el archivo recibido es válido y tiene contenido.
    Devuelve una tupla: (es_valido: bool, contenido: bytes)
    """
    if not file_storage or not file_storage.filename:
        return False, None

    contenido = file_storage.read()
    file_storage.seek(0)  # Volver al inicio para futuras operaciones

    if len(contenido) == 0:
        return False, None

    return True, contenido
