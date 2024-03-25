class Binarizer:
    """
    Класс для реализации процесса бинаризации, описанного в стандарте CABAC H.264/AVC.
    """

    @staticmethod
    def unary_code(symbol):
        """
        Генерирует унарный код для заданного символа.
        :param symbol: Символ для бинаризации.
        :return: Унарный бинарный код.
        """
        # Унарный код для числа n - это n единиц, за которыми следует ноль
        return '1' * symbol + '0'

    @staticmethod
    def truncated_unary_code(symbol, cutoff):
        """
        Генерирует усеченный унарный код для заданного символа.
        :param symbol: Символ для бинаризации.
        :param cutoff: Предельное значение для усеченного унарного кода.
        :return: Усеченный унарный бинарный код.
        """
        return '1' * min(symbol, cutoff) + ('0' if symbol < cutoff else '')

    @staticmethod
    def exp_golomb_code(symbol, order):
        """
        Генерирует код k-го порядка Exp-Golomb для заданного символа.
        :param symbol: Символ для бинаризации.
        :param order: Порядок 'k' кода Exp-Golomb.
        :return: Бинарный код Exp-Golomb.
        """
        prefix_length = (symbol >> order) + 1  # количество единиц в префиксе
        prefix = '1' * prefix_length + '0'
        suffix = f"{symbol & ((1 << order) - 1):0{order}b}" if order > 0 else ''
        return prefix + suffix

    @staticmethod
    def fixed_length_code(symbol, length):
        """
        Генерирует фиксированный бинарный код для заданного символа.
        :param symbol: Символ для бинаризации.
        :param length: Длина бинарного кода.
        :return: Фиксированный бинарный код.
        """
        return f"{symbol:0{length}b}"

    def binarize(self, symbol, method, **kwargs):
        """
        Бинаризирует входной символ в соответствии с указанным методом бинаризации.
        :param symbol: Символ для бинаризации.
        :param method: Метод бинаризации ('unary', 'truncated_unary', 'exp_golomb', 'fixed_length').
        :return: Бинарная строка.
        """
        if method == 'unary':
            return self.unary_code(symbol)
        elif method == 'truncated_unary':
            cutoff = kwargs.get('cutoff', symbol)  # по умолчанию весь символ
            return self.truncated_unary_code(symbol, cutoff)
        elif method == 'exp_golomb':
            order = kwargs.get('order', 0)
            return self.exp_golomb_code(symbol, order)
        elif method == 'fixed_length':
            length = kwargs.get('length')
            return self.fixed_length_code(symbol, length)
        else:
            raise ValueError(f"Неизвестный метод бинаризации: {method}")


# Пример использования:
binarizer = Binarizer()

# Бинаризация символа с использованием унарного кода
print(binarizer.binarize(5, 'unary'))
# Бинаризация символа с использованием усеченного унарного кода
print(binarizer.binarize(5, 'truncated_unary', cutoff=3))
# Бинаризация символа с использованием кода Exp-Golomb
print(binarizer.binarize(14, 'exp_golomb', order=2))
# Бинаризация символа с использованием фиксированной длины
print(binarizer.binarize(5, 'fixed_length', length=4))
