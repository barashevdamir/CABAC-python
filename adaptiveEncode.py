class AdaptiveArithmeticEncoder:
    def __init__(self, context_model):
        self.context_model = context_model  # Интеграция модели контекста
        self.symbol_models = self.init_symbol_models()

    def init_symbol_models(self):
        # Инициализация адаптивных моделей для каждого символа
        symbol_models = {}
        for symbol in range(256):  # Пример для 256 символов
            symbol_models[symbol] = [1, 1]  # Исходные вероятности для 0 и 1
        return symbol_models

    def encode_sequence(self, sequence, data_characteristics):
        """
        Кодирует последовательность символов, адаптируя вероятности на лету.

        Args:
        sequence (list of int): Последовательность символов для кодирования.
        data_characteristics (str): Характеристика данных ('low', 'medium', 'high').

        Returns:
        list of float: Список кодированных значений для каждого символа.
        """
        encoded_values = []

        for symbol in sequence:
            prob_0, prob_1 = self.context_model.get_probabilities()
            # Кодирование текущего символа
            encoded_value = self._encode_symbol(symbol, prob_0, prob_1)
            encoded_values.append(encoded_value)

            # Обновление счетчиков и вероятностей в контекстной модели
            self.context_model.update_model(symbol)

        return encoded_values

    def get_symbol_probabilities(self, symbol):
        # Получение вероятностей для конкретного символа
        model = self.symbol_models[symbol]
        total = sum(model)
        return model[0] / total, model[1] / total

    def _encode_symbol(self, symbol, prob_0, prob_1):
        """
        Кодирует один символ с использованием текущей вероятности для 0.

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
            low = low + (high - low) * prob_0

        # Возврат середины интервала
        return (low + high) / 2

