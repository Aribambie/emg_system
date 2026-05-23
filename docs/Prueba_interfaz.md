# Prueba de la interfaz de señal EMG

Guía para levantar el backend y el frontend y ver la señal en el navegador.

---

## Requisitos previos

- Python 3.12 con el entorno virtual ya creado (ver [Configuracion_ambiente.md](Configuracion_ambiente.md))
- Node.js 22+ y npm 10+ — ya instalados en esta máquina

---

## Paso 1 — Instalar dependencias del backend

Abre una terminal en la raíz del proyecto (`emg_system/`) y activa el entorno:

```powershell
.\venv\Scripts\activate
```

Instala los paquetes nuevos del backend:

```powershell
pip install fastapi[standard] python-dotenv
```

---

## Paso 2 — Instalar dependencias del frontend

En la misma terminal o en una nueva (sin necesidad de activar el venv):

```powershell
cd interfaz/frontend
npm install
```

Esto descarga Vue, Chart.js y Vite en `interfaz/frontend/node_modules/`.

---

## Paso 3 — Levantar el backend

Vuelve a la raíz del proyecto y corre el servidor:

```powershell
cd c:\Users\Winar\OneDrive\Documentos\emg_system
.\venv\Scripts\activate
uvicorn interfaz.backend.server:app --reload
```

Si todo está bien verás:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

Deja esta terminal abierta.

---

## Paso 4 — Levantar el frontend

Abre una **segunda terminal**, sin cerrar la del backend:

```powershell
cd c:\Users\Winar\OneDrive\Documentos\emg_system\interfaz\frontend
npm run dev
```

Verás algo como:

```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

---

## Paso 5 — Ver la señal

1. Abre el navegador en **http://localhost:5173**
2. Presiona **Iniciar**
3. Deberías ver la señal EMG moviéndose en tiempo real

> Por ahora corre en **modo simulación** — genera ruido con contracciones periódicas cada ~4 segundos para simular actividad muscular real.

---

## Activar el sensor BITalino real

Cuando tengas el sensor conectado:

**1.** Pon la MAC address del dispositivo en el archivo `.env` de la raíz:

```
BITALINO_MAC=XX:XX:XX:XX:XX:XX
```

Reemplaza `XX:XX:XX:XX:XX:XX` con la dirección real (la encuentras en la etiqueta del sensor o en el Bluetooth de Windows).

**2.** En [interfaz/backend/server.py](../interfaz/backend/server.py), cambia la línea 16:

```python
SIMULACION = False
```

**3.** Reinicia el backend (Ctrl+C y vuelve a correr el uvicorn).

---

## Solución de problemas comunes

| Problema | Causa probable | Solución |
|---|---|---|
| `uvicorn: command not found` | Venv no activado | Correr `.\venv\Scripts\activate` primero |
| `Cannot connect to WebSocket` | Backend no está corriendo | Verificar que el uvicorn esté activo en el puerto 8000 |
| La gráfica no aparece | Error en el frontend | Revisar la consola del navegador (F12) |
| `ModuleNotFoundError: fastapi` | Dependencias no instaladas | Correr `pip install fastapi[standard]` con el venv activo |
