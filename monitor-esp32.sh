#!/bin/bash
# ESP32 串口长期监听脚本
# 自动保存到 /tmp/esp32_monitor_*.log

LOG_DIR="/tmp/esp32_logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/esp32_$(date +%Y%m%d_%H%M%S).log"
LATEST_LINK="$LOG_DIR/latest.log"

echo "=========================================="
echo "ESP32 串口长期监听"
echo "日志目录：$LOG_DIR"
echo "当前日志：$LOG_FILE"
echo "最新日志：$LATEST_LINK"
echo "=========================================="
echo "启动时间：$(date)"
echo ""

# 创建最新日志的软链接
ln -sf "$LOG_FILE" "$LATEST_LINK"

# 捕获 Ctrl+C 退出
trap 'echo ""; echo "监听已停止，日志保存在：$LOG_FILE"; exit 0' INT TERM

# 持续监听（无限重试）
while true; do
    socat TCP:127.0.0.1:7777 - 2>&1 | while IFS= read -r line; do
        echo "[$(date '+%H:%M:%S')] $line" >> "$LOG_FILE"

        # 高亮显示重要日志
        case "$line" in
            *"E ("*|*"Error"*|*"error"*|*"Failed"*|*"failed"*)
                echo -e "\033[31m[$(date '+%H:%M:%S')] $line\033[0m"
                ;;
            *"W ("*|*"Warning"*|*"warning"*)
                echo -e "\033[33m[$(date '+%H:%M:%S')] $line\033[0m"
                ;;
            *"OTA"*|*"http"*|*"cloud_slash"*)
                echo -e "\033[36m[$(date '+%H:%M:%S')] $line\033[0m"
                ;;
            *)
                echo "[$(date '+%H:%M:%S')] $line"
                ;;
        esac
    done

    # 连接断开后 2 秒重试
    echo "[$(date '+%H:%M:%S')] 连接断开，2 秒后重试..." >> "$LOG_FILE"
    sleep 2
done
