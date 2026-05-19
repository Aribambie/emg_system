import numpy as np
from scipy.signal import butter, sosfilt, sosfreqz

ORDEN      = 20    # orden del filtro
FC1        = 58    # Hz — límite inferior de la banda rechazada
FC2        = 62    # Hz — límite superior de la banda rechazada
FS_DEFAULT = 1000  # Hz


def diseñar(fs=FS_DEFAULT, fc1=FC1, fc2=FC2, orden=ORDEN):
    """Butterworth notch 60 Hz. Devuelve coeficientes SOS."""
    nyq = fs / 2.0
    return butter(orden, [fc1 / nyq, fc2 / nyq], btype="bandstop", output="sos")


def aplicar(sos, señal):
    """Filtra una señal completa sin memoria entre llamadas."""
    return sosfilt(sos, señal)


class RechazaBandaEstadeful:
    """Filtro rechaza-banda para streaming chunk a chunk.

    Mantiene zi entre llamadas para evitar el transitorio al inicio de cada chunk.
    """

    def __init__(self, fs=FS_DEFAULT, fc1=FC1, fc2=FC2, orden=ORDEN):
        self._sos = diseñar(fs, fc1, fc2, orden)
        self._zi  = np.zeros((self._sos.shape[0], 2))

    def filtrar(self, señal):
        salida, self._zi = sosfilt(self._sos, señal, zi=self._zi)
        return salida

    def resetear(self):
        """Limpia el estado interno. Llamar entre sesiones."""
        self._zi = np.zeros((self._sos.shape[0], 2))


if __name__ == "__main__":
    print("Verificando rechaza_banda.py...")

    sos = diseñar()
    w, h = sosfreqz(sos, worN=2048, fs=FS_DEFAULT)

    def db(freq):
        idx = np.argmin(np.abs(w - freq))
        return 20 * np.log10(np.abs(h[idx]) + 1e-12)

    print(f"  Orden:  {ORDEN}")
    print(f"  Fc1:    {FC1} Hz")
    print(f"  Fc2:    {FC2} Hz")
    print(f"  @ 30 Hz  : {db(30):.1f} dB   (esperado ~0 dB)")
    print(f"  @ 60 Hz  : {db(60):.1f} dB  (esperado << -3 dB)")
    print(f"  @ 200 Hz : {db(200):.1f} dB   (esperado ~0 dB)")

    assert db(30)  > -1,   "Falla: no debería atenuar fuera de la banda"
    assert db(60)  < -100, "Falla: debería rechazar 60 Hz agresivamente"
    assert db(200) > -1,   "Falla: no debería atenuar fuera de la banda"

    print("OK rechaza_banda.py verificado correctamente.")
