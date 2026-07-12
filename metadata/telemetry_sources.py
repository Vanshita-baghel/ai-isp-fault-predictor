

telemetry_sources= {
    "cpu_utilization":{
        "source": "SNMP",
        "oid": "1.3.6.1.2.1.25.3.3.1.2",
    },
    "memory_utilization": {
        "source": "SNMP",
        "oid": "1.3.6.1.4.1.2021.4.6.0",
    },
    "bandwidth_mbps": {
        "source": "SNMP",
        "oid": "1.3.6.1.2.1.2.2.1.10",
    },
    "packet_loss": {
        "source": "ICMP ping",
        "oid": None,
    },
    "latency_ms": {
        "source": "ICMP ping",
        "oid": None,
    },
    "bgp_state": {
        "source": "BGP feed",
        "oid": None,
    },
}

for metric, info in telemetry_sources.items():
    print(
        f"{metric} : collected via {info['source']}"
        + (f" (OID: {info['oid']})" if info['oid'] else "")
        )