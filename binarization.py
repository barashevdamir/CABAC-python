def exp_golomb_coding(number):
    """
    Преобразует неотрицательное целое число в его кодовое представление Exp-Golomb.

    Args:
    number (int): Число, подлежащее преобразованию, где number >= 0.

    Returns:
    str: Кодировка числа Exp-Golomb.
    """
    # Увеличиваем число для обработки нуля
    number += 1

    # Длина числа в двоичном формате
    length = number.bit_length()

    # Унарное кодирование префикса: (длина-1) нули, за которыми следует 1
    prefix = '0' * (length - 1) + '1'

    # Двоичное представление суффикса, исключающее начальный бит
    suffix = bin(number)[3:]  # Исключаем префикс '0b1'

    # Объединяем префикс и суффикс для кода Exp-Golomb
    exp_golomb_code = prefix + suffix
    return exp_golomb_code


