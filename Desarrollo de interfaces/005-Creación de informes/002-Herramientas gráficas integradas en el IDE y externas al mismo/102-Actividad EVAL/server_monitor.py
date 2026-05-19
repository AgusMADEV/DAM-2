# server_monitor.py
import psutil
import csv
from datetime import datetime, timedelta
import re
import os
from pytz import timezone  # You may need to install pytz: pip install pytz

# --- Config ---
CSV_DIR = 'monitor_data'
os.makedirs(CSV_DIR, exist_ok=True)

# --- Helper Functions ---
def save_to_csv(filename, headers, data):
    """Saves data to CSV, creating headers if the file doesn't exist."""
    filepath = os.path.join(CSV_DIR, filename)
    file_exists = os.path.isfile(filepath)
    with open(filepath, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow(data)

# --- CPU Monitoring ---
def monitor_cpu():
    cpu_usage = psutil.cpu_percent(interval=1)
    save_to_csv('cpu_usage.csv', ['date', 'cpu_usage'], [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), cpu_usage])

# --- RAM Monitoring ---
def monitor_ram():
    ram = psutil.virtual_memory()
    save_to_csv('ram_usage.csv', ['date', 'ram_usage_percent', 'ram_total_gb'],
                [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ram.percent, round(ram.total / (1024 ** 3), 2)])

# --- Disk I/O Monitoring ---
def monitor_disk_io():
    disk_io_counters = psutil.disk_io_counters(perdisk=True)  # Fixed: Added this line
    for disk, io in disk_io_counters.items():
        # busy_time no está disponible en Windows, solo lo usamos si existe
        busy_time = getattr(io, 'busy_time', 0)
        save_to_csv(f'disk_io_{disk}.csv',
                    ['date', 'read_bytes', 'write_bytes', 'read_ops', 'write_ops', 'read_time_ms', 'write_time_ms', 'busy_time_ms'],
                    [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), io.read_bytes, io.write_bytes, io.read_count, io.write_count, io.read_time, io.write_time, busy_time])

# --- Disk Usage Monitoring ---
def monitor_disk_usage():
    # En Windows, usar la unidad C: en lugar de /
    disk_usage = psutil.disk_usage('C:' if os.name == 'nt' else '/')
    save_to_csv('disk_usage.csv',
                ['date', 'disk_usage_percent', 'disk_total_gb', 'disk_free_gb'],
                [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), disk_usage.percent, round(disk_usage.total / (1024 ** 3), 2), round(disk_usage.free / (1024 ** 3), 2)])

# --- Bandwidth Monitoring ---
def monitor_bandwidth():
    net_io = psutil.net_io_counters(pernic=True)
    for iface, io in net_io.items():
        save_to_csv(f'bandwidth_{iface}.csv',
                    ['date', 'bytes_sent', 'bytes_recv', 'packets_sent', 'packets_recv'],
                    [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), io.bytes_sent, io.bytes_recv, io.packets_sent, io.packets_recv])

# --- Apache2 Request Rate Monitoring ---
def monitor_apache_request_rate():
    # En Windows con XAMPP, el log está en una ubicación diferente
    ACCESS_LOG = 'D:/xampp/apache/logs/access.log' if os.name == 'nt' else '/var/log/apache2/access.log'
    
    # Verificar si el archivo existe
    if not os.path.exists(ACCESS_LOG):
        print(f"Warning: Apache log file not found at {ACCESS_LOG}")
        return
    
    request_counts = {}
    current_time = datetime.now(timezone('UTC'))  # Make current_time timezone-aware
    time_window = timedelta(minutes=1)

    try:
        with open(ACCESS_LOG, 'r') as f:
            for line in f:
                match = re.search(r'\[([^\]]+)\]', line)
                if match:
                    timestamp_str = match.group(1)
                    timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z')  # Already timezone-aware
                    if (current_time - timestamp) <= time_window:
                        minute_key = timestamp.strftime('%Y-%m-%d %H:%M')
                        request_counts[minute_key] = request_counts.get(minute_key, 0) + 1

        for minute, count in request_counts.items():
            save_to_csv('apache_request_rate.csv', ['date', 'requests_per_minute'], [minute, count])
    except Exception as e:
        print(f"Error reading Apache log: {e}")

# --- Main ---
if __name__ == '__main__':
    monitor_cpu()
    monitor_ram()
    monitor_disk_io()
    monitor_disk_usage()
    monitor_bandwidth()
    monitor_apache_request_rate()
    print("Monitoring data saved.")

