import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Tarea

ESTADOS_VALIDOS = ["pendiente", "completada"]


def error(status, codigo, mensaje):
    return JsonResponse({"error": {"codigo": codigo, "mensaje": mensaje}}, status=status, json_dumps_params={"ensure_ascii": False})


@require_http_methods(["GET"])
def lista_tareas(request):
    tareas = Tarea.objects.all().order_by("fechaEntrega")
    estado = request.GET.get("estado")

    if estado:
        if estado not in ESTADOS_VALIDOS:
            return error(400, "ESTADO_INVALIDO", "El estado debe ser 'pendiente' o 'completada'.")
        tareas = tareas.filter(estado=estado)

    return JsonResponse({"data": [t.to_dict() for t in tareas]}, json_dumps_params={"ensure_ascii": False})


@csrf_exempt
@require_http_methods(["GET", "PATCH"])
def detalle_tarea(request, id):
    try:
        tarea = Tarea.objects.get(pk=id)
    except Tarea.DoesNotExist:
        return error(404, "TAREA_NO_ENCONTRADA", f"No existe una tarea con id {id}.")

    if request.method == "GET":
        return JsonResponse(tarea.to_dict(), json_dumps_params={"ensure_ascii": False})

    try:
        body = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return error(400, "JSON_INVALIDO", "El cuerpo de la petición no es un JSON válido.")

    if body.get("estado") != "completada":
        return error(400, "ESTADO_INVALIDO", "Solo se permite enviar {\"estado\": \"completada\"}.")

    tarea.estado = "completada"
    tarea.save()
    return JsonResponse(tarea.to_dict(), json_dumps_params={"ensure_ascii": False})
