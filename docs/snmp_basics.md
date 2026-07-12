# SNMP Basics

## What is SNMP?

SNMP (Simple Network Management Protocol) is a standard protocol used to monitor and manage network devices such as routers, switches, and servers. A monitoring application (the SNMP manager) periodically queries devices (SNMP agents) to collect operational metrics and detect faults.

## SNMP Architecture

```
SNMP Manager (Monitoring System)
            │
      Polls using SNMP
            │
SNMP Agent (Router/Switch)
```

## Key Terms

- **MIB (Management Information Base):** A hierarchical database that defines the metrics exposed by a device.
- **OID (Object Identifier):** The unique address of a metric within the MIB.

## Telemetry Sources for This Project

| Metric | Source | Example OID |
|---------|---------|--------------|
| CPU Utilization | SNMP | 1.3.6.1.2.1.25.3.3.1.2 |
| Memory Utilization | SNMP | 1.3.6.1.4.1.2021.4.6.0 |
| Interface Bandwidth | SNMP | 1.3.6.1.2.1.2.2.1.10 |
| Packet Loss | ICMP Ping | N/A |
| Latency | ICMP Ping | N/A |
| BGP Session State | BGP Feed | N/A |

## Polling Strategy

In a production deployment, the monitoring service will poll network devices every 5 minutes via SNMP. The current dataset is synthetic and simulates data collected at this interval.