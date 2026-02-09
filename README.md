![Logotipo de la aplicación](img-doc/derejpress.png)

# Documentación Técnica de Derej Press

## 1. Introducción

El poryecto **Derej Press** es un sistema integral para la gestión de préstamos, cobranzas y control de clientes. Centraliza el ciclo de vida de préstamos, pagos, anulaciones, reportes y administración de clientes, permitiendo a financieras y entidades de crédito operar de forma eficiente y segura. Está construido sobre **Django 5.2.1** con un backend basado en **MySQL** y una única app denominada `prestamos`, que concentra modelos, vistas, plantillas y recursos estáticos propios del negocio.

## 2. Tecnologías y dependencias clave

- **Django 5.2.1** como framework web y ORM.
- **MySQL** como motor relacional principal (configurado mediante variables de entorno en `settings.py`).
- **ReportLab** y **xhtml2pdf** para emisión de comprobantes PDF y reportes impresos.
- **WhiteNoise** para servir archivos estáticos en despliegues productivos.
- **python-dotenv** (`load_dotenv`) para inyectar secretos y credenciales sin exponerlos en el repositorio.
- **django-prometheus** para métricas y monitoreo.

## 3. Arquitectura general

- **App única (`prestamos`)**: concentra los modelos de dominio, vistas y rutas declaradas en `urls.py`.
- **Plantillas HTML** bajo `templates/prestamos/`, organizadas por vistas (clientes, préstamos, pagos, reportes, etc.).
- **Recursos estáticos** ubicados en `static/` y recolectados en `staticfiles/` para despliegue.
- **Configuración central** en `settings.py`, donde se habilitan middlewares, almacenamiento de estáticos y parámetros regionales.
- **Seguridad**: autenticación estándar de Django, decoradores y permisos para operaciones sensibles (por ejemplo, anulación de recibos o edición de clientes).

## Estructura de Carpetas

```
sistema_pagareses/
│   manage.py
│   requirements.txt
│   manifest.json
│   sw.js
│
├── prestamos/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   └── prestamos/
│   │       ├── anulacion.html
│   │       ├── anulacionderesivo.html
│   │       ├── cliente_detalle.html
│   │       ├── clientes.html
│   │       ├── despacho.html
│   │       ├── estadosdecuentas.html
│   │       ├── facturas.html
│   │       ├── formulario.html
│   │       ├── index.html
│   │       ├── pagare_pdf.html
│   │       ├── prestamospagados.html
│   │       ├── registrodepago.html
│   │       ├── reimprimir.html
│   │       ├── reporte.html
│   │       ├── vistadecliente.html
│   ├── migrations/
│   ├── static/
│   ├── tests.py
│   ├── admin.py
│   ├── apps.py
│
├── sistema_pagareses/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│
├── staticfiles/
│   └── ...
```

## 4. Modelo de datos principal

Los modelos residen en `models.py` y cubren todo el ciclo operativo:

| Modelo            | Rol principal                                                             | Relacionamientos destacados                |
| ----------------- | ------------------------------------------------------------------------- | ------------------------------------------ |
| `Cliente`         | Registro de clientes, datos personales, contacto y financieros.           | Asociado a `Prestamo`, `Ingreso`.          |
| `Prestamo`        | Encapsula cada préstamo, cliente, monto, fechas, estado y método de pago. | FK a `Cliente`, relacionado con `Ingreso`. |
| `Ingreso`         | Registra pagos realizados a préstamos, métodos, tipo y anulación.         | FK a `Prestamo`, anulación por usuario.    |
| `RecibosAnulados` | Historial de recibos anulados, con trazabilidad y usuario responsable.    | FK a `Prestamo`, usuario.                  |

## 5. Módulos funcionales

### 5.1 Autenticación y roles

- Vista `index` maneja login utilizando `django.contrib.auth`. Redirige a reportes tras autenticarse.
- Decoradores y permisos protegen vistas críticas (anulación, edición, eliminación).

### 5.2 Dashboard y reportes

- Vista `reporte` muestra métricas: clientes con mayor deuda, métodos de pago más usados, mejores pagadores, historial de pagos.
- Gráficas y tablas interactivas con datos agregados.

### 5.3 Gestión de clientes

- Registro, edición, eliminación y consulta de clientes.
- Validación de datos y unicidad de identificación.

### 5.4 Préstamos

- Registro de préstamos, asignación de número de factura único, control de estado y vencimiento.
- Relación directa con clientes y pagos.

### 5.5 Pagos y recibos

- Registro de pagos, generación de recibos únicos, control de abonos y pagos completos.
- Generación de comprobantes PDF listos para impresión térmica.

### 5.6 Anulaciones y devoluciones

- Anulación de préstamos y recibos, con registro de motivo, usuario y fecha.
- Restauración de saldos y trazabilidad completa.

### 5.7 Reportes y utilitarios

- Reportes PDF, exportaciones y consultas especiales para gestión y auditoría.

## 6. Flujo operativo end-to-end

