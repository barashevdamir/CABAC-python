import numpy as np
from binarizer import Binarizer
from regular_coding import RegularCodingEngine
from bypass_coding import BypassCodingEngine
from context_modeler import ContextModeler


class CABAC:

    def __init__(self):
        self.context_modeler = ContextModeler()
        self.regular_coding_engine = RegularCodingEngine(self.context_modeler)
        self.bypass_coding_engine = BypassCodingEngine()
        self.binarizer = Binarizer()

    def encode(self, data_block):
        bitstream = bytearray()

        for value in np.nditer(data_block):
            # Бинаризация значения
            bin_string = self.binarizer.binarize(int(value))

            for bin_value in bin_string:
                # Определение, какой движок кодирования использовать
                if self.context_modeler.should_use_bypass(bin_value):
                    # Использование BypassCodingEngine для бинарных значений, которые следует кодировать напрямую
                    coded_bits = self.bypass_coding_engine.encode(bin_value)
                else:
                    # Использование RegularCodingEngine для бинарных значений, требующих контекстной модели
                    coded_bits = self.regular_coding_engine.encode(bin_value, self.context_modeler.get_probabilities())

                # Добавление закодированных битов в итоговый битовый поток
                bitstream.extend(coded_bits)

        # Возвращаем битовый поток как результат кодирования блока
        return bitstream

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

