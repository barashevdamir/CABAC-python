import numpy as np

class ContextModel:
    def __init__(self):
        # Инициализируем контексты для различных динамик изменений
        self.context_models = {
            'low': [1, 1],  # Низкая динамика
            'medium': [1, 1],  # Средняя динамика
            'high': [1, 1]  # Высокая динамика
        }
        self.data_characteristics = 'medium'  # Начальная характеристика данных

    def update_model(self, bit, characteristics):
        """
        Обновляет соответствующий контекст, добавляя встреченный бит, на основе характеристик данных.
        """
        self.data_characteristics = characteristics
        self.context_models[characteristics][bit] += 1

    def get_probabilities(self):
        """
        Возвращает вероятности для текущего контекста, основываясь на характеристиках данных.
        """
        context = self.context_models[self.data_characteristics]
        total = sum(context)
        prob_0 = context[0] / total
        prob_1 = context[1] / total
        return prob_0, prob_1

    def evaluate_data_characteristics(self, block):
        """
        Оценивает и обновляет характеристики блока данных (например, блока пикселей),
        анализируя его текстурные и контрастные характеристики.

        Args:
        block (np.array): 2D массив, представляющий блок пикселей.
        """
        # Расчет стандартного отклонения в блоке для оценки текстуры/контраста
        std_dev = np.std(block)

        # Определение порогов для классификации активности
        low_threshold = 10  # Низкая текстурная активность
        high_threshold = 30  # Высокая текстурная активность

        # Классификация активности на основе стандартного отклонения
        if std_dev < low_threshold:
            self.data_characteristics = 'low'
        elif std_dev > high_threshold:
            self.data_characteristics = 'high'
        else:
            self.data_characteristics = 'medium'

        return self.data_characteristics


# # Пример использования
# advanced_context_model = ContextModel()
# bitstream = [0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1]
# characteristics = ['low', 'medium', 'high']  # Пример характеристик для каждого бита
#
# for bit, char in zip(bitstream, characteristics):
#     prob_0, prob_1 = advanced_context_model.get_probabilities()
#     print(f"Probabilities before encoding {bit} [{char}]: 0={prob_0:.2f}, 1={prob_1:.2f}")
#     advanced_context_model.update_model(bit, char)
