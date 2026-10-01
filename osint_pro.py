#!/usr/bin/env python3
"""
🔥 OSINT PRO - All-in-One Information Gathering Tool
BY KRUTIK 🚨 CYBER EXPERT
Educational Purpose Only
"""

import os
import sys
import socket
import requests
import whois
import dns.resolver
import re
import time
from datetime import datetime

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def cprint(text, color=Colors.WHITE, bold=False):
    style = color + (Colors.BOLD if bold else '')
    print(f"{style}{text}{Colors.RESET}")

def clear():
    os.system('clear')

def header():
    clear()
    cprint("""
╔══════════════════════════════════════════════════════════════╗
║   🔥 OSINT PRO - Information Gathering Tool                ║
║   📌 Email | Phone | Username | DNS | WHOIS | Clone       ║
║   👑 BY KRUTIK CYBER EXPERT                                ║
╚══════════════════════════════════════════════════════════════╝
""", Colors.CYAN, True)

# ─── 1. EMAIL LOOKUP ──────────────────────────────────────────

def email_lookup():
    cprint("\n📧 EMAIL LOOKUP", Colors.GREEN, True)
    email = input("Enter email: ")
    
    print(f"\n🔍 Looking up {email}...\n")
    
    if '@' not in email:
        cprint("❌ Invalid email!", Colors.RED)
        return
    
    domain = email.split('@')[1]
    
    try:
        mx = dns.resolver.resolve(domain, 'MX')
        print(f"📡 MX Records: {[str(r.exchange) for r in mx]}")
    except:
        print("❌ No MX records found")
    
    try:
        spf = dns.resolver.resolve(domain, 'TXT')
        for r in spf:
            if 'v=spf1' in str(r):
                print(f"📡 SPF: {str(r)[:100]}...")
    except:
        pass
    
    cprint("\n✅ Email lookup complete!", Colors.GREEN)

# ─── 2. PHONE LOOKUP ──────────────────────────────────────────

def phone_lookup():
    cprint("\n📱 PHONE LOOKUP", Colors.GREEN, True)
    phone = input("Enter phone number: ")
    
    print(f"\n🔍 Looking up {phone}...\n")
    
    try:
        import phonenumbers
        from phonenumbers import carrier, geocoder, timezone
        
        number = phonenumbers.parse(phone, "IN")
        
        print(f"📌 Country: {geocoder.description_for_number(number, 'en')}")
        print(f"📌 Carrier: {carrier.name_for_number(number, 'en')}")
        print(f"📌 Timezone: {timezone.time_zones_for_number(number)}")
        print(f"📌 Valid: {phonenumbers.is_valid_number(number)}")
    except:
        try:
            response = requests.get(f"https://api.veriphone.com/v1/verify?phone={phone}", timeout=5)
            data = response.json()
            if data.get('valid'):
                print(f"📌 Country: {data.get('country_code')}")
                print(f"📌 Carrier: {data.get('carrier')}")
                print(f"📌 Valid: Yes")
            else:
                print("❌ Invalid phone number!")
        except:
            cprint("❌ Could not lookup phone number!", Colors.RED)

# ─── 3. USERNAME CHECKER ──────────────────────────────────────

def username_checker():
    cprint("\n👤 USERNAME CHECKER", Colors.GREEN, True)
    username = input("Enter username: ")
    
    print(f"\n🔍 Checking {username}...\n")
    
    sites = {
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "YouTube": f"https://youtube.com/@{username}",
        "Reddit": f"https://reddit.com/user/{username}",
        "GitLab": f"https://gitlab.com/{username}",
        "Pinterest": f"https://pinterest.com/{username}",
        "TikTok": f"https://tiktok.com/@{username}",
        "Telegram": f"https://t.me/{username}",
        "Quora": f"https://quora.com/profile/{username}"
    }
    
    for site, url in sites.items():
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                cprint(f"✅ {site}: Available", Colors.GREEN)
            else:
                cprint(f"❌ {site}: Not found", Colors.RED)
        except:
            cprint(f"⚠️ {site}: Could not check", Colors.YELLOW)
        time.sleep(0.5)

# ─── 4. DNS LOOKUP ─────────────────────────────────────────────

def dns_lookup():
    cprint("\n🌐 DNS LOOKUP", Colors.GREEN, True)
    domain = input("Enter domain: ")
    
    print(f"\n🔍 DNS records for {domain}...\n")
    
    records = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
    
    for record in records:
        try:
            answers = dns.resolver.resolve(domain, record)
            for r in answers:
                print(f"📡 {record}: {r}")
        except:
            pass

# ─── 5. WHOIS LOOKUP ──────────────────────────────────────────

