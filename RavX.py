#!/usr/bin/env python3

import requests
from urllib.parse import urlparse, urljoin

# ===================== ASCII BANNER ===================== #
def banner():
    print("""
██████╗ ██╗██████╗ ██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██║██╔══██╗╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██║  ██║██║██████╔╝ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██║  ██║██║██╔══██╗ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██████╔╝██║██║  ██║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝
                        Tool by: RavX                            

============================================================\n""")


def normalize_base_url(url: str) -> str:
    url = url.strip()
    if not urlparse(url).scheme:
        url = "http://" + url
    if not url.endswith("/"):
        url += "/"
    return url


def load_wordlist(path: str):
    entries = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                entries.append(line)
    except Exception as e:
        print(f"[!] Failed to read wordlist: {e}")
        return []
    return entries


# ===================== MAIN ===================== #

def main():
    banner()

    base = input("Enter base URL (e.g. https://example.com): ").strip()
    wordlist_path = input("Enter wordlist file path: ").strip()

    if not base or not wordlist_path:
        print("\n[!] Base URL and wordlist path are required.\n")
        return

    base_url = normalize_base_url(base)
    wordlist = load_wordlist(wordlist_path)

    if not wordlist:
        print("[!] No entries loaded from wordlist. Exiting.")
        return

    print(f"\n[*] Target base: {base_url}")
    print(f"[*] Total entries in wordlist: {len(wordlist)}")
    print("\n=== Showing Only Status 200 Directories ===\n")

    session = requests.Session()

    for entry in wordlist:
        dir_name = entry.strip().strip("/")
        if not dir_name:
            continue

        full_url = urljoin(base_url, dir_name + "/")

        try:
            resp = session.get(full_url, timeout=8, allow_redirects=True)
        except requests.RequestException:
            continue

        if resp.status_code == 200:
            print(f"[200] {full_url}")

    print("\n[*] Scan completed.")
    print("💀 Tool by RavX\n")


if __name__ == "__main__":
    main()

