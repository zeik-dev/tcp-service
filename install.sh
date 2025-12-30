#!/bin/bash
# Script de instalación
# Proyecto Final - Sistemas Operativos
# Estudiante: Randy A. Germosén Ureña (1013-4707)

set -e  # Salir en caso de error

echo "=============================================="
echo "Instalación TCP Service"
echo "Autor: Randy A. Germosén"
echo "=============================================="

# Verificar que se ejecuta como root
if [ "$EUID" -ne 0 ]; then 
    echo "Error: Este script debe ejecutarse como root"
    echo "Usar: sudo $0"
    exit 1
fi

echo ""
echo "[1/10] Actualizando sistema..."
apt update -qq

echo "[2/10] Instalando dependencias..."
apt install -y python3 python3-pip tmux sysstat net-tools ufw > /dev/null

echo "[3/10] Creando usuario y grupo del servicio..."
if ! id -u tcpservice > /dev/null 2>&1; then
    useradd -r -s /bin/false -d /opt/tcp_service tcpservice
    echo "   ✓ Usuario 'tcpservice' creado"
else
    echo "   ✓ Usuario 'tcpservice' ya existe"
fi

echo "[4/10] Creando estructura de directorios..."
mkdir -p /opt/tcp_service
mkdir -p /etc/tcp_service
mkdir -p /var/log/tcp_service
mkdir -p /usr/local/bin

echo "[5/10] Copiando archivos del servicio..."
cp tcp_service.py /usr/local/bin/
chmod +x /usr/local/bin/tcp_service.py
cp config.json /etc/tcp_service/

echo "[6/10] Configurando permisos..."
chown -R tcpservice:tcpservice /opt/tcp_service
chown -R tcpservice:tcpservice /var/log/tcp_service
chown tcpservice:tcpservice /etc/tcp_service/config.json
chmod 640 /etc/tcp_service/config.json

echo "[7/10] Instalando servicio systemd..."
cp tcp-service.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable tcp-service

echo "[8/10] Configurando firewall UFW..."
ufw allow 9000/tcp comment 'TCP Service Daemon'
ufw --force enable
ufw status numbered

echo "[9/10] Iniciando servicio..."
systemctl start tcp-service
sleep 2
systemctl status tcp-service --no-pager

echo "[10/10] Verificando servicio..."
if systemctl is-active --quiet tcp-service; then
    echo "   ✓ Servicio activo y funcionando"
else
    echo "   ✗ Error: El servicio no está activo"
    journalctl -u tcp-service -n 20 --no-pager
    exit 1
fi

echo ""
echo "=============================================="
echo "Instalación completada exitosamente"
echo "=============================================="
echo ""
echo "Comandos útiles:"
echo "  - Ver estado:    sudo systemctl status tcp-service"
echo "  - Ver logs:      sudo journalctl -u tcp-service -f"
echo "  - Reiniciar:     sudo systemctl restart tcp-service"
echo "  - Detener:       sudo systemctl stop tcp-service"
echo "  - Probar:        ./test_client.py --host <IP> --port 9000 --message 'Hola TCP Service'"
echo "  - Prueba de Carga:        ./load_test.py"
echo "  - Monitorear:    ./monitoring.sh"
echo ""