def whois_lookup():
    cprint("\n📋 WHOIS LOOKUP", Colors.GREEN, True)
    domain = input("Enter domain: ")
    
    print(f"\n🔍 WHOIS for {domain}...\n")
    
    try:
        w = whois.whois(domain)
        print(f"📌 Domain: {w.domain_name}")
        print(f"📌 Registrar: {w.registrar}")
        print(f"📌 Creation Date: {w.creation_date}")
        print(f"📌 Expiry Date: {w.expiration_date}")
        print(f"📌 Name Servers: {', '.join(w.name_servers) if w.name_servers else 'N/A'}")
        print(f"📌 Status: {', '.join(w.status) if w.status else 'N/A'}")
    except:
        cprint("❌ Could not fetch WHOIS!", Colors.RED)

# ─── 6. WEBSITE CLONER ────────────────────────────────────────

def website_cloner():
    cprint("\n📂 WEBSITE CLONER", Colors.GREEN, True)
    url = input("Enter URL to clone: ")
    
    if not url.startswith('http'):
        url = 'http://' + url
    
    print(f"\n🔍 Cloning {url}...\n")
    
    try:
        response = requests.get(url, timeout=10)
        
        folder_name = url.replace('http://', '').replace('https://', '').replace('/', '_')
        os.makedirs(folder_name, exist_ok=True)
        
        with open(f"{folder_name}/index.html", "w", encoding='utf-8') as f:
            f.write(response.text)
        
        cprint(f"✅ Website cloned to: {folder_name}/", Colors.GREEN)
        cprint(f"📄 HTML saved: {folder_name}/index.html", Colors.CYAN)
    except Exception as e:
        cprint(f"❌ Error cloning website: {e}", Colors.RED)

# ─── 7. LINK EXTRACTOR ────────────────────────────────────────

def link_extractor():
    cprint("\n🔗 LINK EXTRACTOR", Colors.GREEN, True)
    url = input("Enter URL: ")
    
    if not url.startswith('http'):
        url = 'http://' + url
    
    print(f"\n🔍 Extracting links from {url}...\n")
    
    try:
        response = requests.get(url, timeout=10)
        links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
        
        clean_links = []
        for link in links:
            if link.startswith('http') or link.startswith('/'):
                clean_links.append(link)
        
        clean_links = list(set(clean_links))
        
        print(f"📊 Total links found: {len(clean_links)}\n")
        
        for link in clean_links[:20]:
            print(f"  • {link}")
        
        if len(clean_links) > 20:
            print(f"\n  ... and {len(clean_links) - 20} more")
    except Exception as e:
        cprint(f"❌ Error: {e}", Colors.RED)

# ─── 8. EMAIL EXTRACTOR ──────────────────────────────────────

def email_extractor():
    cprint("\n📧 EMAIL EXTRACTOR", Colors.GREEN, True)
    url = input("Enter URL: ")
    
    if not url.startswith('http'):
        url = 'http://' + url
    
    print(f"\n🔍 Extracting emails from {url}...\n")
    
    try:
        response = requests.get(url, timeout=10)
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
        
        emails = list(set(emails))
        
        if emails:
            print(f"📊 Emails found: {len(emails)}\n")
            for email in emails:
                print(f"  • {email}")
        else:
            cprint("❌ No emails found!", Colors.RED)
    except Exception as e:
        cprint(f"❌ Error: {e}", Colors.RED)

# ─── MAIN MENU ─────────────────────────────────────────────────

def menu():
    header()
    cprint("📋 MAIN MENU", Colors.CYAN, True)
    cprint("─" * 50, Colors.DIM)
    print("")
    print(" 1. 📧 Email Lookup")
    print(" 2. 📱 Phone Lookup")
    print(" 3. 👤 Username Checker")
    print(" 4. 🌐 DNS Lookup")
    print(" 5. 📋 WHOIS Lookup")
    print(" 6. 📂 Website Cloner")
    print(" 7. 🔗 Link Extractor")
    print(" 8. 📧 Email Extractor")
    print(" 0. ❌ Exit")
    print("")
    cprint("─" * 50, Colors.DIM)

def main():
    while True:
        menu()
        choice = input("\n👉 Choose (0-8): ")
        
        if choice == '1':
            email_lookup()
        elif choice == '2':
            phone_lookup()
        elif choice == '3':
            username_checker()
        elif choice == '4':
            dns_lookup()
        elif choice == '5':
            whois_lookup()
        elif choice == '6':
            website_cloner()
        elif choice == '7':
            link_extractor()
        elif choice == '8':
            email_extractor()
        elif choice == '0':
            cprint("\n👋 Thanks for using OSINT PRO!", Colors.GREEN, True)
            sys.exit(0)
        else:
            cprint("❌ Invalid choice!", Colors.RED)
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
