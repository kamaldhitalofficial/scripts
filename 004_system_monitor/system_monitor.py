#!/usr/bin/env python3
"""
System Monitor CLI - Real-time system resource monitoring
Displays CPU, memory, disk, and network usage in a clean terminal interface.
"""

import psutil
import time
import sys
import platform
from datetime import datetime, timedelta

class SystemMonitor:
    """Monitor and display system resources."""
    
    def __init__(self):
        self.platform = platform.system()
        self.boot_time = datetime.fromtimestamp(psutil.boot_time())
        
    def clear_screen(self):
        """Clear terminal screen."""
        print('\033[2J\033[H', end='')
    
    def format_bytes(self, bytes_val):
        """Convert bytes to human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} PB"
    
    def get_progress_bar(self, percentage, width=20):
        """Create a text-based progress bar."""
        filled = int(width * percentage / 100)
        bar = '█' * filled + '░' * (width - filled)
        
        # Color coding
        if percentage < 50:
            color = '\033[92m'  # Green
        elif percentage < 80:
            color = '\033[93m'  # Yellow
        else:
            color = '\033[91m'  # Red
        
        reset = '\033[0m'
        return f"{color}{bar}{reset} {percentage:.1f}%"
    
    def get_cpu_info(self):
        """Get CPU usage information."""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        per_cpu = psutil.cpu_percent(interval=0.1, percpu=True)
        
        info = {
            'overall': cpu_percent,
            'count': cpu_count,
            'frequency': cpu_freq.current if cpu_freq else 0,
            'per_cpu': per_cpu
        }
        return info
    
    def get_memory_info(self):
        """Get memory usage information."""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        info = {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent,
            'swap_total': swap.total,
            'swap_used': swap.used,
            'swap_percent': swap.percent
        }
        return info
    
    def get_disk_info(self):
        """Get disk usage information."""
        partitions = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
            except PermissionError:
                continue
        
        # Disk I/O
        io = psutil.disk_io_counters()
        io_info = {
            'read_bytes': io.read_bytes if io else 0,
            'write_bytes': io.write_bytes if io else 0
        }
        
        return partitions, io_info
    
    def get_network_info(self):
        """Get network usage information."""
        io = psutil.net_io_counters()
        
        info = {
            'bytes_sent': io.bytes_sent,
            'bytes_recv': io.bytes_recv,
            'packets_sent': io.packets_sent,
            'packets_recv': io.packets_recv
        }
        return info
    
    def get_battery_info(self):
        """Get battery information (if available)."""
        if not hasattr(psutil, "sensors_battery"):
            return None
        
        battery = psutil.sensors_battery()
        if battery is None:
            return None
        
        info = {
            'percent': battery.percent,
            'plugged': battery.power_plugged,
            'time_left': battery.secsleft
        }
        return info
    
    def get_temperature_info(self):
        """Get temperature information (if available)."""
        if not hasattr(psutil, "sensors_temperatures"):
            return None
        
        temps = psutil.sensors_temperatures()
        if not temps:
            return None
        
        # Get the first available temperature sensor
        for name, entries in temps.items():
            if entries:
                return {
                    'name': name,
                    'current': entries[0].current,
                    'high': entries[0].high if entries[0].high else None
                }
        return None
    
    def get_uptime(self):
        """Get system uptime."""
        uptime = datetime.now() - self.boot_time
        return uptime
    
    def get_top_processes(self, limit=5):
        """Get top processes by CPU and memory usage."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU
        cpu_top = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:limit]
        # Sort by Memory
        mem_top = sorted(processes, key=lambda x: x['memory_percent'] or 0, reverse=True)[:limit]
        
        return cpu_top, mem_top
    
    def display_header(self):
        """Display header with system info."""
        print("=" * 80)
        print(f"{'SYSTEM MONITOR':^80}")
        print("=" * 80)
        print(f"System: {platform.system()} {platform.release()}")
        print(f"Hostname: {platform.node()}")
        print(f"Boot Time: {self.boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Uptime: {self.get_uptime()}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
    
    def display_cpu(self, cpu_info):
        """Display CPU information."""
        print(f"\n{'CPU USAGE':^80}")
        print("-" * 80)
        print(f"Overall: {self.get_progress_bar(cpu_info['overall'], 40)}")
        print(f"Cores: {cpu_info['count']} | Frequency: {cpu_info['frequency']:.0f} MHz")
        
        # Per-core usage
        print("\nPer-Core Usage:")
        for i, percent in enumerate(cpu_info['per_cpu']):
            print(f"  Core {i}: {self.get_progress_bar(percent, 30)}")
    
    def display_memory(self, mem_info):
        """Display memory information."""
        print(f"\n{'MEMORY USAGE':^80}")
        print("-" * 80)
        print(f"RAM: {self.get_progress_bar(mem_info['percent'], 40)}")
        print(f"     Used: {self.format_bytes(mem_info['used'])} / {self.format_bytes(mem_info['total'])}")
        print(f"     Available: {self.format_bytes(mem_info['available'])}")
        
        if mem_info['swap_total'] > 0:
            print(f"\nSwap: {self.get_progress_bar(mem_info['swap_percent'], 40)}")
            print(f"      Used: {self.format_bytes(mem_info['swap_used'])} / {self.format_bytes(mem_info['swap_total'])}")
    
    def display_disk(self, partitions, io_info):
        """Display disk information."""
        print(f"\n{'DISK USAGE':^80}")
        print("-" * 80)
        
        for partition in partitions[:3]:  # Show first 3 partitions
            print(f"\n{partition['mountpoint']} ({partition['fstype']})")
            print(f"  {self.get_progress_bar(partition['percent'], 40)}")
            print(f"  Used: {self.format_bytes(partition['used'])} / {self.format_bytes(partition['total'])}")
            print(f"  Free: {self.format_bytes(partition['free'])}")
        
        print(f"\nDisk I/O:")
        print(f"  Read: {self.format_bytes(io_info['read_bytes'])}")
        print(f"  Write: {self.format_bytes(io_info['write_bytes'])}")
    
    def display_network(self, net_info, prev_net_info=None):
        """Display network information."""
        print(f"\n{'NETWORK USAGE':^80}")
        print("-" * 80)
        print(f"Total Sent: {self.format_bytes(net_info['bytes_sent'])}")
        print(f"Total Received: {self.format_bytes(net_info['bytes_recv'])}")
        
        if prev_net_info:
            sent_speed = net_info['bytes_sent'] - prev_net_info['bytes_sent']
            recv_speed = net_info['bytes_recv'] - prev_net_info['bytes_recv']
            print(f"\nCurrent Speed:")
            print(f"  Upload: {self.format_bytes(sent_speed)}/s")
            print(f"  Download: {self.format_bytes(recv_speed)}/s")
    
    def display_battery(self, battery_info):
        """Display battery information."""
        if not battery_info:
            return
        
        print(f"\n{'BATTERY':^80}")
        print("-" * 80)
        
        status = "Charging" if battery_info['plugged'] else "Discharging"
        print(f"Status: {status}")
        print(f"Level: {self.get_progress_bar(battery_info['percent'], 40)}")
        
        if not battery_info['plugged'] and battery_info['time_left'] != psutil.POWER_TIME_UNLIMITED:
            time_left = timedelta(seconds=battery_info['time_left'])
            print(f"Time Remaining: {time_left}")
    
    def display_temperature(self, temp_info):
        """Display temperature information."""
        if not temp_info:
            return
        
        print(f"\n{'TEMPERATURE':^80}")
        print("-" * 80)
        print(f"Sensor: {temp_info['name']}")
        print(f"Current: {temp_info['current']:.1f}°C")
        if temp_info['high']:
            print(f"High: {temp_info['high']:.1f}°C")
    
    def display_processes(self, cpu_top, mem_top):
        """Display top processes."""
        print(f"\n{'TOP PROCESSES':^80}")
        print("-" * 80)
        
        print("\nTop 5 by CPU:")
        print(f"{'PID':<8} {'Name':<25} {'CPU %':<10}")
        print("-" * 45)
        for proc in cpu_top:
            print(f"{proc['pid']:<8} {proc['name'][:24]:<25} {proc['cpu_percent']:.1f}%")
        
        print("\nTop 5 by Memory:")
        print(f"{'PID':<8} {'Name':<25} {'Memory %':<10}")
        print("-" * 45)
        for proc in mem_top:
            print(f"{proc['pid']:<8} {proc['name'][:24]:<25} {proc['memory_percent']:.1f}%")
    
    def monitor(self, refresh_rate=2, show_processes=False):
        """Main monitoring loop."""
        prev_net_info = None
        
        try:
            while True:
                self.clear_screen()
                
                # Collect data
                cpu_info = self.get_cpu_info()
                mem_info = self.get_memory_info()
                partitions, io_info = self.get_disk_info()
                net_info = self.get_network_info()
                battery_info = self.get_battery_info()
                temp_info = self.get_temperature_info()
                
                # Display
                self.display_header()
                self.display_cpu(cpu_info)
                self.display_memory(mem_info)
                self.display_disk(partitions, io_info)
                self.display_network(net_info, prev_net_info)
                self.display_battery(battery_info)
                self.display_temperature(temp_info)
                
                if show_processes:
                    cpu_top, mem_top = self.get_top_processes()
                    self.display_processes(cpu_top, mem_top)
                
                print("\n" + "=" * 80)
                print(f"Press Ctrl+C to exit | Refresh rate: {refresh_rate}s")
                
                prev_net_info = net_info
                time.sleep(refresh_rate)
                
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")
            sys.exit(0)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Real-time system resource monitoring',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python system_monitor.py                    # Default monitoring
  python system_monitor.py -r 1               # Refresh every 1 second
  python system_monitor.py -p                 # Show top processes
  python system_monitor.py -r 5 -p            # 5s refresh with processes
        """
    )
    
    parser.add_argument(
        '-r', '--refresh',
        type=float,
        default=2.0,
        help='Refresh rate in seconds (default: 2.0)'
    )
    
    parser.add_argument(
        '-p', '--processes',
        action='store_true',
        help='Show top processes by CPU and memory'
    )
    
    args = parser.parse_args()
    
    if args.refresh < 0.5:
        print("Warning: Refresh rate below 0.5s may cause high CPU usage")
    
    monitor = SystemMonitor()
    monitor.monitor(refresh_rate=args.refresh, show_processes=args.processes)

if __name__ == '__main__':
    main()
