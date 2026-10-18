import random


def get_snmp_data(device_name):

    cpu_usage = random.randint(20, 80)

    memory_usage = random.randint(30, 85)

    interface_status = random.choice([
        "UP",
        "UP",
        "UP",
        "DOWN"
    ])

    uptime_days = random.randint(1, 30)

    return {
        "device": device_name,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "interface_status": interface_status,
        "uptime_days": uptime_days
    }


if __name__ == "__main__":

    data = get_snmp_data("Router-1")

    print("SNMP SIMULATION")
    print("-------------------------")

    print("Device:", data["device"])
    print("CPU Usage:", data["cpu_usage"], "%")
    print("Memory Usage:", data["memory_usage"], "%")
    print("Interface:", data["interface_status"])
    print("Uptime:", data["uptime_days"], "days")