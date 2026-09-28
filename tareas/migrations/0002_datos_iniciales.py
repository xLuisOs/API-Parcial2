from datetime import date

from django.db import migrations


def cargar_tareas(apps, schema_editor):
    Tarea = apps.get_model("tareas", "Tarea")
    Tarea.objects.bulk_create([
        Tarea(titulo="Diagrama ER de la clínica", curso="Bases de Datos II", fechaEntrega=date(2026, 9, 28), estado="pendiente"),
        Tarea(titulo="Contrato de API del dashboard", curso="Programación Web", fechaEntrega=date(2026, 9, 30), estado="pendiente"),
        Tarea(titulo="Analizador léxico", curso="Compiladores", fechaEntrega=date(2026, 10, 2), estado="pendiente"),
        Tarea(titulo="Hoja de integrales dobles", curso="Cálculo II", fechaEntrega=date(2026, 9, 25), estado="completada"),
        Tarea(titulo="Informe de pipeline", curso="Arquitectura de Computadoras", fechaEntrega=date(2026, 10, 5), estado="pendiente"),
    ])


class Migration(migrations.Migration):
    dependencies = [("tareas", "0001_initial")]
    operations = [migrations.RunPython(cargar_tareas, migrations.RunPython.noop)]
