import numpy as np
from binarization import exp_golomb_coding
from adaptiveEncode import AdaptiveArithmeticEncoder
from contextModel import ContextModel


class CABAC:

    def __init__(self):
        self.context_model = ContextModel()
        self.arithmetic_encoder = AdaptiveArithmeticEncoder(self.context_model)

    def encode(self, data_block):
        """
        Кодирует блок данных с использованием CABAC, применяя дифференциальное кодирование и контекстно-зависимую бинаризацию.
        """
        self.context_model.evaluate_data_characteristics(data_block)

        # Дифференциальное кодирование
        diff_encoded_block = self.differential_encode(data_block)

        # Подготовка последовательности для арифметического кодирования
        sequence = self.prepare_sequence(diff_encoded_block)

        # Кодирование последовательности
        encoded_value = self.arithmetic_encoder.encode_sequence(sequence)

        return encoded_value

    def differential_encode(self, data_block):
        """
        Применяет дифференциальное кодирование к блоку данных.
        """
        diff_sequence = [data_block[0]]
        for i in range(1, len(data_block)):
            diff_sequence.append(data_block[i] - data_block[i-1])
        return np.array(diff_sequence)

    def prepare_sequence(self, data_block):
        """
        Подготавливает последовательность для кодирования, используя контекстно-зависимую бинаризацию.
        """
        sequence = []
        for value in np.nditer(data_block):
            # Контекстно-зависимая бинаризация
            if self.context_model.current_context == 'uniform':
                binary_value = exp_golomb_coding(int(value))
            else:
                # Здесь можно реализовать другие методы бинаризации
                binary_value = exp_golomb_coding(int(value))
            sequence.extend([int(bit) for bit in binary_value])

        for bit in sequence:
            self.context_model.update_model(bit)

        return sequence

