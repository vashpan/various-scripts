#!/usr/bin/env python3

import platform
import psutil
import argparse
import subprocess
import json
import csv

from datetime import datetime

def get_system_info():
    # Get model
    model = subprocess.check_output(['sysctl', '-n', 'hw.model']).decode().strip()

    # Get CPU info
    cpu_count = psutil.cpu_count(logical=False)
    cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 'Unknown'

    # Get RAM info
    ram_bytes = psutil.virtual_memory().total
    ram_gb = ram_bytes / (1024 ** 3)

    system_info = {
        'Model': model,
        'CPU Cores': cpu_count,
        'CPU Clock (MHz)': cpu_freq,
        'RAM (GB)': round(ram_gb, 2)
    }

    return system_info

def get_os_info():
    # Get macOS version
    mac_ver = platform.mac_ver()[0]
    os_name = 'macOS ' + mac_ver

    # Get uptime
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time_timestamp)
    uptime = datetime.now() - boot_time

    # Get current date/time of script run
    date_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    os_info = {
        'Date': date_string,
        'System': os_name,
        'Uptime': str(uptime).split('.')[0]  # Remove microseconds
    }

    return os_info

def get_system_stats():
    # Number of processes & threads
    num_processes = len(psutil.pids())
    total_threads = sum(proc.num_threads() for proc in psutil.process_iter(attrs=['num_threads']))

    processes_stats = {
        'Number of Processes': num_processes,
        'Total Threads': total_threads,
    }

    # Memory statistics
    virtual_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()

    memory_stats = {
        'Total Memory (GB)': round(virtual_mem.total / (1024 ** 3), 2),
        'Available Memory (GB)': round(virtual_mem.available / (1024 ** 3), 2),
        'Used Memory (GB)': round(virtual_mem.used / (1024 ** 3), 2),
        'Memory Usage (%)': virtual_mem.percent,
        'Total Swap (GB)': round(swap_mem.total / (1024 ** 3), 2),
        'Used Swap (GB)': round(swap_mem.used / (1024 ** 3), 2),
        'Swap Usage (%)': swap_mem.percent
    }

    # Disk space statistics
    disk_usage = psutil.disk_usage('/')
    disk_stats = {
        'Total Disk Space (GB)': round(disk_usage.total / (1024 ** 3), 2),
        'Used Disk Space (GB)': round(disk_usage.used / (1024 ** 3), 2),
        'Free Disk Space (GB)': round(disk_usage.free / (1024 ** 3), 2),
        'Disk Usage (%)': disk_usage.percent
    }

    stats = {
        'Processes Stats': processes_stats,
        'Memory Stats': memory_stats,
        'Disk Stats': disk_stats
    }

    return stats

def get_process_info():
    process_list = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info', 'num_threads']):
        try:
            pinfo = proc.info
            process_list.append({
                'Name': pinfo['name'],
                'Memory (MB)': round(pinfo['memory_info'].rss / (1024 ** 2), 2),
                'Threads': pinfo['num_threads']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    sorted_process_list = sorted(process_list, key=lambda x: x['Name'])

    return sorted_process_list

def save_to_files(process_list, system_info, os_info, stats):
    # Save to text file
    with open('process_info.txt', 'w') as txt_file:
        txt_file.write('System Information:\n')
        for key, value in system_info.items():
            txt_file.write(f'{key}: {value}\n')
        txt_file.write('\nOS Information:\n')
        for key, value in os_info.items():
            txt_file.write(f'{key}: {value}\n')
        txt_file.write('\nSystem Statistics:\n')
        for key, value in stats.items():
            if isinstance(value, dict):
                txt_file.write(f'{key}:\n')
                for subkey, subvalue in value.items():
                    txt_file.write(f'  {subkey}: {subvalue}\n')
            else:
                txt_file.write(f'{key}: {value}\n')
        txt_file.write('\nProcess List:\n')
        for proc in process_list:
            txt_file.write(f"Name: {proc['Name']}, "
                           f"Memory (MB): {proc['Memory (MB)']}, Threads: {proc['Threads']}\n")

    # Save to CSV file
    with open('process_info.csv', 'w', newline='') as csv_file:
        fieldnames = ['Name', 'Memory (MB)', 'Threads']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for proc in process_list:
            writer.writerow(proc)

    # Save to JSON file
    with open('process_info.json', 'w') as json_file:
        json.dump({
            'system_information': system_info,
            'os_information': os_info,
            'system_statistics': stats,
            'process_list': process_list
        }, json_file, indent=4)

def main():
    parser = argparse.ArgumentParser(description='System Information Script for macOS')
    parser.add_argument('--save-to-files', action='store_true',
                        help='Save detailed information to text, CSV, and JSON files')
    args = parser.parse_args()

    system_info = get_system_info()
    os_info = get_os_info()
    stats = get_system_stats()
    process_list = get_process_info()

    # Print information to screen
    print('\nSystem Information:')
    for key, value in system_info.items():
        print(f'{key}: {value}')

    print('\n\nOS Information:')
    for key, value in os_info.items():
        print(f'{key}: {value}')

    print('\n\nSystem Statistics:')
    for key, value in stats.items():
        print()
        if isinstance(value, dict):
            print(f'{key}:')
            for subkey, subvalue in value.items():
                print(f'  {subkey}: {subvalue}')
        else:
            print(f'{key}: {value}')

    if args.save_to_files:
        save_to_files(process_list, system_info, os_info, stats)
        print('\nDetailed information saved to process_info.txt, process_info.csv, and process_info.json')

if __name__ == '__main__':
    main()