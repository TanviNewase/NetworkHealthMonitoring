
import json
import platform
import re
import shutil
import subprocess
from datetime import datetime


def ping_device(ip):
    """Ping a device five times on Windows or Linux."""

    try:
        system = platform.system().lower()

        if system == "windows":
            command = ["ping", "-n", "5", ip]
        else:
            command = ["ping", "-c", "5", "-W", "2", ip]

        if shutil.which(command[0]) is None:
            raise FileNotFoundError(
                "The ping executable is not installed."
            )

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15
        )

        output = result.stdout + result.stderr

        # Extract packet loss from Windows or Linux output.
        loss_match = re.search(
            r"\((\d+(?:\.\d+)?)%\s*loss\)",
            output,
            re.IGNORECASE
        )

        if not loss_match:
            loss_match = re.search(
                r"(\d+(?:\.\d+)?)%\s*packet loss",
                output,
                re.IGNORECASE
            )

        packet_loss = (
            float(loss_match.group(1))
            if loss_match
            else 100.0
        )

        # Extract average latency.
        latency_match = re.search(
            r"Average\s*=\s*(\d+)ms",
            output,
            re.IGNORECASE
        )

        if not latency_match:
            latency_match = re.search(
                r"(?:rtt|round-trip).*?=\s*"
                r"[\d.]+/([\d.]+)/",
                output,
                re.IGNORECASE
            )

        latency = (
            float(latency_match.group(1))
            if latency_match
            else None
        )

        status = (
            "UP"
            if result.returncode == 0 and packet_loss < 100
            else "DOWN"
        )

        return {
            "status": status,
            "latency": latency,
            "packet_loss": packet_loss,
            "time": datetime.now().strftime("%H:%M:%S")
        }

    except Exception as error:
        return {
            "status": "DOWN",
            "latency": None,
            "packet_loss": 100,
            "time": datetime.now().strftime("%H:%M:%S"),
            "error": str(error)
        }


def load_devices():
    with open("devices.json", "r", encoding="utf-8") as file:
        return json.load(file)


def monitor_devices():
    devices = load_devices()
    results = []

    for device in devices:
        result = ping_device(device["ip"])

        results.append({
            "name": device["name"],
            "ip": device["ip"],
            **result
        })

    return results


if __name__ == "__main__":
    for device in monitor_devices():
        print("-" * 32)
        print("Device:", device["name"])
        print("IP:", device["ip"])
        print("Status:", device["status"])
        print("Latency:", device["latency"], "ms")
        print("Packet Loss:", device["packet_loss"], "%")
        print("Time:", device["time"])
