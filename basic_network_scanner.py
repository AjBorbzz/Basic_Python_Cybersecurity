import nmap


def scan_network(target):
    nm = nmap.PortScanner()
    nm.scan(target, '1-1024') # Scan ports from 1 to 1024
    print(f"scan results for {target}:")

    for host in nm.all_hosts():
        print(f"Host: {host} ({nm[host].hostname()})")
        print(f"State: {nm[host].state()}")

        for proto in nm[host].all_protocols():
            print(f"Protocol: {proto}")

            ports = nm[host][proto].keys()
            for port in sorted(ports):
                print(f"Port : {port}\tState: {nm[host][proto][port]['state']}")
                if 'product' in nm[host][proto][port]:
                    print(f"Service: {nm[host][proto][port]['name']}\tProduct: {nm[host][proto][port]['product']}")

    # Run an Nmap script to detect vulnerabilities
    nm.scan(target, arguments='--script vuln')
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            for port in nm[host][proto].keys():
                if 'script' in nm[host][proto][port]:
                    for script_name, output in nm[host][proto][port]['script'].items():
                        print(f"Script: {script_name}\nOutput: {output}")


if __name__ == '__main__':
    target = input("Enter the target IP address or hostname: ")
    scan_network(target)