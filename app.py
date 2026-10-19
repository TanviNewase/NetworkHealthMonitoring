
from flask import Flask, render_template, jsonify

from monitor import monitor_devices
from snmp_simulator import get_snmp_data

app = Flask(__name__)


@app.route("/healthz")
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route("/")
def dashboard():

    # ICMP monitoring
    devices = monitor_devices()

    # Add simulated SNMP information
    for device in devices:
        snmp_data = get_snmp_data(device["name"])

        device["cpu_usage"] = snmp_data["cpu_usage"]
        device["memory_usage"] = snmp_data["memory_usage"]
        device["interface_status"] = snmp_data["interface_status"]
        device["uptime_days"] = snmp_data["uptime_days"]

    total = len(devices)

    up = sum(
        1 for device in devices
        if device["status"] == "UP"
    )

    down = total - up
    alerts = []

    for device in devices:

        if device["status"] == "DOWN":
            alerts.append(
                f"{device['name']} is unreachable"
            )

        elif device["packet_loss"] > 10:
            alerts.append(
                f"{device['name']} has "
                f"{device['packet_loss']}% packet loss"
            )

        elif (
            device["latency"] is not None
            and device["latency"] > 100
        ):
            alerts.append(
                f"{device['name']} has high latency: "
                f"{device['latency']} ms"
            )

        if device["cpu_usage"] > 75:
            alerts.append(
                f"{device['name']} has high CPU usage: "
                f"{device['cpu_usage']}%"
            )

        if device["memory_usage"] > 80:
            alerts.append(
                f"{device['name']} has high memory usage: "
                f"{device['memory_usage']}%"
            )

        if device["interface_status"] == "DOWN":
            alerts.append(
                f"{device['name']} interface is DOWN"
            )

    return render_template(
        "dashboard.html",
        devices=devices,
        total=total,
        up=up,
        down=down,
        alerts=alerts
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
