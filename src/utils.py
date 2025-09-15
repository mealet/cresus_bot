import re


def parse_time_to_seconds(time_str: str):
    time_str = time_str.strip().lower()

    multipliers = {
        "s": 1,
        "sec": 1,
        "second": 1,
        "m": 60,
        "min": 60,
        "minute": 60,
        "h": 3600,
        "hour": 3600,
        "d": 86400,
        "day": 86400,
        "w": 604800,
        "week": 604800,
    }

    pattern = r"^(\d+\.?\d*)\s*([a-zA-Z]+)$"
    match = re.match(pattern, time_str)

    if not match:
        raise ValueError(f"Неверный формат времени: {time_str}")

    number = float(match.group(1))
    unit = match.group(2).lower()

    if unit not in multipliers:
        raise ValueError(f"Неизвестная единица измерения: {unit}")

    return int(number * multipliers[unit])
