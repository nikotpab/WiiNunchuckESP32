#  Transmisión Serial Arduino → Python

### Lectura de Sensor I2C y Visualización en Tiempo Real

Este proyecto implementa un sistema de **adquisición y transmisión de datos** entre una **placa Arduino** y un **computador**, utilizando comunicación serial y un sensor conectado mediante protocolo **I2C**.
En el computador, un script en Python recibe y procesa los datos enviados, permitiendo su visualización o análisis.

---

## 📌 Características principales

* Lectura de datos desde un sensor I2C conectado a los pines **A4 (SDA)** y **A5 (SCL)**.
* Transmisión continua de los valores al computador mediante **puerto serial USB**.
* Script en Python para:

  * Recibir datos por serial
  * Procesarlos
  * Mostrar o graficar la información en tiempo real
* Compatible con Arduino Uno y tarjetas equivalentes.

---

## Conexiones del Sensor

### Distribución de pines del módulo

![sensor](/mnt/data/acbfdf44-8701-4d82-9f4e-017cca56b65b.png)

### Conexión al Arduino

![arduino diagram](/mnt/data/Screenshot 2025-11-19 at 11.19.01.png)

### Tabla de conexión

| Pin del Sensor | Función                  | Pin en Arduino |
| -------------- | ------------------------ | -------------- |
| **Vcc (+)**    | Alimentación 3.3V        | 3V3            |
| **Gnd (-)**    | Tierra                   | GND            |
| **Data (d)**   | SDA – Línea de datos I2C | A4             |
| **Clock (c)**  | SCL – Línea de reloj I2C | A5             |

---

## Requisitos

### Hardware

* Arduino Uno / Nano / similar
* Módulo sensor I2C
* Cable USB
* PC con Python instalado

### Software

* Arduino IDE
* Python 3
* Librerías Python:

  ```bash
  pip install pyserial matplotlib
  ```

---

### 1. **Subir el código Arduino**

Carga el archivo:

```
PFSDYAC_ARDUINO.ino
```

desde el Arduino IDE y súbelo a la PCB.

### 2. **Configurar el puerto serial en Python**

En `PFSDYAC.py`, ajusta el puerto:

```python
ser = serial.Serial("COM3", 9600)  # En Windows
# ó
ser = serial.Serial("/dev/ttyUSB0", 9600)  # En Linux/Mac
```

### 3. **Ejecutar el programa de lectura**

```bash
python3 PFSDYAC.py
```

### 4. **Visualización**

El script mostrará los valores recibidos y los graficará en tiempo real.

NOTA: El código PFSDYAC.py solo funciona para > macOS 26, para cambiar esto se elimina la línea #2: matplotlib.use('MacOSX')

---
### 5. **Informe**
https://drive.google.com/file/d/1FRfjRMWILw5i6jN1gp3tDIyG_3jYnGjO/view?usp=sharing
