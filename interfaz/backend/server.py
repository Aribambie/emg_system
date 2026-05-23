import sys
import asyncio
import json
from pathlib import Path

import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from procesamiento_de_señales.filtros.pasa_banda import PasaBandaEstadeful
from procesamiento_de_señales.filtros.rechaza_banda import RechazaBandaEstadeful
from procesamiento_de_señales.adquisicion import Adquisicion, FS, CHUNK

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SIMULACION = True  # cambiar a False con el sensor conectado


@app.get("/estado")
def estado():
    return {"simulacion": SIMULACION}


def _simular_chunk(t: float, n: int) -> np.ndarray:
    tiempo = np.arange(n) / FS + t
    ruido = np.random.randn(n) * 0.02
    # contracción simulada cada 4 segundos, dura ~1s
    contraccion = np.sin(2 * np.pi * 120 * tiempo) * 0.25 * (np.sin(2 * np.pi * 0.25 * tiempo) > 0.6)
    return ruido + contraccion


@app.websocket("/ws/emg")
async def stream_emg(ws: WebSocket):
    await ws.accept()
    filtro_pb = PasaBandaEstadeful()
    filtro_rb = RechazaBandaEstadeful()
    t = 0.0

    try:
        if SIMULACION:
            while True:
                chunk = _simular_chunk(t, CHUNK)
                chunk = filtro_pb.filtrar(chunk)
                chunk = filtro_rb.filtrar(chunk)
                await ws.send_text(json.dumps({"muestras": chunk.tolist()}))
                t += CHUNK / FS
                await asyncio.sleep(CHUNK / FS)
        else:
            with Adquisicion() as sensor:
                while True:
                    chunk = sensor.leer(CHUNK)
                    chunk = filtro_pb.filtrar(chunk)
                    chunk = filtro_rb.filtrar(chunk)
                    await ws.send_text(json.dumps({"muestras": chunk.tolist()}))
                    await asyncio.sleep(0)
    except WebSocketDisconnect:
        pass
