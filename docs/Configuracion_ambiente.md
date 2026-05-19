# Configuración del ambiente de desarrollo

## ¿Qué es un entorno virtual y por qué se usa?

Un entorno virtual (`venv`) es una instalación de Python aislada para un proyecto específico. En lugar de instalar las librerías directamente en el sistema operativo, se instalan dentro de una carpeta del proyecto.

**Sin entorno virtual**, si instalas `numpy 2.x` para este proyecto y otro proyecto necesita `numpy 1.x`, se pisan y uno deja de funcionar.

**Con entorno virtual**, cada proyecto tiene sus propias versiones independientes. El resto de la máquina no se ve afectado.

Además, el entorno virtual no se comparte ni se sube a GitHub. En cambio, el archivo `requirements.txt` funciona como la "receta": cualquier persona puede recrear el entorno idéntico desde cero en su propia máquina.

---

## ¿Por qué Python 3.12?

### Por qué no Python 3.10 (versión de soporte oficial de bitalino)

`bitalino 1.2.6` declara soporte oficial hasta Python 3.10, pero esa versión fue lanzada en octubre de 2021 y su fin de vida es en octubre de 2026. Usar 3.10 implicaría quedarse con una versión envejecida cuando Python 3.12 ya está disponible, es más rápido, más seguro y tiene mejor soporte de `numpy` y `scipy`.

`bitalino` es una librería escrita en Python puro (sin extensiones compiladas en C), por lo que funciona correctamente en Python 3.12 a pesar de no estar listada oficialmente. Se instala con `--no-deps` para evitar que sus dependencias anticuadas generen conflictos.

### Por qué no Python 3.13 o 3.14

`bitalino 1.2.6` fue lanzada en marzo de 2022 y no ha tenido actualizaciones desde entonces. No existe ninguna confirmación de compatibilidad con Python 3.13 o 3.14. Migrar a esas versiones introduciría un riesgo sin beneficio real para este proyecto.

Python 3.12 tiene soporte oficial hasta octubre de 2028, lo que lo hace una elección estable y sin urgencia de actualización.

**Resumen:**

| Versión | Motivo para no usarla |
|---|---|
| 3.10 | Demasiado antigua, fin de vida cercano |
| 3.11 | 3.12 es mejor opción en todos los aspectos |
| **3.12** | **Versión elegida — estable, soportada hasta 2028, confirmada funcional** |
| 3.13 | Sin confirmación de compatibilidad con bitalino |
| 3.14 | Demasiado nueva, alto riesgo con bitalino |

---

## Paso a paso para generar el entorno

### Requisitos previos

- Tener instalado **Python 3.12** desde [python.org](https://www.python.org/downloads/)
- Estar en la carpeta raíz del proyecto: `emg_system/`

### 1. Crear el entorno virtual

```powershell
python -m venv venv
```

Esto genera la carpeta `venv/` con la siguiente estructura:

```
venv/
├── Scripts/        ← Python, pip y scripts de activación
├── Lib/            ← Librerías instaladas (numpy, scipy, etc.)
├── Include/        ← Archivos para compilar extensiones en C
└── pyvenv.cfg      ← Versión de Python que usa el entorno
```

Esta carpeta no se edita a mano. Se genera automáticamente y se puede borrar y recrear en cualquier momento.

### 2. Activar el entorno

```powershell
.\venv\Scripts\activate
```

Cuando el entorno está activo, el prompt del terminal muestra `(venv)` al inicio. A partir de ese momento, cualquier comando `pip install` instala dentro del entorno y no en el sistema.

### 3. Instalar las librerías del proyecto

```powershell
pip install bitalino==1.2.6 --no-deps
pip install pyserial numpy scipy
```

El flag `--no-deps` en bitalino es obligatorio: sin él, pip intenta instalar dependencias de bitalino que son incompatibles con Python 3.12 y rompen la instalación.

### 4. Verificar que todo quedó instalado

```powershell
pip list
```

Debe mostrar:

```
bitalino   1.2.6
numpy      2.4.5
pyserial   3.5
scipy      1.17.1
pip        26.1.1
```

### 5. Desactivar el entorno al terminar

```powershell
deactivate
```

---

## Qué contiene el entorno una vez instalado

| Paquete | Versión | Para qué sirve |
|---|---|---|
| `bitalino` | 1.2.6 | Comunicación con el sensor BITalino vía Bluetooth o USB |
| `pyserial` | 3.5 | Conexión al puerto COM de Windows (requerido por bitalino) |
| `numpy` | 2.4.5 | Manejo de arreglos y operaciones matemáticas sobre la señal EMG |
| `scipy` | 1.17.1 | Filtros digitales y procesamiento de señales |

---

## Cómo recrear el entorno desde cero

Si el entorno se daña o se quiere reconstruir en otra máquina:

```powershell
# 1. Borrar el entorno actual (opcional, solo si ya existe)
Remove-Item -Recurse -Force venv

# 2. Crear el entorno nuevo
python -m venv venv

# 3. Activar
.\venv\Scripts\activate

# 4. Instalar todo
pip install bitalino==1.2.6 --no-deps
pip install pyserial numpy scipy
```

> La carpeta `venv/` nunca se sube a GitHub. El archivo `requirements.txt` es el que se comparte.
