#!/usr/bin/env python3
"""
Prueba del Cliente TCP para el Servicio TCP
"""

import socket
import sys
import json

def test_tcp_service(host='localhost', port=9000, message="Hola desde el cliente"):
    """Envía un mensaje al servicio TCP y recibe respuesta"""
    
    print(f"Conectando a {host}:{port}...")
    
    try:
        # Crear socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)
        
        # Conectar
        client.connect((host, port))
        print(f"✓ Conectado exitosamente")
        
        # Enviar mensaje
        client.sendall(message.encode('utf-8'))
        print(f"✓ Mensaje enviado: {message}")
        
        # Recibir respuesta
        response = client.recv(1024)
        print(f"✓ Respuesta recibida:")
        
        try:
            response_data = json.loads(response.decode('utf-8'))
            print(json.dumps(response_data, indent=2))
        except:
            print(response.decode('utf-8', errors='ignore'))
        
        client.close()
        print("✓ Conexión cerrada")
        return True
        
    except socket.timeout:
        print("✗ Error: Timeout - El servidor no respondió")
        return False
    except ConnectionRefusedError:
        print("✗ Error: Conexión rechazada - El servidor no está escuchando")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 9000
    message = sys.argv[3] if len(sys.argv) > 3 else "Test desde cliente Python"
    
    test_tcp_service(host, port, message)