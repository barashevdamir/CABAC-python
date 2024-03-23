def exp_golomb_coding(number, order=0):
    """
    Преобразует целое число в его кодовое представление Exp-Golomb,
    включая поддержку отрицательных чисел и ордеров кодирования.

    Args:
    number (int): Число, подлежащее преобразованию.
    order (int): Ордер кодирования, который определяет количество битов,
                 используемых для бинарной части кода.

    Returns:
    str: Кодировка числа Exp-Golomb.
    """
    # Преобразование целого числа в натуральное с учетом отрицательных значений
    mapped_number = (abs(number) * 2) - (1 if number < 0 else 0)

    # Применение ордера к числу
    mapped_number = mapped_number >> order

    # Увеличиваем число для обработки нуля
    mapped_number += 1

    # Длина числа в двоичном формате
    length = mapped_number.bit_length()

    # Унарное кодирование префикса: (длина-1) нули, за которыми следует 1
    prefix = '0' * (length - 1) + '1'

    # Двоичное представление суффикса, исключающее начальный бит
    suffix = bin(mapped_number)[3:]  # Исключаем префикс '0b1'
    if order > 0:
        suffix += bin(number & ((1 << order) - 1))[2:].zfill(order)  # Добавляем ордер битов в конец

    # Объединяем префикс и суффикс для кода Exp-Golomb
    exp_golomb_code = prefix + suffix
    return exp_golomb_code

