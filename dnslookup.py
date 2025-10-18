import dns.resolver
def query_all_records(domain:str, timeout:float) -> dict:
    record_types = [
        "A", "AAAA", "CNAME", "MX", "NS",
        "TXT", "SOA", "SRV", "PTR"
    ]

    resolver = dns.resolver.Resolver()
    resolver.nameservers = ["8.8.8.8", "1.1.1.1"]
    resolver.lifetime = timeout

    results = {}

    for rtype in record_types:
        try:
            answers = resolver.resolve(domain, rtype)
            detailed = []
            for rdata in answers:
                if rtype == "MX":
                    detailed.append({
                        "priority": rdata.preference,
                        "mail_server": str(rdata.exchange)
                    })
                elif rtype == "SOA":
                    detailed.append({
                        "primary_name_server": str(rdata.mname),
                        "responsible_email": str(rdata.rname),
                        "serial": rdata.serial,
                        "refresh": rdata.refresh,
                        "retry": rdata.retry,
                        "expire": rdata.expire,
                        "default TTL": rdata.minimum
                    })
                elif rtype == "SRV":
                    detailed.append({
                        "priority": rdata.priority,
                        "weight": rdata.weight,
                        "port": rdata.port,
                        "target": str(rdata.target)
                    })
                elif rtype == "TXT":
                    detailed.append("".join(rdata.strings))
                else:
                    detailed.append(rdata.to_text())
            results[rtype] = detailed
        except dns.resolver.NoAnswer:
            results[rtype] = []
        except dns.resolver.NXDOMAIN:
            results[rtype] = "Domain does not exist"
            break
        except dns.resolver.NoNameservers:
            results[rtype] = "No nameservers responded"
        except Exception as e:
            results[rtype] = f"Error: {e}"

    return results

def print_dns_results(domain:str, results:dict) -> None:
    print(f"\nDNS Report for: {domain}\n{'='*60}\n")
    for rtype, data in results.items():
        print(f"🔹 {rtype} Records")
        print("-" * 60)
        if isinstance(data, str):
            print(f"  {data}")
        elif isinstance(data, list):
            if not data:
                print("  (no records found)")
            else:
                for idx, entry in enumerate(data, start=1):
                    if isinstance(entry, dict):
                        print(f"  Record #{idx}:")
                        for k, v in entry.items():
                            print(f"    {k:<20}: {v}")
                    else:
                        print(f"  - {entry}")
        print()

def proces_dnslookup(domain:str,timeout:float) -> None:
    result = query_all_records(domain, timeout)
    print_dns_results(domain, result)