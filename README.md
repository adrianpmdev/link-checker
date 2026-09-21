<div align="center">

# Link Checker

### Servicio interno que comprueba periódicamente que los enlaces de los productos siguen funcionando

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
[![Author](https://img.shields.io/badge/Author-adrianpmdev-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/adrianpmdev)

</div>

---

## Descripción

Pequeño servicio interno para una tienda online. Guarda los productos y sus enlaces, comprueba todos los enlaces automáticamente cada cierto tiempo y ofrece un endpoint con los productos cuyos enlaces están rotos.

## Funcionalidades

- Comprobación automática y periódica de los enlaces de todos los productos.
- Guarda el código HTTP, si el enlace está roto y la fecha de la última comprobación de cada producto.
- Endpoint con la lista de productos con enlaces rotos.
- Comprobación bajo demanda sin esperar a la siguiente ejecución programada.
- Documentación interactiva de la API (Swagger) en `/docs`.

## Tecnologías

| Tecnología | Uso |
| --- | --- |
| Python 3.11+ | Lenguaje |
| FastAPI | API REST |
| Requests | Comprobación HTTP de los enlaces |
| SQLite | Almacenamiento |

## Estructura del proyecto

```
link-checker/
├── app/
│   ├── main.py          # Punto de entrada, ciclo de vida y routers
│   ├── config.py        # Configuración (variables de entorno)
│   ├── database.py      # Conexión SQLite, esquema y datos de ejemplo
│   ├── schemas.py       # Modelos Pydantic
│   ├── repository.py    # Consultas SQL
│   ├── checker.py       # Lógica de comprobación de enlaces
│   ├── scheduler.py     # Comprobación periódica en segundo plano
│   └── routers/
│       ├── products.py  # Endpoints /products
│       └── checks.py    # Endpoints /checks
├── data/                # Base de datos SQLite (se crea al arrancar)
└── requirements.txt
```

## Puesta en marcha

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abre http://localhost:8000/docs. En el primer arranque se crea la base de datos con productos de ejemplo, algunos con enlaces rotos.

### Configuración

| Variable | Por defecto | Descripción |
| --- | --- | --- |
| `DB_PATH` | `data/link_checker.db` | Fichero SQLite |
| `CHECK_INTERVAL_MINUTES` | `60` | Minutos entre comprobaciones automáticas |
| `REQUEST_TIMEOUT_SECONDS` | `10` | Tiempo máximo de espera por enlace |

## Endpoints

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/products` | Listar todos los productos |
| POST | `/products` | Añadir un producto |
| GET | `/products/broken` | Listar los productos con enlaces rotos |
| POST | `/checks/run` | Lanzar una comprobación ahora |

---

<div align="center">

Made in 2026 by [@adrianpmdev](https://github.com/adrianpmdev)

</div>
