Simple Port Scanner:

A simple port scanner that allows for single port scanning and scanning over a range of ports concurrently with CLI compatibility.

To use, simply specify a host, low end of the port range, and high end of the range

ex: 

```bash
python cli.py localhost 1 9000
```

The scanner determines whether a port is open by attempting a TCP connection to it (a "connect scan"). If the connection succeeds, the port is open; if it's refused, the port is closed; if the host can't be resolved, the scan reports that upfront rather than silently returning zero results.

Core components:

check_port(host, port) — Opens a socket and attempts to connect to a single port using connect_ex, which returns an error code instead of raising an exception on failure. This keeps the open/closed logic simple. A 1-second timeout prevents the scan from hanging on unresponsive (filtered) ports. Results are returned as a PortStatus enum (OPEN, CLOSED, UNRESOLVED) rather than raw strings, to avoid ambiguous or typo-prone comparisons elsewhere in the code.

scan_range(host, port_range) — Resolves the hostname once upfront (failing fast with a clear UNRESOLVED status if it can't), then checks every port in the given range concurrently using a ThreadPoolExecutor. Each port check is submitted as a separate task, and results are collected as they complete via as_completed, rather than waiting for them in a fixed order.

Please only use this utility on hosts you are permitted to test on