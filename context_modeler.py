# Таблица инициализации состояний вероятностей для различных контекстов.
PROBABILITY_STATES = [{'state_index': i, 'mps': 0} for i in range(64)]

# Сопоставление синтаксических элементов с диапазонами индексов контекста для разных типов срезов
SYNTAX_ELEMENT_TO_CONTEXT_INDEX = {
    'mb_type': {'I': (0, 10), 'P': (14, 20), 'B': (27, 35)},
    'mb_skip_flag': {'I': (), 'P': (11, 13), 'B': (24, 26)},
    'sub_mb_type': {'I': (), 'P': (11, 13), 'B': (24, 26)},
    'mvd (horizontal)': {'I': (), 'P': (40, 46), 'B': (40, 46)},
    'mvd (vertical)': {'I': (), 'P': (47, 53), 'B': (47, 53)},
    'ref_idx': {'I': (), 'P': (54, 59), 'B': (54, 59)},
    'mb_qp_delta': {'I': (60, 63), 'P': (60, 63), 'B': (60, 63)},
    'intra_chroma_pred_mode': {'I': (64, 67), 'P': (64, 67), 'B': (64, 67)},
    'prev_intra4x4_pred_mode_flag': {'I': (68, 68), 'P': (68, 68), 'B': (68, 68)},
    'rem_intra4x4_pred_mode': {'I': (69, 69), 'P': (69, 69), 'B': (69, 69)},
    'mb_field_decoding_flag': {'I': (70, 72), 'P': (70, 72), 'B': (70, 72)},
    'coded_block_pattern': {'I': (73, 84), 'P': (73, 84), 'B': (73, 84)},
    'coded_block_flag': {'I': (85, 104), 'P': (85, 104), 'B': (85, 104)},
    'significant_coeff_flag': {'I': (105, 165, 277, 337), 'P': (105, 165, 277, 337), 'B': (105, 165, 277, 337)},
    'last_significant_coeff_flag': {'I': (166, 226, 338, 398), 'P': (166, 226, 338, 398), 'B': (166, 226, 338, 398)},
    'coeff_abs_level_minus1': {'I': (227, 275), 'P': (227, 275), 'B': (227, 275)},
    'end_of_slice_flag': {'I': (276, 276), 'P': (276, 276), 'B': (276, 276)}
}

# Значения смещения индекса контекста в зависимости от категории контекста
CONTEXT_CATEGORY_OFFSETS = {
    'coded_block_flag': [0, 4, 8, 12, 16],
    'significant_coeff_flag': [0, 15, 29, 44, 47],
    'last_significant_coeff_flag': [0, 15, 29, 44, 47],
    'coeff_abs_level_minus1': [0, 10, 20, 30, 39]
}


# Таблица сопоставления базовых блоков с количеством коэффициентов и ассоциированными категориями контекста
BASIC_BLOCK_TYPES = {
    'Luma DC block for Intra16x16': {'MaxNumCoeff': 16, 'ctx_cat': 0},
    'Luma AC block for Intra16x16': {'MaxNumCoeff': 15, 'ctx_cat': 1},
    'Luma block for Intra4x4': {'MaxNumCoeff': 16, 'ctx_cat': 2},
    'Luma block for Inter': {'MaxNumCoeff': 16, 'ctx_cat': 2},
    'U-Chroma DC block for Intra': {'MaxNumCoeff': 4, 'ctx_cat': 3},
    'V-Chroma DC block for Intra': {'MaxNumCoeff': 4, 'ctx_cat': 3},
    'U-Chroma DC block for Inter': {'MaxNumCoeff': 4, 'ctx_cat': 3},
    'V-Chroma DC block for Inter': {'MaxNumCoeff': 4, 'ctx_cat': 3},
    'U-Chroma AC block for Intra': {'MaxNumCoeff': 15, 'ctx_cat': 4},
    'V-Chroma AC block for Intra': {'MaxNumCoeff': 15, 'ctx_cat': 4},
    'U-Chroma AC block for Inter': {'MaxNumCoeff': 15, 'ctx_cat': 4},
    'V-Chroma AC block for Inter': {'MaxNumCoeff': 15, 'ctx_cat': 4},
}


class ContextModeler:
    """
    Класс для реализации моделирования контекста в соответствии со стандартом CABAC H.264/AVC.
    """

    def __init__(self, num_contexts, slice_type='P', slice_qp=26):
        """
        Инициализация модели контекста.

        :param num_contexts: Количество контекстных моделей.
        :param slice_type: Тип среза ('P', 'B', 'I').
        :param slice_qp: Параметр квантования для среза.
        """
        self.num_contexts = num_contexts
        self.context_models = [None] * num_contexts
        self.slice_type = slice_type
        self.slice_qp = slice_qp
        self._initialize_context_models()

    def _initialize_context_models(self):
        for i in range(len(self.context_models)):
            # Инициализация каждой контекстной модели с начальным состоянием вероятности
            self.context_models[i] = PROBABILITY_STATES[i % len(PROBABILITY_STATES)]

    def get_context_index(self, syntax_element, bin_idx, ctx_cat):
        # Получение начального и конечного индекса для данного синтаксического элемента
        range_start, range_end = SYNTAX_ELEMENT_TO_CONTEXT_INDEX[syntax_element][self.slice_type]
        # Получение смещения для данной категории контекста
        offset = CONTEXT_CATEGORY_OFFSETS[syntax_element][ctx_cat]
        # Вычисление контекстного индекса
        context_index = range_start + offset + bin_idx
        return context_index



