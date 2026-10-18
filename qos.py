def analyze_qos(latency, packet_loss, status):

    if status == "DOWN":
        return "CRITICAL"

    if packet_loss > 10:
        return "POOR"

    if latency is not None and latency > 100:
        return "POOR"

    if packet_loss > 0:
        return "WARNING"

    if latency is not None and latency > 50:
        return "MODERATE"

    return "GOOD"