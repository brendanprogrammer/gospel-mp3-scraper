import psutil

def check_disk_partitions():
    """Prints all disk partitions and their usage."""
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"Partition: {partition.device}")
        usage = psutil.disk_usage(partition.mountpoint)
        print(f"Total: {usage.total / (1024 ** 3):.2f} GB")
        print(f"Used: {usage.used / (1024 ** 3):.2f} GB")
        print(f"Free: {usage.free / (1024 ** 3):.2f} GB")
        print('-' * 40)

check_disk_partitions()