# System Monitor CLI

A real-time terminal-based system resource monitoring tool that displays CPU, memory, disk, and network usage with a clean, colorful interface.

## Features

- **Real-time Monitoring** - Live updates of system resources
- **CPU Tracking** - Overall and per-core CPU usage
- **Memory Stats** - RAM and swap usage monitoring
- **Disk Information** - Usage and I/O statistics for all partitions
- **Network Speed** - Upload/download speed tracking
- **Battery Status** - Battery level and time remaining (laptops)
- **Temperature Sensors** - Hardware temperature monitoring (if available)
- **Color-coded Bars** - Visual progress bars (green/yellow/red)
- **Top Processes** - CPU and memory intensive process tracking
- **Customizable Refresh** - Adjustable update intervals

## Installation

Install the required dependency:

```bash
pip install psutil
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Monitoring

```bash
# Default monitoring (2-second refresh)
python system_monitor.py
```

### Custom Refresh Rate

```bash
# Fast refresh (1 second)
python system_monitor.py -r 1

# Slow refresh (5 seconds)
python system_monitor.py -r 5

# Very fast (0.5 second minimum)
python system_monitor.py -r 0.5
```

### Show Top Processes

```bash
# Display top 5 processes by CPU and memory
python system_monitor.py -p

# Combine with custom refresh rate
python system_monitor.py -r 3 -p
```

### Exit Monitoring

Press `Ctrl+C` to stop monitoring and exit.

## Command-Line Options

```
optional arguments:
  -h, --help            Show help message and exit
  -r REFRESH, --refresh REFRESH
                        Refresh rate in seconds (default: 2.0)
  -p, --processes       Show top processes by CPU and memory
```

## Display Sections

### System Information
- Operating system and version
- Hostname
- Boot time and uptime
- Current time

### CPU Usage
- Overall CPU percentage
- Number of cores
- Current frequency (MHz)
- Individual core usage with progress bars

### Memory Usage
- RAM usage with progress bar
- Used, total, and available memory
- Swap memory usage (if available)

### Disk Usage
- Partition information (mount point, filesystem type)
- Used/free/total space for each partition
- Total disk read/write I/O

### Network Usage
- Total bytes sent and received
- Current upload/download speed (calculated between refreshes)

### Battery Status (Laptops)
- Charging/discharging status
- Battery percentage
- Estimated time remaining

### Temperature (If Available)
- Hardware sensor readings
- Current and maximum temperatures

### Top Processes (Optional)
- Top 5 processes by CPU usage
- Top 5 processes by memory usage
- Process ID, name, and usage percentage

## Visual Elements

### Progress Bars

Progress bars are color-coded based on usage:

- **Green** (0-50%) - Normal usage
- **Yellow** (50-80%) - Moderate usage
- **Red** (80-100%) - High usage

Example:
```
CPU: ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 32.5%
RAM: ████████████████░░░░░░░░░░░░░░░░░░░░░░░░ 62.3%
```

### Size Formatting

All byte values are displayed in human-readable format:
- B (Bytes)
- KB (Kilobytes)
- MB (Megabytes)
- GB (Gigabytes)
- TB (Terabytes)

## Platform Support

- **Linux** - Full support for all features
- **macOS** - Full support (temperature sensors may vary)
- **Windows** - Full support (temperature sensors may be limited)

## Use Cases

- **System Administration** - Monitor server resources
- **Development** - Track resource usage during testing
- **Performance Tuning** - Identify resource bottlenecks
- **Troubleshooting** - Find resource-hungry processes
- **General Monitoring** - Keep an eye on system health

## Performance Tips

1. **Refresh Rate** - Higher refresh rates (< 1s) consume more CPU
2. **Process Display** - Showing processes adds minimal overhead
3. **Long Running** - Safe to run for extended periods
4. **Background Monitoring** - Minimal impact on system performance

## Examples

### Monitor During Development
```bash
# Watch resources while running your application
python system_monitor.py -r 1 -p
```

### Server Monitoring
```bash
# Slower refresh for long-term monitoring
python system_monitor.py -r 10
```

### Quick System Check
```bash
# Fast refresh to see current state
python system_monitor.py -r 0.5
```

### Find Resource Hogs
```bash
# Show processes to identify heavy users
python system_monitor.py -p
```

## Troubleshooting

### Permission Errors
Some system information may require elevated privileges:
```bash
# Linux/macOS
sudo python system_monitor.py

# Windows (run as Administrator)
python system_monitor.py
```

### Missing Temperature Sensors
Temperature monitoring is platform and hardware dependent. If not available, this section won't be displayed.

### High CPU Usage
If the monitor itself uses too much CPU, increase the refresh rate:
```bash
python system_monitor.py -r 5
```

## Technical Details

### Dependencies
- **psutil** (v5.9.0+) - Cross-platform library for system and process utilities

### Resource Collection
- CPU data collected via `psutil.cpu_percent()`
- Memory via `psutil.virtual_memory()`
- Disk via `psutil.disk_usage()` and `psutil.disk_io_counters()`
- Network via `psutil.net_io_counters()`
- Processes via `psutil.process_iter()`

### Update Mechanism
The monitor clears the screen and redraws all information at each refresh interval using ANSI escape codes for smooth updates.

## Requirements

- Python 3.6 or higher
- psutil library

## License

This script is part of the Daily Python Scripts collection and is licensed under the MIT License. See the [LICENSE](../LICENSE) file in the root directory for details.
