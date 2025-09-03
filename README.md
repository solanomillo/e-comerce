🛒 E-Commerce con Django

Este es un proyecto de e-commerce desarrollado con el framework Django, utilizando el sistema de Templates para la generación de vistas dinámicas.
La aplicación incluye un sistema completo de gestión de productos, categorías, búsqueda y un panel administrativo mejorado.

✨ Características principales

🔎 Búsqueda por categorías

🔎 Búsqueda por nombre de producto

📄 Vista de detalles del producto

🛍️ Carrito de compras persistente

👤 Gestión de usuarios y autenticación

🎨 Panel de administración moderno con Jazzmin

💳 Integración con PayPal Sandbox para pruebas de pagos

📑 Configuración mediante variables de entorno

🛠️ Tecnologías utilizadas

Backend: Django (Python)

Frontend: HTML5, CSS3, JavaScript

Framework CSS: Bootstrap 5

Iconos: FontAwesome

Panel Admin: Django Jazzmin

Base de datos: MySQL

Gestión de configuración: python-decouple

Control de dependencias: pip + virtualenv

🚀 Instalación y ejecución
1️⃣ Clonar el repositorio
git clone https://github.com/tuusuario/tu-repo.git
cd tu-repo

2️⃣ Crear y activar un entorno virtual
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate

3️⃣ Instalar dependencias
pip install -r requirements.txt

4️⃣ Configurar el archivo .env

Crea un archivo .env en la raíz del proyecto con las variables:

SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_NAME=tiendaonline
DATABASE_USER=tu_usuario
DATABASE_PASSWORD=tu_password
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306
PAYPAL_TEST=True
PAYPAL_USER_EMAIL=tu_email@business.example.com

5️⃣ Aplicar migraciones
python manage.py migrate

6️⃣ Crear un superusuario
python manage.py createsuperuser

7️⃣ Ejecutar el servidor
python manage.py runserver


La aplicación estará disponible en:
👉 http://127.0.0.1:8000/


📌 Próximas mejoras

✅ Cupones y descuentos

✅ Soporte para múltiples pasarelas de pago (Stripe, MercadoPago)

✅ Panel con estadísticas de ventas

✅ Envío de correos de confirmación de pedidos

📄 Licencia

Este proyecto se distribuye bajo la licencia MIT.
Eres libre de usarlo, modificarlo y adaptarlo para tus proyectos.