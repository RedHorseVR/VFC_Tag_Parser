#!/usr/bin/env python3
import subprocess
import time
import os
import curses
from datetime import datetime


def get_gpu_info():
    # """Get GPU information using nvidia-smi."""
    try:
        # Run nvidia-smi command
        result = subprocess.run(
            [
                'nvidia-smi',
                '--query-gpu=index,name,temperature.gpu,utilization.gpu,utilization.memory,memory.used,memory.total,power.draw',
                '--format=csv,noheader,nounits',
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        # Parse output
        gpus = []
        for line in result.stdout.strip().split('\n'):
            values = [val.strip() for val in line.split(',')]
            if len(values) >= 8:
                gpu = {
                    'id': values[0],
                    'name': values[1],
                    'temp': values[2],
                    'gpu_util': values[3],
                    'mem_util': values[4],
                    'mem_used': values[5],
                    'mem_total': values[6],
                    'power': values[7],
                }
                gpus.append(gpu)

        return gpus
    except subprocess.CalledProcessError as e:
        return [{'error': f"Error executing nvidia-smi: {e.stderr}"}]
    except Exception as e:
        return [{'error': f"Unexpected error: {str(e)}"}]


def draw_gpu_info(stdscr, refresh_rate=1):
    # """Draw GPU information on the screen."""
    # Set up colors
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    curses.init_pair(3, curses.COLOR_RED, -1)

    GREEN = curses.color_pair(1)
    YELLOW = curses.color_pair(2)
    RED = curses.color_pair(3)

    # Hide cursor
    curses.curs_set(0)

    try:
        while True:
            # Get window dimensions
            max_y, max_x = stdscr.getmaxyx()

            # Clear screen
            stdscr.clear()

            # Get current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Print header
            header = f"GPU Monitor for WSL - {current_time} (Press 'q' to quit)"
            stdscr.addstr(0, 0, header, curses.A_BOLD)
            stdscr.addstr(1, 0, "=" * min(len(header), max_x - 1))

            # Get GPU info
            gpus = get_gpu_info()

            row = 3
            for gpu in gpus:
                if 'error' in gpu:
                    stdscr.addstr(row, 0, f"Error: {gpu['error']}")
                    row += 1
                    continue

                # Print GPU name and ID
                stdscr.addstr(row, 0, f"GPU {gpu['id']}: {gpu['name']}", curses.A_BOLD)
                row += 1

                # Temperature with color based on value
                temp = float(gpu['temp'])
                temp_color = GREEN if temp < 70 else (YELLOW if temp < 85 else RED)
                stdscr.addstr(row, 2, f"Temperature: ", curses.A_BOLD)
                stdscr.addstr(f"{temp}°C", temp_color)
                row += 1

                # GPU Utilization with color and bar
                gpu_util = float(gpu['gpu_util'])
                gpu_util_color = GREEN if gpu_util < 50 else (YELLOW if gpu_util < 90 else RED)
                bar_width = min(50, max_x - 25)
                filled_width = int(bar_width * gpu_util / 100)

                stdscr.addstr(row, 2, f"GPU Utilization: ", curses.A_BOLD)
                stdscr.addstr(f"{gpu_util}% ", gpu_util_color)
                stdscr.addstr("[")
                stdscr.addstr("=" * filled_width, gpu_util_color)
                stdscr.addstr(" " * (bar_width - filled_width))
                stdscr.addstr("]")
                row += 1

                # Memory Usage
                mem_used = float(gpu['mem_used'])
                mem_total = float(gpu['mem_total'])
                mem_percent = (mem_used / mem_total) * 100 if mem_total > 0 else 0
                mem_color = GREEN if mem_percent < 50 else (YELLOW if mem_percent < 90 else RED)
                filled_width = int(bar_width * mem_percent / 100)

                stdscr.addstr(row, 2, f"Memory Usage: ", curses.A_BOLD)
                stdscr.addstr(f"{mem_used}/{mem_total} MB ({mem_percent:.1f}%) ", mem_color)
                stdscr.addstr("[")
                stdscr.addstr("=" * filled_width, mem_color)
                stdscr.addstr(" " * (bar_width - filled_width))
                stdscr.addstr("]")
                row += 1

                # Power Usage
                stdscr.addstr(row, 2, f"Power Usage: ", curses.A_BOLD)
                stdscr.addstr(f"{gpu['power']} W")
                row += 2

            # Instructions
            stdscr.addstr(row, 0, f"Refresh rate: {refresh_rate} second(s). Press '+' to increase, '-' to decrease.")

            # Refresh the screen
            stdscr.refresh()

            # Check for key presses
            stdscr.timeout(refresh_rate * 1000)
            key = stdscr.getch()

            # Quit on 'q'
            if key == ord('q'):
                break
            # Increase refresh rate on '+'
            elif key == ord('+') or key == ord('='):
                refresh_rate = max(0.1, refresh_rate - 0.1)
            # Decrease refresh rate on '-'
            elif key == ord('-'):
                refresh_rate = min(10, refresh_rate + 0.1)

    except KeyboardInterrupt:
        pass


def main():
    # Check if nvidia-smi is available
    try:
        subprocess.run(['nvidia-smi', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: nvidia-smi not found. Make sure NVIDIA drivers are installed correctly in WSL.")
        return

    # Run the curses application
    curses.wrapper(draw_gpu_info)


if __name__ == "__main__":
    main()
