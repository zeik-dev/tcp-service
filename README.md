# TCP Service Daemon - Proyecto Final Sistemas Operativos

Servicio TCP daemon implementado en Python para Ubuntu Server 24.04 LTS, desarrollado como proyecto final de la asignatura Sistemas Operativos (ICC331) de PUCMM.

## 👨‍💻 Autor

**Randy A. Germosén Ureña**
- ID: 1013-4707
- Universidad: PUCMM
- Materia: Sistemas Operativos (ICC331)

### Instalación

```bash
# 1. Ejecutar el script de instalación
sudo ./install.sh
```

### ¿Qué hace?

```bash
# 1. Instalar dependencias
sudo apt update
sudo apt install -y python3 python3-pip tmux sysstat net-tools ufw

# 2. Crear usuario del servicio
sudo useradd -r -s /bin/false -d /opt/tcp_service tcpservice

# 3. Crear directorios
sudo mkdir -p /opt/tcp_service
sudo mkdir -p /etc/tcp_service
sudo mkdir -p /var/log/tcp_service

# 4. Copiar archivos
sudo cp tcp_service.py /usr/local/bin/
sudo chmod +x /usr/local/bin/tcp_service.py
sudo cp config.json /etc/tcp_service/

# 5. Configurar permisos
sudo chown -R tcpservice:tcpservice /opt/tcp_service
sudo chown -R tcpservice:tcpservice /var/log/tcp_service
sudo chown tcpservice:tcpservice /etc/tcp_service/config.json
sudo chmod 640 /etc/tcp_service/config.json

# 6. Instalar servicio systemd
sudo cp tcp-service.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tcp-service
sudo systemctl start tcp-service

# 7. Configurar firewall
sudo ufw allow 9000/tcp
sudo ufw enable
```

## Configuración

El servicio se configura mediante el archivo `/etc/tcp_service/config.json`:

```json
{
    "host": "0.0.0.0",
    "port": 9000,
    "max_connections": 5,
    "buffer_size": 1024
}
```

### Parámetros:

- **host**: Interfaz en la que escuchar (0.0.0.0 = todas)
- **port**: Puerto TCP (default: 9000)
- **max_connections**: Conexiones simultáneas máximas
- **buffer_size**: Tamaño del buffer de recepción (bytes)

## Uso

### Gestión del Servicio

```bash
# Iniciar
sudo systemctl start tcp-service

# Detener
sudo systemctl stop tcp-service

# Reiniciar
sudo systemctl restart tcp-service

# Ver estado
sudo systemctl status tcp-service

# Habilitar inicio automático
sudo systemctl enable tcp-service

# Deshabilitar inicio automático
sudo systemctl disable tcp-service
```

**Desarrollado** para mi clase de Sistemas Operativos impartida por Carlos Camacho**