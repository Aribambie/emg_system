import numpy as np
from scipy.signal import butter, sosfilt, sosfreqz

ORDEN      = 20    # orden del filtro
FC_LOW     = 20    # Hz — corte inferior (librería BITalino nueva)
FC_HIGH    = 450   # Hz — corte superior (librería BITalino nueva)
FC_LOW_V   = 50    # Hz — corte inferior (librería BITalino vieja)
FC_HIGH_V  = 250   # Hz — corte superior (librería BITalino vieja)
FS_DEFAULT = 1000  # Hz


def diseñar(fs=FS_DEFAULT, fc_low=FC_LOW, fc_high=FC_HIGH, orden=ORDEN):
    """Butterworth pasa-banda. Devuelve coeficientes SOS."""
    nyq = fs / 2.0
    return butter(orden, [fc_low / nyq, fc_high / nyq], btype="bandpass", output="sos")


def aplicar(sos, señal):
    """Filtra una señal completa sin memoria entre llamadas."""
    return sosfilt(sos, señal)


class PasaBandaEstadeful:
    """Filtro pasa-banda para streaming chunk a chunk.

    Mantiene zi entre llamadas para evitar el transitorio al inicio de cada chunk.
    """

    def __init__(self, fs=FS_DEFAULT, fc_low=FC_LOW, fc_high=FC_HIGH, orden=ORDEN):
        self._sos = diseñar(fs, fc_low, fc_high, orden)
        self._zi  = np.zeros((self._sos.shape[0], 2))

    def filtrar(self, señal):
        salida, self._zi = sosfilt(self._sos, señal, zi=self._zi)
        return salida

    def resetear(self):
        """Limpia el estado interno. Llamar entre sesiones."""
        self._zi = np.zeros((self._sos.shape[0], 2))


if __name__ == "__main__":
    print("Verificando pasa_banda.py...")

    sos = diseñar()
    w, h = sosfreqz(sos, worN=2048, fs=FS_DEFAULT)

    def db(freq):
        idx = np.argmin(np.abs(w - freq))
        return 20 * np.log10(np.abs(h[idx]) + 1e-12)

    print(f"  Orden:     {ORDEN}")
    print(f"  Fc_low:    {FC_LOW} Hz")
    print(f"  Fc_high:   {FC_HIGH} Hz")
    print(f"  @ 10 Hz  : {db(10):.1f} dB   (esperado < -3 dB)")
    print(f"  @ 100 Hz : {db(100):.1f} dB   (esperado ~0 dB)")
    print(f"  @ 460 Hz : {db(460):.1f} dB  (esperado < -3 dB)")

    assert db(10)  < -3,  "Falla: debería atenuar por debajo de Fc_low"
    assert db(100) > -1,  "Falla: debería pasar la banda central"
    assert db(460) < -3,  "Falla: debería atenuar por encima de Fc_high"

    print("OK pasa_banda.py verificado correctamente.")
