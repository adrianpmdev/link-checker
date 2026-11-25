<div align="center">

# 🔗 Link Checker

### Servicio interno que comprueba periódicamente que los enlaces de los productos siguen funcionando

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

[![Author](https://img.shields.io/badge/Author-adrianpmdev-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/adrianpmdev)

</div>

---

<br>

## 📖 Descripción

Pequeño **servicio interno para una tienda online**. Guarda los productos y sus enlaces, **los comprueba automáticamente** cada cierto tiempo y ofrece un endpoint con los **productos cuyos enlaces están rotos**.

> 🎯 **Un enlace está roto** cuando la petición falla o el servidor responde con un código 4xx o 5xx.

---

<br>

## 🚀 Funcionalidades

- ⏱️ **Comprobación periódica** de todos los enlaces, al arrancar y cada `CHECK_INTERVAL_MINUTES`.
- 🔁 **Reintento con GET** cuando el servidor no admite `HEAD`.
- 🔒 **Sin comprobaciones solapadas**: si ya hay una en marcha, la manual responde `409`.
- 📚 **Documentación de la API** (Swagger) en `/docs`.

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/health` | Estado del servicio |
| GET | `/products` | Listar todos los productos |
| POST | `/products` | Añadir un producto |
| GET | `/products/broken` | Listar los productos con enlaces rotos |
| POST | `/checks/run` | Lanzar una comprobación ahora |

---

<br>

## ⚙️ Puesta en marcha

Necesitas **Python 3.12 o superior** ([python.org/downloads](https://www.python.org/downloads/)). Desde la carpeta del proyecto:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abre http://localhost:8000/docs. En el primer arranque se crean productos de ejemplo, algunos con enlaces rotos.

### 🔧 Ajustes

| Variable | Por defecto | Descripción |
| --- | --- | --- |
| `DB_PATH` | `data/link_checker.db` | Fichero SQLite |
| `SEED_SAMPLE_DATA` | `true` | Crear productos de ejemplo si la base de datos está vacía |
| `CHECK_INTERVAL_MINUTES` | `60` | Minutos entre comprobaciones automáticas |
| `REQUEST_TIMEOUT_SECONDS` | `10` | Tiempo máximo de espera por enlace |

### 🧪 Tests

```bash
python -m pytest
```

Los tests usan una base de datos temporal y respuestas HTTP falsas: no salen a la red.

---

<br>

## 📝 Decisiones y límites

- 🧵 **La comprobación periódica vive dentro de la API** y los enlaces se comprueban uno detrás de otro. Es suficiente para un catálogo pequeño; con muchos enlaces convendría comprobarlos en paralelo o en un proceso aparte.
- ⚠️ **El servicio hace peticiones a las URLs que se añaden**, así que no debe exponerse fuera de la red interna.
- 🔓 **Sin autenticación ni paginación**, por ser una herramienta interna pequeña.

---

<br>

## 👤 Autor

[@adrianpmdev](https://github.com/adrianpmdev) · Junior Full Stack Developer

---

<br>

<div align="center">

✨ Made in **2026** by [@adrianpmdev](https://github.com/adrianpmdev) ✨

</div>
