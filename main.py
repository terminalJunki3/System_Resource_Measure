import psutil
import csv

def write_header(file_path, headers, test_name):
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        headers.append(test_name)
        writer.writerow(headers)


def calculate_memory_usage(memory_info, total_memory):
    return round((memory_info / (1024 * 1024)) / total_memory * 100, 2)


def collect_process_info(process, test_name):
    cpu_percent = process.cpu_percent(interval=0.1)
    virtual_memory_percent = calculate_memory_usage(process.memory_info().vms, psutil.virtual_memory().total)
    physical_memory_percent = calculate_memory_usage(process.memory_info().rss, psutil.virtual_memory().available)
    disk_io_read = round(psutil.disk_io_counters().read_bytes / (1024 * 1024), 2)
    disk_io_write = round(psutil.disk_io_counters().write_bytes / (1024 * 1024), 2)
    row = [cpu_percent, virtual_memory_percent, physical_memory_percent, disk_io_read, disk_io_write, test_name]
    return row


def write_data(file_path, data):
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)


def main():
    overall_performance_headers = ['cpu_percent', 'Total_memory_usage %', 'Disk I/O read(MBs)', 'Disk I/O write(MBs)']
    per_process_headers = ['cpu_percent', 'Virtual Memory Usage%', 'Physical Memory Usage%', 'Disk I/O read(MBs)',
                           'Disk I/O write(MBs)']
    test_name = input("Enter Test Name: ")
    write_header('Overall performance.csv', overall_performance_headers, test_name)
    write_header('Per_process_performance.csv', per_process_headers, test_name)
    write_header('Per_process_performance2.csv', per_process_headers, test_name)

    processes = [psutil.Process(pid) for pid in [15580, 15581]]  # add process here

    while True:
        overall_performance_data = [psutil.cpu_percent(interval=1), psutil.virtual_memory().percent,
                                    round(psutil.disk_io_counters().read_bytes / (1024 * 1024), 2),
                                    round(psutil.disk_io_counters().write_bytes / (1024 * 1024), 2), test_name]
        write_data('Overall performance.csv', overall_performance_data)

        per_process_performance = [sum(collect_process_info(process, test_name)[0] for process in processes),
                                   sum(collect_process_info(process, test_name)[1] for process in processes),
                                   sum(collect_process_info(process, test_name)[2] for process in processes),
                                   sum(collect_process_info(process, test_name)[3] for process in processes),
                                   sum(collect_process_info(process, test_name)[4] for process in processes), test_name]
        write_data('Per_process_performance.csv', per_process_performance)
        for process in processes:
            process_performance = collect_process_info(process, test_name)
            write_data('Per_process_performance2.csv', process_performance)

        user_input = input("Type 'done' to exit: ")
        if user_input == "done":
            break


if __name__ == '__main__':
    main()
