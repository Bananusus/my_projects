# run.py

from app import create_app
import ssl

# Создаем экземпляр приложения, вызывая функцию из __init__.py
app = create_app()

if __name__ == '__main__':
    # Создаем SSL-контекст
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # Загружаем сертификат и приватный ключ
    context.load_cert_chain('cert.pem', 'key.pem')

    # Запускаем сервер разработки Flask с SSL-контекстом
    # host='127.0.0.1' - только локальный доступ
    # port=8443 - стандартный порт для HTTPS
    # ssl_context=context - указываем созданный SSL-контекст
    # debug=True - режим отладки (в продакшене НЕЛЬЗЯ использовать с ssl_context так!)
    app.run(debug=True, host='127.0.0.1', port=8443, ssl_context=context)
