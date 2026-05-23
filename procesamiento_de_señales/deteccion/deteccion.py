import numpy as np


def detectar(señal, fs=1000, win_ms=200, ruido_ms=100, ganancia=1.5):
    """Extrae la ventana de actividad muscular de la señal."""
    eta = np.abs(señal)
    m = int(ruido_ms * fs / 1000)
    umbral = ganancia * np.max(eta[:m])

    activo = eta > umbral

    # suavizado con ventana deslizante del 2.5% de muestras totales
    w = max(1, int(0.025 * len(señal)))
    suavizado = np.convolve(activo.astype(float), np.ones(w) / w, mode="same") > 0.5

    indices = np.where(suavizado)[0]
    centro = int((indices[0] + indices[-1]) / 2) if len(indices) else int(np.argmax(eta))

    n_win = int(win_ms * fs / 1000)
    inicio = max(0, centro - n_win // 2)
    fin = min(len(señal), inicio + n_win)

    return señal[inicio:fin]
