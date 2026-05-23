import sys
import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from procesamiento_de_señales.filtros.pasa_banda import PasaBandaEstadeful
from procesamiento_de_señales.filtros.rechaza_banda import RechazaBandaEstadeful
from procesamiento_de_señales.adquisicion import Adquisicion, CHUNK

TIMEOUT_CONEXION = 6.0   # segundos máximos por intento de conexión
INTERVALO_REINTENTO = 2  # segundos entre reintentos

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/estado")
def estado():
    return {"mac": os.getenv("BITALINO_MAC", "")}


@app.websocket("/ws/emg")
async def stream_emg(ws: WebSocket):
    await ws.accept()
    loop = asyncio.get_event_loop()
    sensor = None

    # busca el sensor hasta que conecte o el cliente cierre
    while sensor is None:
        try:
            s = Adquisicion()
            await asyncio.wait_for(
                loop.run_in_executor(None, s.conectar),
                timeout=TIMEOUT_CONEXION,
            )
            sensor = s
        except Exception:
            try:
                await ws.send_text(json.dumps({"estado": "conectando"}))
            except Exception:
                return  # el cliente cerró mientras esperaba
            await asyncio.sleep(INTERVALO_REINTENTO)

    filtro_pb = PasaBandaEstadeful()
    filtro_rb = RechazaBandaEstadeful()

    try:
        await ws.send_text(json.dumps({"conectado": True}))
        while True:
            chunk = await loop.run_in_executor(None, sensor.leer, CHUNK)
            chunk = filtro_pb.filtrar(chunk)
            chunk = filtro_rb.filtrar(chunk)
            await ws.send_text(json.dumps({"muestras": chunk.tolist()}))
    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await ws.send_text(json.dumps({"error": str(e)}))
        except Exception:
            pass
    finally:
        sensor.desconectar()
