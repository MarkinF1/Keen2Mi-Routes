import os
import re
import ipaddress
import time
import requests
from pathlib import Path

ROUTE_PATTERN = re.compile(r"route\s+add\s+([\d\.]+)\s+mask\s+([\d\.]+)", re.IGNORECASE)


def add_route_to_xiaomi(router_ip: str, stok_token: str, cidr_route: str) -> bool:
    """Отправляет POST-запрос на роутер для добавления маршрута."""
    url = f"http://{router_ip}/cgi-bin/luci/;stok={stok_token}/api/misystem/smartvpn_url"

    payload = {
        "url": cidr_route,
        "opt": "0"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            return True
        else:
            print(f"Ошибка HTTP {response.status_code} при добавлении {cidr_route}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения при добавлении {cidr_route}: {e}")
        return False


def parse_file(src_file: Path, router_ip: str, stok_token: str) -> tuple[int, int]:
    """Парсит отдельный файл, отправляет маршруты и возвращает счетчики успеха/ошибок."""
    print(f"\nЧитаем файл: {src_file}")

    file_added_count = 0
    file_not_added_count = 0

    with open(src_file, 'r', encoding='utf-8', errors='ignore') as f_in:
        for line in f_in:
            match = ROUTE_PATTERN.search(line)
            if match:
                ip = match.group(1)
                mask = match.group(2)

                try:
                    # Конвертируем в формат 192.168.1.1/24
                    interface = ipaddress.IPv4Interface(f"{ip}/{mask}")
                    cidr_route = str(interface.with_prefixlen)

                    print(f"  Добавляем: {cidr_route}...", end=" ")
                    if add_route_to_xiaomi(router_ip, stok_token, cidr_route):
                        print("OK")
                        file_added_count += 1
                    else:
                        print("FAIL")
                        file_not_added_count += 1

                    # Пауза, чтобы не повесить веб-сервер роутера множеством одновременных запросов
                    time.sleep(0.1)

                except ValueError:
                    print(f"  [!] Ошибка парсинга IP/Маски: {line.strip()}")

    total_processed = file_added_count + file_not_added_count
    print(f"Из файла {src_file.name} добавлено {file_added_count}/{total_processed} маршрутов.")

    return file_added_count, file_not_added_count


def process_and_upload_routes(router_ip: str, stok_token: str, src_dir: str):
    """Определяет тип пути (файл/папка) и запускает цикл обработки."""
    src_path = Path(src_dir)

    if not src_path.exists():
        print(f"Ошибка: Путь '{src_dir}' не найден.")
        return

    total_added = 0
    total_not_added = 0

    if src_path.is_file():
        added, not_added = parse_file(src_path, router_ip, stok_token)
        total_added += added
        total_not_added += not_added

    elif src_path.is_dir():
        for root, dirs, files in os.walk(src_path):
            for file in files:
                file_path = Path(root) / file
                added, not_added = parse_file(file_path, router_ip, stok_token)
                total_added += added
                total_not_added += not_added

    total_processed = total_added + total_not_added
    print(f"\nГотово! Всего добавлено маршрутов: {total_added}/{total_processed}")


if __name__ == "__main__":
    print("=== Утилита импорта маршрутов ===")
    try:
        r_ip = input("Введите IP роутера (например, 192.168.1.1): ").strip()
        token = input("Введите актуальный STOK из адресной строки: ").strip()
        source = input("Введите путь к каталогу или файлу (например, sites): ").strip()

        if r_ip and token and source:
            process_and_upload_routes(router_ip=r_ip, stok_token=token, src_dir=source)
        else:
            print("Ошибка: Все поля должны быть заполнены!")

    except KeyboardInterrupt:
        print("\n\nВыполнение прервано пользователем. Выход...")