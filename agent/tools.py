# agent/tools.py — Herramientas del agente Taller la Frontera
import os
import yaml
import logging
from datetime import datetime

logger = logging.getLogger("agentkit")


def cargar_info_negocio() -> dict:
    try:
        with open("config/business.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error("config/business.yaml no encontrado")
        return {}


def obtener_horario() -> dict:
    info = cargar_info_negocio()
    ahora = datetime.now()
    dia_semana = ahora.weekday()  # 0=Lunes, 6=Domingo
    hora = ahora.hour

    if dia_semana < 5:  # Lunes a Viernes
        esta_abierto = 9 <= hora < 18
    elif dia_semana == 5:  # Sábado
        esta_abierto = 10 <= hora < 14
    else:
        esta_abierto = False

    return {
        "horario": info.get("negocio", {}).get("horario", "Lunes a Viernes 9am-6pm, Sábados 10am-2pm"),
        "esta_abierto": esta_abierto,
    }


def buscar_en_knowledge(consulta: str) -> str:
    resultados = []
    knowledge_dir = "knowledge"

    if not os.path.exists(knowledge_dir):
        return "No hay archivos de conocimiento disponibles."

    for archivo in os.listdir(knowledge_dir):
        ruta = os.path.join(knowledge_dir, archivo)
        if archivo.startswith(".") or not os.path.isfile(ruta):
            continue
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
                if consulta.lower() in contenido.lower():
                    resultados.append(f"[{archivo}]: {contenido[:500]}")
        except (UnicodeDecodeError, IOError):
            continue

    if resultados:
        return "\n---\n".join(resultados)
    return "No encontré información específica sobre eso en mis archivos."


# Herramientas para agendar citas
citas_pendientes: dict[str, dict] = {}


def iniciar_cita(telefono: str) -> dict:
    citas_pendientes[telefono] = {
        "nombre": None,
        "vehiculo": None,
        "servicio": None,
        "fecha": None,
        "hora": None,
        "paso": 1,
    }
    return citas_pendientes[telefono]


def obtener_cita_en_progreso(telefono: str) -> dict | None:
    return citas_pendientes.get(telefono)


def actualizar_cita(telefono: str, campo: str, valor: str):
    if telefono in citas_pendientes:
        citas_pendientes[telefono][campo] = valor


def confirmar_cita(telefono: str) -> str:
    cita = citas_pendientes.get(telefono)
    if not cita:
        return "No hay cita en progreso."
    resumen = (
        f"Cita agendada:\n"
        f"- Cliente: {cita.get('nombre', 'N/A')}\n"
        f"- Vehículo: {cita.get('vehiculo', 'N/A')}\n"
        f"- Servicio: {cita.get('servicio', 'N/A')}\n"
        f"- Fecha: {cita.get('fecha', 'N/A')}\n"
        f"- Hora: {cita.get('hora', 'N/A')}"
    )
    del citas_pendientes[telefono]
    return resumen


# Herramienta para calificar leads
def calificar_lead(nombre: str, tipo: str, vehiculos: str, necesidad: str) -> str:
    return (
        f"Lead registrado:\n"
        f"- Nombre/Empresa: {nombre}\n"
        f"- Tipo: {tipo}\n"
        f"- Vehículos: {vehiculos}\n"
        f"- Necesidad: {necesidad}"
    )
