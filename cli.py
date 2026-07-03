from scanner import scan_range, PortStatus
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A simple concurrent port scanner")
    parser.add_argument("host", help="Target host to scan")
    parser.add_argument("range_min", help="Low value of port range to scan", type=int)
    parser.add_argument("range_max", help="High value of port range to scan", type=int)

    args = parser.parse_args()

    arg_tuple = (args.range_min, args.range_max)

    open_ports = scan_range(args.host, arg_tuple)
    if open_ports == PortStatus.UNRESOLVED:
        print("Unresolved Host")
    else:

        if len(open_ports) >= 1:
            print("Open Ports: ")
            for entry in open_ports:
                print(entry)
        else:
            print("No Open Ports")
