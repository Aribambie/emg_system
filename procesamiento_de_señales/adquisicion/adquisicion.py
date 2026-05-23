import os
import numpy as np

MAC_DEFAULT = os.getenv("BITALINO_MAC", "XX:XX:XX:XX:XX:XX")
FS = 1000
CANAL = [0]  # A1
CHUNK = 100  # muestras por lectura


class Adquisicion:
    def __init__(self, mac=MAC_DEFAULT):
        self.mac = mac
        self._device = None

    def conectar(self):
        import bitalino
        self._device = bitalino.BITalino(self.mac)
        self._device.start(FS, CANAL)

    def leer(self, n=CHUNK):
        raw = self._device.read(n)
        return raw[:, -1] * (3.3 / 1024)

    def desconectar(self):
        if self._device:
            self._device.stop()
            self._device.close()
            self._device = None

    def __enter__(self):
        self.conectar()
        return self

    def __exit__(self, *_):
        self.desconectar()
