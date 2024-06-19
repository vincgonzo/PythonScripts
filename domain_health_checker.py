#!/bin/python3
import dns.resolver
import dns.exception
import requests

def load_domains(filename):
    """Load domains from a file into a set, ensuring each domain is clean and lowercased."""
    with open(filename, 'r') as file:
        return {line.strip().lower() for line in file if line.strip()}

def filter_whitelisted_domains(all_domains, blacklist):
    """Filter out blacklisted domains from all domains."""
    return all_domains - blacklist

def verify_dns(domain):
    """Verify if a domain has a valid DNS record."""
    try:
        # Resolve the domain to check if it's valid
        dns.resolver.resolve(domain, 'A')
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout, dns.resolver.NoNameservers):
        return False

def check_reputation(domain, api_key):
    """Check the reputation of a domain using VirusTotal API."""
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers = {
        "x-apikey": api_key
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            # Check if the domain is flagged as malicious by any engine
            malicious = json_response.get('data', {}).get('attributes', {}).get('last_analysis_stats', {}).get('malicious', 0)
            return malicious == 0  # Return True if not malicious
        else:
            print(f"Failed to get reputation for {domain}: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error checking reputation for {domain}: {e}")
        return False

def save_domains(filename, domains):
    """Save the whitelisted and verified domains to a file."""
    with open(filename, 'w') as file:
        for domain in sorted(domains):
            file.write(f"{domain}\n")

# File paths
all_domains_file = 'all_domains.txt'
blacklist_file = 'blacklist.txt'
whitelisted_domains_file = 'whitelisted_domains.txt'

# VirusTotal API key (replace with your actual API key)
virustotal_api_key = 'YOUR_VIRUS_TOTAL_API_KEY'
# Load domains
try:
    all_domains = load_domains(all_domains_file)
    blacklist = load_domains(blacklist_file)

    # Check if domains are properly loaded
    if not all_domains:
        raise ValueError("The all_domains.txt file is empty or missing.")
    if not blacklist:
        print("Warning: The blacklist.txt file is empty or missing. DNS verification and reputation checks will be applied to all domains.")

    # Filter whitelisted domains
    whitelisted_domains = filter_whitelisted_domains(all_domains, blacklist)

    # Perform DNS verification and reputation check on whitelisted domains
    verified_whitelisted_domains = {
        domain for domain in whitelisted_domains
        if verify_dns(domain) and check_reputation(domain, virustotal_api_key)
    }

    # Save the whitelisted and verified domains
    save_domains(whitelisted_domains_file, verified_whitelisted_domains)

    print(f"Whitelisted and verified domains have been saved to {whitelisted_domains_file}")

except FileNotFoundError as fnfe:
    print(f"Error: {fnfe}")
except Exception as e:
    print(f"An error occurred: {e}")
