import matplotlib
matplotlib.use('MacOSX')

import serial
import serial.tools.list_ports
import time
import collections
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def select_serial_port():
    print("Puertos seriales disponibles:")
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print("No se encontraron puertos seriales. Asegúrate de que tu dispositivo esté conectado.")
        return None

    for i, port in enumerate(ports):
        print(f"  {i}: {port.device} - {port.description}")

    while True:
        try:
            choice = int(input("Selecciona el número del puerto a utilizar: "))
            if 0 <= choice < len(ports):
                return ports[choice].device
            else:
                print("Selección inválida. Inténtalo de nuevo.")
        except (ValueError, IndexError):
            print("Entrada inválida. Por favor, introduce un número de la lista.")

class NunchukPlotter:
    def __init__(self, port, baud_rate, window_size=100):
        self.port = port
        self.baud_rate = baud_rate
        self.window_size = window_size
        self.ser = None
        self.sample_count = 0
        self.y_data = collections.deque(maxlen=window_size)
        self._setup_plot()

    def _setup_plot(self):
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.manager.set_window_title("Monitor de Sensores Nunchuk")
        self.fig.patch.set_facecolor('#000000')
        self.ax.set_facecolor('#101010')
        self.line, = self.ax.plot([], [], color='#00ff00', linewidth=2, label='Joystick Y')
        self.ax.set_title("Datos en Tiempo Real: Nunchuk", color='white')
        self.ax.set_ylabel("Valor Joystick Y (0-255)", color='white')
        self.ax.set_xlabel("Muestras", color='white')
        self.ax.set_ylim(0, 260)
        self.ax.grid(True, linestyle='--', alpha=0.2)
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.text_info = self.ax.text(0.02, 0.95, 'Iniciando...', transform=self.ax.transAxes, 
                                      color='white', fontsize=10, verticalalignment='top', 
                                      fontfamily='monospace',
                                      bbox=dict(boxstyle="round", facecolor='#333333', alpha=0.8))

    def _connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=0.1)
            print(f"Conectado a {self.port}. Esperando datos...")
            time.sleep(2)
            return True
        except serial.SerialException as e:
            print(f"Error al conectar: {e}")
            self.ser = None
            return False

    def _get_direction(self, jx, jy):
        direc = "CENTRO"
        if jy > 200: direc = "ARRIBA"
        elif jy < 50: direc = "ABAJO"
        if jx > 200: direc = "DERECHA" if direc == "CENTRO" else f"{direc}-DERECHA"
        elif jx < 50: direc = "IZQUIERDA" if direc == "CENTRO" else f"{direc}-IZQUIERDA"
        return direc

    def update(self, frame):
        if self.ser is None or not self.ser.is_open:
            self.text_info.set_text(f"BUSCANDO DISPOSITIVO EN {self.port}...")
            if not self._connect():
                time.sleep(1)
                return
        
        line_raw = ''
        try:
            while self.ser.in_waiting > 0:
                line_raw = self.ser.readline().decode('utf-8', errors='ignore').strip()
                
                if not line_raw:
                    continue

                parts = line_raw.split(',')
                if len(parts) == 5:
                    joy_x, joy_y, acc_x, acc_y, acc_z = map(int, parts)
                    
                    self.y_data.append(joy_y)
                    self.sample_count += 1
                    
                    x_values = range(max(0, self.sample_count - self.window_size), self.sample_count)
                    
                    visible_y_data = list(self.y_data)
                    visible_x_data = list(x_values)[-len(visible_y_data):]

                    self.line.set_data(visible_x_data, visible_y_data)
                    
                    self.ax.set_xlim(max(0, self.sample_count - self.window_size), self.sample_count + 1)

                    direction = self._get_direction(joy_x, joy_y)
                    info_text = (f"--- JOYSTICK ---\n"
                                 f"Posición X: {joy_x}\n"
                                 f"Posición Y: {joy_y}\n"
                                 f"DIRECCIÓN : {direction}\n\n"
                                 f"--- ACELERÓMETRO ---\n"
                                 f"Eje X: {acc_x}\n"
                                 f"Eje Y: {acc_y}\n"
                                 f"Eje Z: {acc_z}")
                    self.text_info.set_text(info_text)

        except (ValueError, IndexError):
            print(f"Dato inválido o incompleto recibido: '{line_raw}'")
        except serial.SerialException:
            print("Error de comunicación. Intentando reconectar...")
            if self.ser: self.ser.close()
            self.ser = None

    def start(self):
        self.ani = FuncAnimation(self.fig, self.update, interval=50, cache_frame_data=False)
        plt.show()

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Puerto serial cerrado.")

if __name__ == "__main__":
    PUERTO = select_serial_port()
    
    if PUERTO:
        BAUD_RATE = 115200
        plotter = NunchukPlotter(port=PUERTO, baud_rate=BAUD_RATE)
        
        try:
            plotter.start()
        except KeyboardInterrupt:
            print("Programa detenido por el usuario.")
        finally:
            plotter.close()
    else:
        print("No se seleccionó un puerto. Saliendo del programa.")
