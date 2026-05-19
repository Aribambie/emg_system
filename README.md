# EMG System

Sistema de adquisición y procesamiento de señales electromiográficas (EMG) usando el sensor BITalino.

## Estructura del proyecto

```
emg_system/
├── procesamiento_de_señales/
│   ├── filtros/
│   │   ├── pasa_banda.py       # Filtro Butterworth pasa-banda (20–450 Hz)
│   │   └── rechaza_banda.py    # Filtro Butterworth notch 60 Hz
│   ├── adquisicion/
│   ├── clasificadores/
│   └── deteccion/
├── interfaz/
├── docs/
│   ├── Configuracion_ambiente.md
│   └── README.md
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.12
- Windows 11

## Configuración del ambiente

Ver [docs/Configuracion_ambiente.md](docs/Configuracion_ambiente.md) para el paso a paso completo.

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install bitalino==1.2.6 --no-deps
pip install pyserial numpy scipy
```

## Dependencias

| Paquete | Versión | Uso |
|---|---|---|
| bitalino | 1.2.6 | Comunicación con el sensor |
| pyserial | 3.5 | Conexión al puerto COM |
| numpy | 2.4.5 | Procesamiento numérico |
| scipy | 1.17.1 | Filtros digitales |

## Uso de IA

Claude (Anthropic) se usó como apoyo para la configuración del ambiente de desarrollo: selección de versiones de dependencias, documentación del entorno virtual y manejo del repositorio.
