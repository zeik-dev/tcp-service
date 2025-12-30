#!/usr/bin/env python3
"""
TCP Service Daemon - Proyecto Final Sistemas Operativos
Estudiante: Randy A. Germosén Ureña
ID: 1013-4707
"""

import socket
import signal
import sys
import logging
import json
import os
from datetime import datetime
from pathlib import Path

# Configuración
CONFIG_FILE = "/etc/tcp_service/config.json"
LOG_FILE = "/var/log/tcp_service/service.log"
PID_FILE = "/var/run/tcp_service.pid"

class TCPServiceDaemon:
    def __init__(self):
        self.running = True
        self.server_socket = None
        self.config = self.load_config()
        self.setup_logging()
        self.setup_signal_handlers()
        
    def load_config(self):
        """Carga la configuración desde archivo JSON"""
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Configuración por defecto
            return {
                "host": "0.0.0.0",
                "port": 9000,
                "max_connections": 5,
                "buffer_size": 1024
            }
    
    def setup_logging(self):
        """Configura el sistema de logging"""
        log_dir = Path(LOG_FILE).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_FILE),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('TCPService')
    
    def setup_signal_handlers(self):
        """Configura los manejadores de señales del sistema"""
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        signal.signal(signal.SIGINT, self.handle_shutdown)
        self.logger.info("Signal handlers configurados (SIGTERM, SIGINT)")
    
    def handle_shutdown(self, signum, frame):
        """Maneja el cierre graceful del servicio"""
        signame = signal.Signals(signum).name
        self.logger.info(f"Señal {signame} recibida. Iniciando shutdown graceful...")
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception as e:
                self.logger.error(f"Error cerrando socket: {e}")
        self.cleanup()
        sys.exit(0)
    
    def cleanup(self):
        """Limpieza de recursos al cerrar"""
        try:
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
            self.logger.info("Cleanup completado")
        except Exception as e:
            self.logger.error(f"Error en cleanup: {e}")
    
    def write_pid(self):
        """Escribe el PID del proceso en archivo"""
        try:
            pid_dir = Path(PID_FILE).parent
            pid_dir.mkdir(parents=True, exist_ok=True)
            with open(PID_FILE, 'w') as f:
                f.write(str(os.getpid()))
        except Exception as e:
            self.logger.error(f"Error escribiendo PID: {e}")
    
    def handle_client(self, client_socket, address):
        """Maneja la conexión de un cliente"""
        try:
            self.logger.info(f"Nueva conexión desde {address[0]}:{address[1]}")
            
            # Recibir datos
            data = client_socket.recv(self.config['buffer_size'])
            
            if data:
                message = data.decode('utf-8', errors='ignore')
                self.logger.info(f"Datos recibidos de {address[0]}: {message[:100]}")
                
                # Respuesta al cliente
                response = {
                    "status": "success",
                    "timestamp": datetime.now().isoformat(),
                    "message": "Datos recibidos correctamente",
                    "received_bytes": len(data)
                }
                
                client_socket.sendall(json.dumps(response).encode('utf-8'))
            else:
                self.logger.warning(f"Conexión vacía desde {address[0]}")
                
        except Exception as e:
            self.logger.error(f"Error manejando cliente {address[0]}: {e}")
        finally:
            client_socket.close()
            self.logger.info(f"Conexión cerrada con {address[0]}:{address[1]}")
    
    def start(self):
        """Inicia el servicio TCP"""
        self.write_pid()
        self.logger.info("="*60)
        self.logger.info("TCP Service Daemon - Iniciando")
        self.logger.info(f"Estudiante: Randy A. Germosén Ureña - ID: 1013-4707")
        self.logger.info(f"Puerto configurado: {self.config['port']}")
        self.logger.info("="*60)
        
        try:
            # Crear socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind y Listen
            self.server_socket.bind((self.config['host'], self.config['port']))
            self.server_socket.listen(self.config['max_connections'])
            
            self.logger.info(f"Servidor escuchando en {self.config['host']}:{self.config['port']}")
            self.logger.info(f"Máximo de conexiones: {self.config['max_connections']}")
            
            while self.running:
                try:
                    self.server_socket.settimeout(1.0)
                    client_socket, address = self.server_socket.accept()
                    self.handle_client(client_socket, address)
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        self.logger.error(f"Error aceptando conexión: {e}")
                    
        except Exception as e:
            self.logger.error(f"Error fatal en el servicio: {e}")
            raise
        finally:
            self.cleanup()

def main():
    """Función principal"""
    daemon = TCPServiceDaemon()
    daemon.start()

if __name__ == "__main__":
    main()