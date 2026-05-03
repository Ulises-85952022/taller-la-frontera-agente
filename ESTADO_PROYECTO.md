# Estado del Proyecto — Taller la Frontera WhatsApp Agent

## Resumen
Agente de WhatsApp con IA construido con AgentKit. Está en producción y funcionando.

---

## Datos del negocio
- **Negocio:** Taller la Frontera
- **Giro:** Taller mecánico especializado en tracto camiones, vehículos diesel/gasolina, camionetas de carga y flotillas empresariales
- **Agente:** Soporte la Frontera
- **Tono:** Amigable y casual
- **Horario:** Lunes-Viernes 9am-6pm, Sábados 10am-2pm
- **Casos de uso:** FAQ, agendar citas, calificar leads

---

## Stack técnico
- **IA:** Claude API (claude-sonnet-4-6) vía Anthropic
- **Servidor:** FastAPI + Uvicorn
- **WhatsApp:** Whapi.cloud
- **Base de datos:** SQLite (aiosqlite + SQLAlchemy)
- **Deploy:** Render.com (plan gratuito)

---

## URLs y credenciales

### Producción
- **URL pública:** `https://taller-la-frontera-agente.onrender.com`
- **Webhook activo:** `https://taller-la-frontera-agente.onrender.com/webhook/messages`

### Repositorio GitHub
- **Repo:** `https://github.com/Ulises-85952022/taller-la-frontera-agente`
- **Rama:** `main`

### Variables de entorno (configuradas en Render)
- `ANTHROPIC_API_KEY` — en Render → Environment
- `WHAPI_TOKEN` — en Render → Environment
- `WHATSAPP_PROVIDER=whapi`
- `PORT=8000`
- `ENVIRONMENT=production`

> Las claves NO están en el repo. Están solo en Render y en el `.env` local (excluido de git).

---

## Estructura del proyecto
```
whatsapp-agentkit/
├── agent/
│   ├── main.py          ← FastAPI + rutas /webhook y /webhook/messages
│   ├── brain.py         ← Conexión Claude API
│   ├── memory.py        ← Historial SQLite por teléfono
│   ├── tools.py         ← FAQ, citas, leads
│   └── providers/
│       ├── base.py      ← Clase abstracta
│       ├── whapi.py     ← Adaptador Whapi.cloud
│       └── __init__.py  ← Factory de proveedores
├── config/
│   ├── business.yaml    ← Datos del negocio
│   └── prompts.yaml     ← System prompt del agente (AQUÍ SE PERSONALIZA)
├── knowledge/           ← Subir aquí PDF/TXT con info del negocio
├── tests/
│   └── test_local.py    ← Simular chat sin WhatsApp
├── requirements.txt
├── Dockerfile
└── .env                 ← NO va a GitHub
```

---

## Lo que falta pulir

1. **System prompt** (`config/prompts.yaml`) — ajustar según cómo responde el agente en conversaciones reales
2. **Knowledge base** — subir archivos con precios, servicios, FAQ a la carpeta `knowledge/`
3. **Cold start** — Render gratuito duerme el servidor tras 15 min. Primera respuesta tarda ~30s. Considerar plan pago si afecta clientes.
4. **Persistencia de DB** — SQLite en Render se borra con cada redeploy. Para producción real, agregar PostgreSQL en Render.

---

## Comandos útiles

```bash
# Clonar el proyecto
git clone https://github.com/Ulises-85952022/taller-la-frontera-agente.git
cd taller-la-frontera-agente

# Instalar dependencias
pip install -r requirements.txt

# Copiar variables de entorno
cp .env.example .env
# Editar .env con las claves reales

# Test local (sin WhatsApp)
python tests/test_local.py

# Arrancar servidor local
uvicorn agent.main:app --reload --port 8000
```

## Para hacer push con cambios
```bash
git add .
git commit -m "descripcion del cambio"
git push origin main
# Render redeploy automáticamente al detectar el push
```

---

## Notas técnicas
- Whapi envía mensajes a `/webhook/messages` (no a `/webhook` estándar)
- El Dockerfile usa `${PORT:-8000}` para compatibilidad con Render
- El historial de conversación se guarda por número de teléfono en SQLite
- El system prompt se carga en cada request desde `config/prompts.yaml` (sin reiniciar el servidor)
