# MetroMed — Sistema CRM con Gamificación

Sistema CRM y de Inventario desarrollado en Django con módulo de Gamificación (MetroCoins), enfocado en seguridad multicapa, rendimiento SPA y diseño responsivo.

## 📦 Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|---|---|---|
| Python | 3.14 | Lenguaje principal |
| Django | 6.0.6 | Framework web backend |
| SQLite3 | Integrada | Base de datos |
| Bootstrap 5 | Local | Framework CSS/JS |
| HTMX | Local | Navegación SPA sin recargas |
| django-bootstrap5 | 26.2 | Integración Bootstrap con Django |

## 🏗️ Arquitectura del Proyecto

```
dcrm/
├── dcrm/                   # Configuración principal Django
│   ├── settings.py         # INSTALLED_APPS, DB, Middleware
│   ├── urls.py             # Rutas principales
│   └── wsgi.py
├── website/                # App principal (CRUD + Auth)
│   ├── models.py           # Modelo Usuarios
│   ├── views.py            # Vistas CRUD + Login/Logout
│   ├── forms.py            # SignUpForm + AddUsuarioForm (con Regex)
│   ├── urls.py             # Rutas de la app website
│   └── templates/          # HTML + Static assets
│       ├── base.html       # Template base (Bootstrap local + HTMX)
│       ├── navbar.html     # Barra de navegación SPA
│       ├── home.html       # Página principal + Login
│       ├── register.html   # Registro de usuarios
│       └── static/         # CSS, JS locales
├── gamification/           # App de Gamificación MetroCoins
│   ├── models.py           # GameConfig, UserMetroCoins, GameSession...
│   ├── views.py            # Vistas de juegos + admin
│   ├── admin.py            # Registro en Django Admin
│   ├── urls.py             # Rutas /juegos/
│   └── templates/gamification/
│       ├── lobby.html      # Lobby de juegos disponibles
│       ├── cartas.html     # Juego de memoria (JS)
│       ├── serpiente.html  # Juego Snake (Canvas JS)
│       ├── ruleta.html     # Ruleta diaria (animación JS)
│       ├── preguntas.html  # Trivia de preguntas
│       ├── profile.html    # Perfil del usuario + historial
│       ├── ranking.html    # Top 50 jugadores
│       ├── admin_stats.html    # Estadísticas globales (staff)
│       └── admin_games.html    # Gestión de juegos (staff)
├── uml/                    # Diagramas PlantUML
│   ├── 01_contexto_c1.puml
│   ├── 02_contenedores_c2.puml
│   ├── 03_componentes_c3.puml
│   ├── 04_codigo_c4.puml
│   ├── 05_patron_mtv.puml
│   ├── 06_patron_decorator.puml
│   ├── 07_patron_dry_modelform.puml
│   ├── 08_patron_template_method.puml
│   ├── 09_patron_observer_signals.puml
│   └── 10_patron_strategy.puml
├── arquitectura.puml       # Diagrama general de arquitectura
├── requirements.txt        # Dependencias del proyecto
├── README.md               # Este archivo
└── manage.py               # Comando de gestión Django
```

## 🔐 Módulos y Funcionalidades

### 1. Login con Roles
- Sistema de autenticación con `django.contrib.auth`.
- Control de acceso basado en `is_staff` y `is_superuser`.
- Decoradores `@login_required` y `@staff_member_required` para proteger vistas.
- Helper `is_admin()` para verificar permisos en operaciones CRUD.

### 2. CRUD Completo
- **Create:** `add_record` — Agregar registros de usuarios.
- **Read:** `home` — Listado de todos los registros; `customer_record` — Detalle individual.
- **Update:** `update_record` — Editar registros existentes.
- **Delete:** `delete_record` — Eliminar registros (solo Admin).

### 3. Menú SPA (Single Page Application)
- Integración de **HTMX** cargado localmente (`htmx.min.js`).
- Atributo `hx-boost="true"` en el `<body>` para intercepción automática de enlaces.
- Atributos `hx-get`, `hx-target="#main-content"` y `hx-push-url="true"` en el navbar.
- Navegación fluida sin recargas completas de página.

### 4. Alertas
- Framework `messages` de Django con alertas Bootstrap descartables.
- Toasts asíncronos de Bootstrap para recompensas de juegos.

### 5. Módulo de Gamificación (MetroCoins)
- **4 Juegos interactivos:** Cartas en Pareja, Serpiente, Ruleta Diaria, Trivia.
- **Sistema de recompensas:** MetroCoins con niveles (Bronce → Plata → Oro → Platino).
- **Panel administrativo:** Gestión de juegos y estadísticas globales.
- **Ranking global:** Top 50 jugadores por monedas acumuladas.

## 🛡️ Seguridad — 4 Capas

| Capa | Mecanismo | Ubicación |
|---|---|---|
| **1. Frontend** | Atributo HTML `pattern="^[a-zA-Z0-9_]*$"` + `required` | Templates HTML |
| **2. Backend** | `RegexValidator` de Django en `forms.py` | `website/forms.py` |
| **3. Autorización** | `@login_required`, `@staff_member_required`, `is_admin()` | `views.py` |
| **4. Base de Datos** | ORM Django parametriza queries (anti SQL Injection) + `{% csrf_token %}` | ORM + Templates |

## 🎨 Interfaz y Recursos Locales

- **Bootstrap 5 Local:** CSS y JS cargados desde `/static/css/` y `/static/js/` sin CDNs externas.
- **HTMX Local:** Archivo `htmx.min.js` incluido en `/static/js/`.
- **Tema MetroCoins:** Paleta futurista de tonos tierra oscuros definida en `metrocoins.css`.
- **Tipografía:** Orbitron (títulos), Inter (cuerpo), JetBrains Mono (números).

## 📐 Patrones de Diseño Implementados

1. **MTV (Model-Template-View):** Arquitectura fundamental de Django separando datos, lógica y presentación.
2. **Decorator:** `@login_required` y `@staff_member_required` extienden comportamiento de vistas.
3. **DRY / ModelForm:** `AddUsuarioForm` genera campos automáticamente desde el modelo `Usuarios`.
4. **Template Method:** Herencia de templates (`base.html` → `home.html`, `lobby.html`, etc.).
5. **Observer (Signals):** `post_save` en `User` crea automáticamente la billetera `UserMetroCoins`.
6. **Strategy:** Cada juego implementa su propia fórmula de cálculo de monedas.

## 🚀 Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/LillianaU/clase_dj_Ficha-3147211.git

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# 4. Crear superusuario
python manage.py createsuperuser

# 5. Levantar el servidor
python manage.py runserver
```

## 👥 Equipo

Proyecto desarrollado como entregable final — Ficha 3147211.
