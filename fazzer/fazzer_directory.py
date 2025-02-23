import requests
import os
import sys
import logging
import re
import configparser
from concurrent.futures import ThreadPoolExecutor

# Загружаем настройки из application.properties
config = configparser.ConfigParser()
config.read("application.properties")

LOG_LEVEL = config.get("Settings", "log_level", fallback="INFO")
MAX_WORKERS = config.getint("Settings", "max_workers", fallback=10)


def setup_logging():
    """Настраивает логирование."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("fuzzer.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )


def load_file_list(file_name):
    """Загружает список файлов и директорий из файла."""
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        logging.error("Файл со списком не найден.")
        return []


def check_url(full_url, output_file):
    """Проверяет доступность URL."""
    try:
        response = requests.get(full_url, timeout=5)
        if response.status_code != 404:
            logging.info(f"[+] Найдено: {full_url}")
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(full_url + '\n')
    except requests.exceptions.SSLError as e:
        logging.warning(f"[!] SSL ошибка при подключении к {full_url}: {e}")
    except requests.RequestException as e:
        logging.warning(f"[!] Ошибка запроса к {full_url}: {e}")


def fuzz_files(url, extensions, file_list, output_file):
    """Фаззинг файлов на указанном сайте с многопоточностью."""
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for index, file in enumerate(file_list):
            for ext in extensions:
                full_url = f"{url.rstrip('/')}/{file}{ext.strip()}"
                sys.stdout.write(f"\r[*] Проверка: {full_url} ({index + 1}/{len(file_list)})")
                sys.stdout.flush()
                futures.append(executor.submit(check_url, full_url, output_file))
        for future in futures:
            future.result()  # Дожидаемся выполнения всех потоков

    logging.info("\n[✓] Фаззинг завершен. Результаты записаны в file.txt")


def is_valid_url(url):
    """Проверяет, является ли введенный URL корректным."""
    regex = re.compile(
        r'^(https?://)?'  # Протокол
        r'(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})'  # Доменное имя
        r'(:[0-9]{1,5})?'  # Порт
        r'(/.*)?$', re.IGNORECASE)  # Путь
    return re.match(regex, url)


def get_valid_url():
    """Запрашивает у пользователя URL и проверяет его валидность."""
    while True:
        url = input("Введите URL сайта: ").strip()
        url = url.rstrip('/')
        if is_valid_url(url):
            return url
        logging.error("Введен некорректный URL. Попробуйте снова.")


def main():
    setup_logging()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    file_name = input(
        "Введите имя файла со словарем (нажмите Enter для использования 'wordlist.txt'): ") or os.path.join(script_dir,
                                                                                                            "wordlist.txt")
    output_file = input("Введите имя выходного файла (нажмите Enter для использования 'file.txt'): ") or os.path.join(
        script_dir, "file.txt")

    if os.path.exists(output_file):
        overwrite = input(f"Файл {output_file} уже существует. Перезаписать? (y/n): ").strip().lower()
        if overwrite != 'y':
            logging.info("Выход из программы.")
            return
        os.remove(output_file)

    url = get_valid_url()
    extensions = [ext.strip() for ext in
                  input("Введите расширения файлов через запятую (например, .txt,.php): ").split(',')]

    file_list = load_file_list(file_name)
    if not file_list:
        return

    fuzz_files(url, extensions, file_list, output_file)


if __name__ == "__main__":
    main()
