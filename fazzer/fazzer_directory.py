import requests
import os
import sys


def load_file_list(file_name):
    """Загружает список файлов и директорий из файла."""
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            file_list = [line.strip() for line in f.readlines() if line.strip()]
        return file_list
    except FileNotFoundError:
        print("Файл со списком не найден.")
        return []


def fuzz_files(url, extensions, file_list, output_file):
    """Фаззинг файлов на указанном сайте и запись результатов в реальном времени."""

    with open(output_file, 'w', encoding='utf-8') as f:
        for index, file in enumerate(file_list):
            for ext in extensions:
                full_url = f"{url.rstrip('/')}/{file}{ext.strip()}"
                sys.stdout.write(f"\r[*] Проверка: {full_url} ({index + 1}/{len(file_list)})")
                sys.stdout.flush()

                try:
                    response = requests.get(full_url, timeout=5)
                    if response.status_code != 404:
                        print(f"\n[+] Найдено: {full_url}")
                        f.write(full_url + '\n')
                        f.flush()
                except requests.exceptions.SSLError as e:
                    print(f"\n[!] SSL ошибка при подключении к {full_url}: {e}")
                except requests.RequestException as e:
                    print(f"\n[!] Ошибка запроса к {full_url}: {e}")

    print("\n[✓] Фаззинг завершен. Результаты записаны в file.txt")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(script_dir, "wordlist.txt")
    output_file = os.path.join(script_dir, "file.txt")

    url = input("Введите URL сайта (без / на конце): ")
    extensions = [ext.strip() for ext in
                  input("Введите расширения файлов через запятую (например, .txt,.php): ").split(',')]

    file_list = load_file_list(file_name)
    if not file_list:
        return

    fuzz_files(url, extensions, file_list, output_file)


if __name__ == "__main__":
    main()
