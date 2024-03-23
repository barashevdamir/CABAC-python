import numpy as np

class ContextModel:
    def __init__(self):
        # Инициализируем контексты для различных типов данных
        self.contexts = {
            'edge': [1, 1],  # Для краев или границ
            'texture': [1, 1],  # Для текстурных областей
            'uniform': [1, 1]  # Для однородных областей
        }
        self.current_context = 'uniform'  # Установка исходного контекста
        # Инициализация порогов для классификации активности
        self.low_threshold = 10
        self.high_threshold = 30

    def update_context(self, data_type):
        """
        Обновляет текущий контекст на основе типа данных.

        Args:
        data_type (str): Тип данных ('edge', 'texture', 'uniform').
        """
        if data_type not in self.contexts:
            # Динамическое создание нового контекста при необходимости
            self.contexts[data_type] = [1, 1]
        self.current_context = data_type

    def update_model(self, bit):
        """
        Обновляет модель для текущего контекста, добавляя встреченный бит.

        Args:
        bit (int): Бит, который нужно добавить в модель (0 или 1).
        """
        self.contexts[self.current_context][bit] += 1

    def get_probabilities(self):
        """
        Возвращает вероятности для текущего контекста.

        Returns:
        tuple: Кортеж, содержащий вероятности появления бита 0 и бита 1.
        """
        context = self.contexts[self.current_context]
        total = sum(context)
        prob_0 = context[0] / total
        prob_1 = context[1] / total
        return prob_0, prob_1

    def evaluate_data_characteristics(self, block):
        # Расчёт стандартного отклонения в блоке
        std_dev = np.std(block)

        # Адаптивная настройка порогов и классификация активности
        if std_dev < self.low_threshold:
            self.update_context('uniform')
        elif std_dev > self.high_threshold:
            self.update_context('texture')
        else:
            self.update_context('edge')

        return self.current_context