1. **Registro de cliente**: alta de datos personales y financieros.
2. **Registro de préstamo**: asignación de cliente, monto, fechas y método de pago.
3. **Registro de pago**: abono o pago completo, generación de recibo y actualización de saldo.
4. **Anulación**: reversión de préstamos o recibos, restaurando saldos y dejando trazabilidad.
5. **Reportes**: visualización de métricas, exportación y análisis.

## 7. Integraciones internas y archivos relevantes

- **Rutas**: centralizadas en `urls.py`.
- **Plantillas**: cada feature tiene su HTML (por ejemplo, `clientes.html`, `reporte.html`, `registrodepago.html`).
- **Assets**: imágenes y scripts en `static/`; archivos compilados en `staticfiles/` listos para WhiteNoise.

## 8. Seguridad y cumplimiento

- Credenciales y llaves se cargan desde `.env` (no versionado).
- CSRF habilitado globalmente; endpoints críticos usan `@csrf_exempt` solo cuando es imprescindible.
- Validaciones server-side para montos, unicidad y consistencia de datos.
- Permisos y autenticación para operaciones sensibles.

## 9. Despliegue y configuración

1. Crear archivo `.env` con las siguientes variables de entorno:

```bash
SECRET_KEY="tu_clave_secreta"
DB_NAME="nombre_base_datos"
DB_USER="usuario"
DB_PASSWORD="contraseña"
DB_HOST="localhost"
DB_PORT="3306"
ALLOWED_HOSTS="localhost,127.0.0.1"
CSRF_TRUSTED_ORIGINS="http://localhost,http://127.0.0.1"
DEBUG=True
```

2. Instalar dependencias (`requirements.txt`).
3. Ejecutar migraciones (`python manage.py migrate`).
4. Crear superusuario (`python manage.py createsuperuser`).
5. Colectar estáticos (`python manage.py collectstatic`).
6. Configurar servicio WSGI apuntando a `wsgi.py` y habilitar WhiteNoise para estáticos.

## 10. Métricas y mejoras futuras sugeridas

- **KPI adicionales**: aging de cuentas, ranking de clientes, alertas de vencimiento.
- **Alertas proactivas**: notificaciones por correo o WhatsApp para cuentas vencidas.
- **API pública**: encapsular endpoints clave en una API REST (Django REST Framework).
- **Pruebas automatizadas**: ampliar `tests.py` con casos de préstamo, pago y anulación.

---

## Modelos Clave

- **Cliente:** Datos personales, contacto y financieros.
- **Prestamo:** Préstamos, estado, fechas, monto y cliente asociado.
- **Ingreso:** Pagos, abonos, tipo, método y anulación.
- **RecibosAnulados:** Historial de anulaciones, motivos y usuario responsable.

## Templates

La aplicación cuenta con templates personalizados para cada funcionalidad, con diseño moderno y sidebar fijo. Ejemplos:

- `clientes.html`: Gestión y consulta de clientes.
- `prestamospagados.html`: Listado de préstamos pagados.
- `registrodepago.html`: Registro y control de pagos.
- `reporte.html`: Dashboard y métricas.
- `anulacion.html`: Anulación de préstamos.
- `anulacionderesivo.html`: Anulación de recibos.
- `facturas.html` y `pagare_pdf.html`: Comprobantes y pagarés para impresión.

## Instalación

1. **Requisitos:**
   - Python 3.10+
   - Django 5.2.1
   - MySQL
   - Paquetes adicionales: `pillow`, `reportlab`, `xhtml2pdf`, `django-prometheus`, `python-dotenv`, `whitenoise`.

2. **Instalación de dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configuración de base de datos:**
   - Edita las variables de entorno en `.env` para definir `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.
   - El sistema utiliza MySQL con configuración estricta y soporte para zona horaria.

4. **Migraciones:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Creación de superusuario:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecución del servidor:**
   ```bash
   python manage.py runserver
   ```

## Uso

- Accede al sistema desde el navegador en `http://localhost:8000`.
- Inicia sesión con usuario registrado.
- Utiliza el dashboard para visualizar métricas.
- Gestiona clientes, préstamos, pagos, anulaciones y reportes desde el menú lateral.
- Imprime comprobantes y pagarés desde las vistas correspondientes.

## Seguridad y Roles

- El sistema implementa autenticación y autorización basada en usuarios y permisos de Django.
- Los roles permiten segmentar el acceso a funcionalidades críticas.

## Pruebas

- El archivo `tests.py` está preparado para pruebas unitarias con Django TestCase.
- Se recomienda implementar pruebas para cada modelo y vista crítica.

## Personalización

- Los templates pueden ser adaptados para branding propio.
- El sistema soporta ampliación de modelos y vistas para nuevas funcionalidades.

## Dependencias

Ver archivo `requirements.txt` para la lista completa.

## Configuración

- Variables de entorno para seguridad y base de datos.
- Soporte para archivos estáticos y media.
- Configuración de zona horaria y localización.

## Contacto y Soporte

Para soporte, contactar al desarrollador o consultar la documentación de Django.

---
