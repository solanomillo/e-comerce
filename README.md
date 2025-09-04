# 🛒 E-Commerce con Django
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=flat&logo=bootstrap&logoColor=white)
![FontAwesome](https://img.shields.io/badge/FontAwesome-339AF0?style=flat&logo=fontawesome&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Jazzmin](https://img.shields.io/badge/Jazzmin-FF6F00?style=flat&logo=django&logoColor=white)
![Estado](https://img.shields.io/badge/Estado-Funcional-green)

Este es un proyecto de **e-commerce** desarrollado con el framework **Django**, utilizando el sistema de **Templates** para la generación de vistas dinámicas.  
La aplicación incluye un sistema completo de gestión de productos, categorías, búsqueda y un panel administrativo mejorado.

---

## 📑 Tabla de contenidos
1. [✨ Características principales](#-características-principales)
2. [🛠️ Tecnologías utilizadas](#️-tecnologías-utilizadas)
3. [🚀 Instalación y ejecución](#-instalación-y-ejecución)
5. [📌 Próximas mejoras](#-próximas-mejoras)
6. [📄 Licencia](#-licencia)

---

## ✨ Características principales
- 🔎 **Búsqueda por categorías**  
- 🔎 **Búsqueda por nombre de producto**  
- 📄 **Vista de detalles del producto**  
- 🛍️ **Carrito de compras** persistente  
- 👤 **Gestión de usuarios y autenticación**  
- 🎨 **Panel de administración moderno con Jazzmin**  
- 💳 **Integración con PayPal Sandbox** para pruebas de pagos  
- 📑 **Configuración mediante variables de entorno**  

---

## 🛠️ Tecnologías utilizadas

![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=flat&logo=bootstrap&logoColor=white)
![FontAwesome](https://img.shields.io/badge/FontAwesome-339AF0?style=flat&logo=fontawesome&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Jazzmin](https://img.shields.io/badge/Jazzmin-FF6F00?style=flat&logo=django&logoColor=white)
![Estado](https://img.shields.io/badge/Estado-Funcional-green)

---

## 🚀 Instalación y ejecución

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/tuusuario/tu-repo.git
cd tu-repo
```
### 2️⃣ Crear y activar un entorno virtual
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```
### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```
### 4️⃣ Configurar el archivo .env

Crea un archivo .env en la raíz del proyecto con las variables:
```bash
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
```

### 5️⃣ Aplicar migraciones
```bash
python manage.py migrate
```

### 6️⃣ Crear un superusuario
```bash
python manage.py createsuperuser
```
### 7️⃣ Ejecutar el servidor
```bash
python manage.py runserver
```
La aplicación estará disponible en:
👉 http://127.0.0.1:8000/

📌 Próximas mejoras

✅ Soporte para múltiples pasarelas de pago (Stripe, MercadoPago)

✅ Panel con estadísticas de ventas

✅ Envío de correos de confirmación de pedidos

# 👨‍💻 Autor
**Julio Solano**  
🔗 [GitHub](https://github.com/solanomillo)  
📧 solanomillo144@gmail.com

📄 Licencia

Este proyecto se distribuye bajo la licencia MIT.
Eres libre de usarlo, modificarlo y adaptarlo para tus proyectos.
