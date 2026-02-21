def caching_fibonacci():
    """
    Повертає функцію fibonacci(n), яка рахує n-не число Фібоначчі
    рекурсивно і кешує вже обчислені значення (замикання).
    """
    cache = {0: 0, 1: 1}

    def fibonacci(n: int) -> int:
        if not isinstance(n, int):
            raise TypeError("n must be an integer")
        if n < 0:
            raise ValueError("n must be >= 0")

        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


if __name__ == "__main__":
    fib = caching_fibonacci()

    print(fib(10))  # 55
    print(fib(15))  # 610

    # Перевірка, що кеш працює (повторний виклик не перерахує все заново)
    print(fib(10))  # 55