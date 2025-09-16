from app import create_app

app = create_app()

@app.route('/')
def mostrar_login():
    # Esta ruta podrías moverla al blueprint de auth si lo preferís
    return "¡Zainex corriendo!"

if __name__ == '__main__':
    app.run(debug=True)
    
    