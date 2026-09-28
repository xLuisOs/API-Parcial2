# API de Tareas del Estudiante (Serie III)

API sencilla en Django para que el dashboard pueda consultar las tareas del estudiante y marcarlas como completadas.

## Cómo levantarla

```bash
python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

La migración ya carga 5 tareas de ejemplo, así que se puede probar de una vez en `http://127.0.0.1:8000/api/tareas`.

## Contrato de la API

| Acción             | Método HTTP | Endpoint                          |
|--------------------|-------------|-----------------------------------|
| Consultar tareas   | GET         | `/api/tareas`                     |
| Consultar una tarea| GET         | `/api/tareas/{id}`                |
| Filtrar por estado | GET         | `/api/tareas?estado=pendiente`    |
| Completar tarea    | PATCH       | `/api/tareas/{id}`                |

Para completar una tarea se manda en el body:

```json
{ "estado": "completada" }
```

Usé PATCH porque solo cambia un campo de la tarea, no se reemplaza completa. El filtro va como query param porque sigue siendo la misma lista de tareas, solo que filtrada; no hace falta otro endpoint.

| Código | Cuándo                                            |
|--------|---------------------------------------------------|
| 200    | La consulta o la actualización salió bien         |
| 400    | El estado enviado no es `pendiente` ni `completada` |
| 404    | La tarea no existe                                |
| 405    | Se usa un método que no está permitido (ej. DELETE) |

## Preguntas

### 1. Ejemplo de respuesta JSON al consultar una tarea

`GET /api/tareas/2` → `200 OK`

```json
{
  "id": 2,
  "titulo": "Contrato de API del dashboard",
  "curso": "Programación Web",
  "fechaEntrega": "2026-09-30",
  "estado": "pendiente"
}
```

La fecha va en formato ISO (`AAAA-MM-DD`) para que el frontend la pueda leer sin problemas.

### 2. ¿Qué código devuelve si la tarea no existe?

Devuelve **404 Not Found**, porque la petición está bien hecha pero el recurso que se pide no existe. No tendría sentido mandar un 200 vacío ni un 500, porque el servidor no falló.

`GET /api/tareas/99` → `404 Not Found`

```json
{
  "error": {
    "codigo": "TAREA_NO_ENCONTRADA",
    "mensaje": "No existe una tarea con id 99."
  }
}
```

El mensaje le sirve a la persona y el `codigo` le sirve al frontend para saber qué pasó sin tener que leer el texto.

### 3. Un cambio que rompería el contrato (Breaking Change)

Cambiar `fechaEntrega` de texto ISO (`"2026-09-30"`) a otro formato, por ejemplo `"30/09/2026"`, o renombrar el campo a `fecha_entrega`. El dashboard ordena y marca las tareas vencidas usando ese campo, así que de un día para otro dejaría de funcionar aunque la API "siga respondiendo".

Lo mismo pasaría si se agregara un estado nuevo como `"en_progreso"` sin avisar, porque el frontend solo espera `pendiente` o `completada`.



