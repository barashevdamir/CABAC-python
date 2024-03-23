class AdaptiveArithmeticEncoder:
    def __init__(self):
        self.prob_0 = 0.5  # Начальная вероятность символа 0

    def encode_sequence(self, sequence):
        """
        Кодирует последовательность символов, адаптируя вероятности на лету.

        Args:
        sequence (list of int): Последовательность символов для кодирования.

        Returns:
        list of float: Список кодированных значений для каждого символа.
        """
        encoded_values = []
        counts = {0: 1, 1: 1}  # Псевдосчеты для избегания деления на ноль

        for symbol in sequence:
            # Кодирование текущего символа
            encoded_value = self._encode_symbol(symbol, self.prob_0)
            encoded_values.append(encoded_value)

            # Обновление счетчиков и вероятностей
            counts[symbol] += 1
            self.prob_0 = counts[0] / sum(counts.values())

        return encoded_values

    def _encode_symbol(self, symbol, prob_0):
        """
        Кодирует один символ с использованием заданной вероятности для 0.

        Args:
        symbol (int): Символ для кодирования.
        prob_0 (float): Вероятность символа 0.

        Returns:
        float: Кодированное значение символа.
        """
        if symbol not in [0, 1]:
            raise ValueError("Symbol must be 0 or 1")

        # Начальный интервал [0, 1)
        low = 0.0
        high = 1.0

        # Адаптация интервала
        if symbol == 0:
            high = low + prob_0
        else:
            low = low + prob_0

        # Возврат середины интервала
        return (low + high) / 2


# # Пример использования
# encoder = AdaptiveArithmeticEncoder()
# sequence = [0, 1, 0, 0, 1, 1, 0, 1, 1, 0]
# encoded_sequence = encoder.encode_sequence(sequence)
# print("Encoded sequence:", encoded_sequence)
