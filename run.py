from app import create_app

app = create_app()

if __name__ == '__main__':
    # Ejecuta la aplicación en modo debug y expone el puerto local
    app.run(debug=True, host='0.0.0.0', port=5000)