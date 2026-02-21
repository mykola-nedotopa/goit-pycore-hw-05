import sys
from collections import Counter
from typing import Dict, List, Optional

KNOWN_LEVELS = ("INFO", "DEBUG", "ERROR", "WARNING")


def parse_log_line(line: str) -> Dict[str, str]:
    """
    Парсить рядок логу формату:
    YYYY-MM-DD HH:MM:SS LEVEL Message...
    Повертає dict: date, time, level, message
    """
    parts = line.strip().split(" ", 3)
    if len(parts) < 4:
        raise ValueError(f"Bad log line format: {line!r}")

    date, time, level, message = parts
    return {"date": date, "time": time, "level": level.upper(), "message": message}


def load_logs(file_path: str) -> List[Dict[str, str]]:
    """
    Завантажує лог-файл у список dict'ів.
    Некоректні/порожні рядки пропускає.
    """
    logs: List[Dict[str, str]] = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for idx, raw_line in enumerate(f, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    logs.append(parse_log_line(line))
                except ValueError:
                    continue
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except OSError as e:
        raise OSError(f"Cannot read file '{file_path}': {e}") from e

    return logs


def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    """
    Фільтрує логи за рівнем (case-insensitive).
    Використано елемент ФП: filter + lambda.
    """
    lvl = level.upper()
    return list(filter(lambda log: log.get("level") == lvl, logs))


def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Рахує кількість записів по рівнях.
    """
    counter = Counter(log.get("level", "UNKNOWN") for log in logs)
    return dict(counter)


def display_log_counts(counts: Dict[str, int]) -> None:
    """
    Друкує таблицю статистики.
    """
    header_left = "Рівень логування"
    header_right = "Кількість"
    print(f"{header_left:<16} | {header_right}")
    print("-" * 17 + "|----------")

    # спочатку стандартні рівні, потім решта (якщо трапились)
    ordered = [lvl for lvl in KNOWN_LEVELS if lvl in counts] + sorted(
        lvl for lvl in counts.keys() if lvl not in KNOWN_LEVELS
    )
    for lvl in ordered:
        print(f"{lvl:<16} | {counts[lvl]}")


def print_level_details(filtered: List[Dict[str, str]], level: str) -> None:
    print(f"\nДеталі логів для рівня '{level.upper()}':")
    for log in filtered:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("Використання: python main.py /path/to/logfile.log [level]")
        print("Приклад: python main.py logfile.log error")
        return 1

    file_path = argv[1]
    level: Optional[str] = argv[2] if len(argv) >= 3 else None

    try:
        logs = load_logs(file_path)
    except Exception as e:
        print(f"Помилка: {e}", file=sys.stderr)
        return 1

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level:
        filtered = filter_logs_by_level(logs, level)
        print_level_details(filtered, level)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))