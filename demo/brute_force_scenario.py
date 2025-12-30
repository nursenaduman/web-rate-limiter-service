import requests
import time
from datetime import datetime

# Hedef URL (Rate limited endpoint)
TARGET_URL = "http://127.0.0.1:8000/limited-endpoint"

# Senaryo ayarları
TOTAL_REQUESTS = 15
ATTACK_DELAY = 0.2  # saniye


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'


def print_request_info(i, response):
    timestamp = datetime.now().strftime("%H:%M:%S")

    remaining = response.headers.get("X-RateLimit-Remaining")
    limit = response.headers.get("X-RateLimit-Limit")

    rate_info = ""
    if remaining is not None and limit is not None:
        rate_info = f" | Kalan Hak: {remaining}/{limit}"

    if response.status_code == 200:
        print(
            f"[{timestamp}] [{i}] "
            f"{Colors.GREEN}İzin Verildi (HTTP 200){Colors.RESET}"
            f"{rate_info}"
        )

    elif response.status_code == 429:
        print(
            f"[{timestamp}] [{i}] "
            f"{Colors.RED}⛔ ENGELLENDİ (HTTP 429){Colors.RESET}"
            f"{rate_info}"
        )

    else:
        print(
            f"[{timestamp}] [{i}] "
            f"{Colors.YELLOW}Beklenmeyen durum: {response.status_code}{Colors.RESET}"
        )

def brute_force_scenario():
    print(f"{Colors.CYAN}=== BRUTE FORCE SALDIRI SENARYOSU BAŞLIYOR ==={Colors.RESET}")
    print(f"Hedef Endpoint : {TARGET_URL}")
    print(f"Toplam İstek   : {TOTAL_REQUESTS}")
    print(f"Saldırı Hızı   : {ATTACK_DELAY} sn\n")

    for i in range(1, TOTAL_REQUESTS + 1):
        try:
            response = requests.get(TARGET_URL)
            print_request_info(i, response)

        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}Bağlantı hatası: {e}{Colors.RESET}")
            break

        time.sleep(ATTACK_DELAY)

    print(f"\n{Colors.CYAN}=== SENARYO TAMAMLANDI ==={Colors.RESET}")
    print("Gözlem: Rate limiting mekanizması limit aşıldığında isteği engellemiştir.")


if __name__ == "__main__":
    brute_force_scenario()
