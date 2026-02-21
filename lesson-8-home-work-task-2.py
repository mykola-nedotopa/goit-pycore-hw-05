import re
from typing import Callable, Iterator


# Дійсні числа (з крапкою), які відокремлені пробілами з обох боків
_FLOAT_RE = re.compile(r"(?:(?<=\s)|^)(\d+\.\d+)(?=\s|$)")


def generator_numbers(text: str) -> Iterator[float]:
    """
    Аналізує текст і повертає генератор дійсних чисел (float),
    що відокремлені пробілами з обох боків.
    """
    for match in _FLOAT_RE.finditer(text):
        yield float(match.group(1))


def sum_profit(text: str, func: Callable[[str], Iterator[float]]) -> float:
    """
    Повертає суму всіх чисел, які згенерує func(text).
    """
    return sum(func(text))


if __name__ == "__main__":
    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими надходженнями "
        "27.45 і 324.00 доларів."
    )
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income:.2f}")  # очікувано: 1351.46