#!/bin/bash
# Script de monitoreo utilizando tmux para el servicio TCP

SESSION_NAME="so-monitoring"

# Verificación de instalación de tmux
if ! command -v tmux &> /dev/null; then
    echo "Error: tmux no está instalado"
    echo "Instalar con: sudo apt install tmux"
    exit 1
fi

# Matar sesión existente si existe
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Crear nueva sesión
tmux new-session -d -s $SESSION_NAME

# Panel 1: Logs del servicio TCP
tmux send-keys -t $SESSION_NAME "journalctl -u tcp-service -f" C-m

tmux split-window -h -t $SESSION_NAME

# Panel 2: Monitoreo de CPU y Memoria
tmux send-keys -t $SESSION_NAME "watch -n 1 'systemctl status tcp-service | head -20'" C-m

tmux select-pane -t 0
tmux split-window -v -t $SESSION_NAME

# Panel 3: Procesos y memoria
tmux send-keys -t $SESSION_NAME "watch -n 2 'ps aux | grep -E \"(tcp_service|PID)\" | head -10; echo; free -h'" C-m

tmux select-pane -t 2
tmux split-window -v -t $SESSION_NAME

# Panel 4: I/O de disco y red
tmux send-keys -t $SESSION_NAME "watch -n 2 'iostat -x 1 1; echo; ss -tuln | grep 9000'" C-m

# Seleccionar el primer panel
tmux select-pane -t 0

# Adjuntar a la sesión
tmux attach-session -t $SESSION_NAME