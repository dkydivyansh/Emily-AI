import platform
import psutil
import socket
import os
from datetime import datetime
import GPUtil
from fpdf import FPDF
import subprocess

def generate_system_info_pdf():
    # Define color variables for better readability
    bgreen = "\033[1;32m"  # Bright green
    bblue = "\033[1;34m"   # Bright blue
    reset = "\033[0m"      # Reset to default color

    # Device Name
    device_name = socket.gethostname()

    # System Info
    system = platform.system()
    system_version = platform.version()
    architecture = platform.architecture()[0]

    # Processor Info
    processor = platform.processor()
    cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 'Unknown'
    logical_cores = psutil.cpu_count(logical=True)
    physical_cores = psutil.cpu_count(logical=False)

    # RAM Info
    virtual_mem = psutil.virtual_memory()
    total_ram = virtual_mem.total / (1024 ** 3)
    available_ram = virtual_mem.available / (1024 ** 3)
    used_ram = virtual_mem.used / (1024 ** 3)

    # Swap Memory Info
    swap = psutil.swap_memory()
    total_swap = swap.total / (1024 ** 3)
    used_swap = swap.used / (1024 ** 3)
    free_swap = swap.free / (1024 ** 3)

    # Disk Info
    disk_partitions = psutil.disk_partitions()
    disk_usage = {partition.mountpoint: psutil.disk_usage(partition.mountpoint) for partition in disk_partitions}

    # Disk I/O statistics
    disk_io = psutil.disk_io_counters()

    # Network Info
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    network_interfaces = psutil.net_if_addrs()

    # Boot Time and Uptime
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    uptime_seconds = (datetime.now() - datetime.fromtimestamp(boot_time_timestamp)).total_seconds()
    uptime_hours = uptime_seconds / 3600

    # CPU Load Average (1 min, 5 min, 15 min averages)
    cpu_load = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else "Load average not available on this system"

    # Temperature Sensors (if supported)
    if hasattr(psutil, 'sensors_temperatures'):
        temperatures = psutil.sensors_temperatures()
    else:
        temperatures = None

    # Fan Speed (if supported)
    if hasattr(psutil, 'sensors_fans'):
        fans = psutil.sensors_fans()
    else:
        fans = None

    # Battery Info (if available)
    battery = psutil.sensors_battery()
    battery_info = f"{battery.percent}% {'charging' if battery.power_plugged else 'discharging'}" if battery else "No battery"

    # GPU Info (if available)
    gpus = GPUtil.getGPUs()
    gpu_info = [{"GPU Name": gpu.name, "Total Memory (MB)": gpu.memoryTotal, "Available Memory (MB)": gpu.memoryFree, 
                 "Used Memory (MB)": gpu.memoryUsed, "Temperature (C)": gpu.temperature} for gpu in gpus]

    # Running Processes
    running_processes = [{"PID": proc.info['pid'], "Name": proc.info['name'], "User": proc.info['username']} 
                         for proc in psutil.process_iter(['pid', 'name', 'username'])]

    # User Information
    users = psutil.users()

    # Environment Variables
    env_vars = os.environ

    # Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "System Information - Emily AI", 0, 1, 'C')

    # Add the gathered system information to the PDF
    pdf.set_font("Arial", 'I', 12)

    pdf.cell(0, 10, f"Device Name: {device_name}", 0, 1)
    pdf.cell(0, 10, f"System: {system} {system_version}", 0, 1)
    pdf.cell(0, 10, f"Architecture: {architecture}", 0, 1)
    pdf.cell(0, 10, f"Processor: {processor}", 0, 1)
    pdf.cell(0, 10, f"CPU Frequency: {cpu_freq:.2f} MHz", 0, 1)
    pdf.cell(0, 10, f"Logical Cores: {logical_cores}", 0, 1)
    pdf.cell(0, 10, f"Physical Cores: {physical_cores}", 0, 1)

    pdf.cell(0, 10, "", 0, 1)  # Blank line
    pdf.cell(0, 10, "RAM Info:", 0, 1)
    pdf.cell(0, 10, f"  Total RAM: {total_ram:.2f} GB", 0, 1)
    pdf.cell(0, 10, f"  Available RAM: {available_ram:.2f} GB", 0, 1)
    pdf.cell(0, 10, f"  Used RAM: {used_ram:.2f} GB", 0, 1)

    pdf.cell(0, 10, "", 0, 1)  # Blank line
    pdf.cell(0, 10, "Swap Memory Info:", 0, 1)
    pdf.cell(0, 10, f"  Total Swap: {total_swap:.2f} GB", 0, 1)
    pdf.cell(0, 10, f"  Used Swap: {used_swap:.2f} GB", 0, 1)
    pdf.cell(0, 10, f"  Free Swap: {free_swap:.2f} GB", 0, 1)

    pdf.cell(0, 10, "", 0, 1)  # Blank line
    pdf.cell(0, 10, "Disk Partitions and Usage:", 0, 1)
    for mountpoint, usage in disk_usage.items():
        pdf.cell(0, 10, f"  {mountpoint}: {usage.total / (1024 ** 3):.2f} GB total, {usage.used / (1024 ** 3):.2f} GB used, {usage.free / (1024 ** 3):.2f} GB free", 0, 1)

    pdf.cell(0, 10, "", 0, 1)  # Blank line
    pdf.cell(0, 10, "Disk I/O:", 0, 1)
    pdf.cell(0, 10, f"  Read: {disk_io.read_bytes / (1024 ** 3):.2f} GB, Written: {disk_io.write_bytes / (1024 ** 3):.2f} GB", 0, 1)

    pdf.cell(0, 10, "", 0, 1)  # Blank line
    pdf.cell(0, 10, "Network Info:", 0, 1)
    pdf.cell(0, 10, f"  Hostname: {host_name}", 0, 1)
    pdf.cell(0, 10, f"  IP Address: {ip_address}", 0, 1)
    for interface, addresses in network_interfaces.items():
        pdf.cell(0, 10, f"  Interface: {interface}", 0, 1)
        for addr in addresses:
            pdf.cell(0, 10, f"    Address: {addr.address} ({addr.family.name})", 0, 1)

    pdf.cell(0, 10, "", 0, 1)  # Blank line
    pdf.cell(0, 10, f"Boot Time: {boot_time}", 0, 1)
    pdf.cell(0, 10, f"System Uptime: {uptime_hours:.2f} hours", 0, 1)

    pdf.cell(0, 10, "", 0, 1)  # Blank line
    pdf.cell(0, 10, f"CPU Load Average (1 min, 5 min, 15 min): {cpu_load}", 0, 1)

    if temperatures:
        pdf.cell(0, 10, "Temperature Sensors:", 0, 1)
        for name, entries in temperatures.items():
            for entry in entries:
                pdf.cell(0, 10, f"  {name}: {entry.label or 'Unknown'} = {entry.current}°C", 0, 1)
    else:
        pdf.cell(0, 10, "No temperature sensors available", 0, 1)

    if fans:
        pdf.cell(0, 10, "Fan Speeds:", 0, 1)
        for name, fan in fans.items():
            pdf.cell(0, 10, f"  {name}: {fan[0]} RPM", 0, 1)
    else:
        pdf.cell(0, 10, "No fan speed sensors available", 0, 1)

    if battery:
        pdf.cell(0, 10, f"Battery Status: {battery_info}", 0, 1)
    else:
        pdf.cell(0, 10, "No battery information available", 0, 1)

    if gpus:
        pdf.cell(0, 10, "GPU Info:", 0, 1)
        for gpu in gpu_info:
            pdf.cell(0, 10, f"  {gpu['GPU Name']}: {gpu['Total Memory (MB)']} MB, Available: {gpu['Available Memory (MB)']} MB, Used: {gpu['Used Memory (MB)']} MB, Temp: {gpu['Temperature (C)']} °C", 0, 1)
    else:
        pdf.cell(0, 10, "No GPU information available", 0, 1)

    pdf.cell(0, 10, "", 0, 1)  # Blank line
    pdf.cell(0, 10, "Running Processes:", 0, 1)
    for process in running_processes:
        pdf.cell(0, 10, f"  PID: {process['PID']}, Name: {process['Name']}, User: {process['User']}", 0, 1)

    pdf.cell(0, 10, "", 0, 1)  # Blank line
    pdf.cell(0, 10, "User Information:", 0, 1)
    for user in users:
        pdf.cell(0, 10, f"  Username: {user.name}, Terminal: {user.terminal}, Host: {user.host}, Started: {user.started}", 0, 1)

    pdf.cell(0, 10, "", 0, 1)  # Blank line
    pdf.cell(0, 10, "Environment Variables:", 0, 1)
    for key, value in env_vars.items():
        pdf.cell(0, 10, f"  {key}: {value}", 0, 1)

    # Save the PDF to Desktop
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    pdf_file_path = os.path.join(desktop_path, 'System_Info.pdf')
    pdf.output(pdf_file_path)

    # Open the PDF with the default application
    subprocess.Popen([pdf_file_path], shell=True)

# Call the function to generate the PDF
