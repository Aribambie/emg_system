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
    filtro_pb = PasaBandaEstadeful()
    filtro_rb = RechazaBandaEstadeful()

    try:
        with Adquisicion() as sensor:
            await ws.send_text(json.dumps({"conectado": True}))
            while True:
                chunk = sensor.leer(CHUNK)
                chunk = filtro_pb.filtrar(chunk)
                chunk = filtro_rb.filtrar(chunk)
                await ws.send_text(json.dumps({"muestras": chunk.tolist()}))
                await asyncio.sleep(0)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await ws.send_text(json.dumps({"error": str(e)}))
