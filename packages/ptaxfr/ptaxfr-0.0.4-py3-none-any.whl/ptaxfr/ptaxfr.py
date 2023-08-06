#!/usr/bin/python3
"""
    ptaxfr - DNS Zone Transfer Testing Tool

    Copyright (c) 2020 HACKER Consulting s.r.o.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__version__ = "0.0.4"

import argparse
import re
import sys

from ptlibs import ptmisclib, ptjsonlib
from ptthreads import ptthreads

import dns.resolver
import dns.zone


class ptaxfr:
    def __init__(self, args):
        self.use_json = args.json
        self.ptjsonlib = ptjsonlib.ptjsonlib(self.use_json)
        self.ptthreads = ptthreads.ptthreads()

        self.vulnerable_only = args.vulnerable_only
        self.silent = args.silent
        self.print_records = args.print_records
        self.print_subdomains = args.print_subdomains
        self.unique = args.unique

        try:
            self.domains = ptmisclib.read_file(args.file) if args.file else args.domain
        except FileNotFoundError:
            ptmisclib.end_error("File not found", self.ptjsonlib.add_json(SCRIPTNAME), self.ptjsonlib, self.use_json)

    def run(self, args):
        if self.print_records and self.print_subdomains:
            ptmisclib.end_error("Cannot use -pr and -ps parameters together", self.ptjsonlib.add_json("ns_check"), self.ptjsonlib, self.use_json)
        if self.vulnerable_only:
            ptmisclib.ptprint(ptmisclib.out_ifnot("Vulnerable domains:", "TITLE", self.use_json or self.silent))
        self.ptthreads.threads(self.domains, self.ns_check, args.threads)
        ptmisclib.ptprint(ptmisclib.out_if(self.ptjsonlib.get_all_json(), None, self.use_json))

    def ns_check(self, domain):
        """Finds and tests all nameservers of <domain> for zone transfer"""
        printlock = ptthreads.printlock()
        is_vulnerable = None
        vulnerable_ns_zones = []
        json_no = self.ptjsonlib.add_json("ns_check")
        self.ptjsonlib.add_data(json_no, {"domain": domain, "NS": []})

        printlock.add_string_to_output(ptmisclib.out_ifnot(ptmisclib.get_colored_text(f"Testing domain: {domain}", "TITLE"), "TITLE", self.use_json or self.vulnerable_only), silent=self.silent)
        resolver = dns.resolver.Resolver()
        resolver.timeout = 15
        domain_nameservers = []
        try:
            ns_query = resolver.resolve(domain, "NS", tcp=True)
            for rdata in ns_query:
                nameserver_name = str(rdata)[:-1]
                nameserver_ip = [str(ip) for ip in resolver.resolve(str(rdata)[:-1], "A")][0]
                domain_nameservers.append({"ns_name": str(rdata)[:-1], "ns_ip": nameserver_ip, "vulnerable": "null", "data": []})
                try:
                    printlock.add_string_to_output(ptmisclib.out_ifnot(f"Nameserver: {nameserver_name}", "INFO", self.use_json or self.vulnerable_only), silent=self.silent)
                    printlock.add_string_to_output(ptmisclib.out_ifnot(f"IP: {nameserver_ip}", "INFO", self.use_json or self.vulnerable_only), silent=self.silent)
                    zone = dns.zone.from_xfr(dns.query.xfr(nameserver_ip, domain, lifetime=5.01))
                    printlock.add_string_to_output(ptmisclib.out_ifnot(f"Vulnerable: True", "VULN", self.use_json or self.vulnerable_only), silent=self.silent, end="\n")
                    domain_nameservers[-1].update({"vulnerable": "True"})
                    vulnerable_ns_zones.append({nameserver_name: zone})
                    is_vulnerable = True
                except dns.exception.Timeout:
                    # TODO Zkontrolovat spolehlivost.
                    printlock.add_string_to_output(ptmisclib.out_ifnot(f"Timeout error", "ERROR", self.use_json or self.vulnerable_only), silent=self.silent)
                    domain_nameservers[-1].update({"vulnerable": "False"})
                except dns.exception.DNSException:
                    printlock.add_string_to_output(ptmisclib.out_ifnot(f"Vulnerable: False", "NOTVULN", self.use_json or self.vulnerable_only), silent=self.silent, end="\n")
                    domain_nameservers[-1].update({"vulnerable": "False"})
            self.ptjsonlib.set_status(json_no, "ok")
            self.ptjsonlib.add_data(json_no, {"NS": domain_nameservers})
            self.ptjsonlib.set_vulnerable(json_no, is_vulnerable)

            if is_vulnerable:
                printlock.add_string_to_output(domain, self.vulnerable_only)

            if is_vulnerable and not self.vulnerable_only and (self.print_records or self.print_subdomains):
                if self.unique:
                    printlock.add_string_to_output("\n"+ptmisclib.out_ifnot(f"Nameservers:", "INFO", self.use_json), silent=self.silent)
                    unique_result = []
                for entry in vulnerable_ns_zones:
                    for nameserver, zone in entry.items():
                        if self.unique:
                            printlock.add_string_to_output(ptmisclib.out_ifnot(f"{nameserver}", "INFO", self.use_json), silent=self.silent)
                        else:
                            printlock.add_string_to_output("\n"+ptmisclib.out_ifnot(f"{nameserver}:", "INFO", self.use_json), silent=self.silent)

                        if self.print_records:
                            data, output_string_list = self.extract_dns_records(zone, printlock)
                        else:
                            data = self.extract_subdomains(zone, printlock)

                        for j in domain_nameservers:
                            if j["ns_name"] == nameserver:
                                j["data"] = data

                if self.unique:
                    if self.print_records:
                        unique_result += [string for string in output_string_list if string not in unique_result]
                        printlock.add_string_to_output("\n"+ptmisclib.out_ifnot(f"Unique DNS Records:", "INFO", self.use_json), silent=self.silent)
                        for string in unique_result:
                            printlock.add_string_to_output(ptmisclib.out_ifnot(f"{string}", "", self.use_json))
                    if self.print_subdomains:
                        printlock.add_string_to_output("\n"+ptmisclib.out_ifnot(f"Unique Subdomains:", "INFO", self.use_json), silent=self.silent)
                        unique_result += [data for data in data if data not in unique_result]
                        self.unique_print_subdomains(unique_result, printlock)

        except Exception as e:
            self.ptjsonlib.set_status(json_no, "error", "domain not reachable")
            printlock.add_string_to_output(ptmisclib.out_ifnot(f"Domain not reachable - {e}", "ERROR", self.use_json or self.vulnerable_only), silent=self.silent)

        printlock.lock_print_output(end="\n")

    def extract_dns_records(self, zone, printlock):
        data = []
        output_string_list = []
        for name, node in zone.nodes.items():
            names = re.findall(r"DNS IN ([\(\)\w]*) rdataset", str(node.rdatasets))
            for i, rdataset in enumerate(node.rdatasets):
                if not self.vulnerable_only:
                    rdataset_records_str = str(rdataset).replace("\n", ", ")
                    rdataset_records_list = list(rdataset_records_str.split(","))
                    for rdataset_record in rdataset_records_list:
                        output_string = ""
                        rdataset_data = re.findall(rf"{names[i].replace('(', ' ').replace(')', ' ')}(.*)", rdataset_record)[0]
                        rdataset_type = names[i]
                        split_list = rdataset_records_str.split()

                        multiline_record = None
                        if len(rdataset_records_str.split(", ")) > 1:
                            multiline_record = [record.split() for record in rdataset_records_str.split(", ")]

                        if multiline_record:
                            output_string += str(name)
                            for r_no in range(len(multiline_record)):
                                if r_no == 0:
                                    output_string += f"{' '*(30-len(str(name)))}"
                                else:
                                    output_string += f"{' '*30}"
                                output_string += f"{multiline_record[r_no][0]}{' '*(10-len(multiline_record[r_no][0]))}{multiline_record[r_no][1]}{' '*(10-len(multiline_record[r_no][1]))}{multiline_record[r_no][2]}{' '*(10-len(multiline_record[r_no][2]))}{' '.join(multiline_record[r_no])}"
                        else:
                            output_string += f"{str(name)}{' '*(30-len(str(name)))}{split_list[0]}{' '*(10-len(str(split_list[0])))}{split_list[1]}{' '*(10-len(str(split_list[1])))}{split_list[2]}{' '*(10-len(str(split_list[2])))}{' '.join(split_list[3:])}".strip()
                        if self.unique:
                            if output_string not in output_string_list:
                                output_string_list.append(output_string)
                            else:
                                continue
                        else:
                            printlock.add_string_to_output(output_string)
                        data.append({"subdomain": str(name), "type": rdataset_type, "content": rdataset_data.lstrip()})

        return data, output_string_list

    def extract_subdomains(self, zone, printlock):
        data = []
        result_final = set()
        for name in zone.nodes.keys():
            result_final.add(str(name))
        result_final = list(result_final)
        result_final.sort()
        for name in result_final:
            if name == "@":
                continue
            if not self.vulnerable_only and not self.unique:
                printlock.add_string_to_output(ptmisclib.out_ifnot(f"{str(name)}", None, self.use_json), trim=True)
            data.append({"subdomain": str(name)})
        return data

    def unique_print_subdomains(self, unique_result, printlock):
        for entry in unique_result:
            subdomain = list(entry.values())[0]
            printlock.add_string_to_output(ptmisclib.out_ifnot(f"{subdomain}", "", self.use_json))


def get_help():
    return [
        {"description": ["DNS Zone Transfer Testing Tool"]},
        {"usage": ["ptaxfr <options>"]},
        {"usage_example": ["ptaxfr -d example.com", "ptaxfr -d example1.com example2.com example3.com", "ptaxfr -f domain_list.txt"]},
        {"options": [
            ["-d",  "--domain",           "<domain>",   "Test domain"],
            ["-f",  "--file",             "<file>",     "Test domains from file"],
            ["-pr", "--print-records",    "",           "Print DNS records"],
            ["-ps", "--print-subdomains", "",           "Print subdomains only"],
            ["-u",  "--unique",           "",           "Print unique records only"],
            ["-V",  "--vulnerable-only",  "",           "Print only vulnerable domains"],
            ["-s",  "--silent",           "",           "Silent mode (show result only)"],
            ["-t",  "--threads",          "<threads>",  "Number of threads (default 20)"],
            ["-j",  "--json",             "",           "Enable JSON output"],
            ["-v",  "--version",          "",           "Show script version and exit"],
            ["-h",  "--help",             "",           "Show this help message and exit"],
        ]}
    ]


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    required = parser.add_argument_group("One of the following arguments is required")
    required = required.add_mutually_exclusive_group(required=True)
    required.add_argument("-d", "--domain", type=str, nargs="+")
    required.add_argument("-f", "--file", type=str)
    parser.add_argument("-pr", "--print-records", action="store_true")
    parser.add_argument("-ps", "--print-subdomains", action="store_true")
    parser.add_argument("-u", "--unique", action="store_true")
    parser.add_argument("-V", "--vulnerable-only", action="store_true")
    parser.add_argument("-s", "--silent", action="store_true")
    parser.add_argument("-t", "--threads", type=int, default=20)
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("-v", "--version", action="version", version=f"{SCRIPTNAME} {__version__}")

    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        ptmisclib.help_print(get_help(), SCRIPTNAME, __version__)
        sys.exit(0)
    args = parser.parse_args()
    ptmisclib.print_banner(SCRIPTNAME, __version__, args.json or args.silent, space=0)
    return args


def main():
    global SCRIPTNAME
    SCRIPTNAME = "ptaxfr"
    args = parse_args()
    script = ptaxfr(args)
    script.run(args)


if __name__ == "__main__":
    main()
