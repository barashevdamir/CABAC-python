class BypassCodingEngine:
    """
    Класс, отвечающий за байпасное кодирование в CABAC.
    В байпасном режиме бины кодируются без использования адаптации контекста.
    """
    def __init__(self):
        self.buffer = []
        self.buffer_limit = 16
        self.bitstream = bytearray()  # Байтовый массив для хранения выходного потока

    def encode(self, bin_value):
        """
        Кодирует один бит в байпасном режиме.

        Args:
        bin_value (int): Бинарное значение (0 или 1) для кодирования.

        Returns:
        str: Кодированное значение бита в виде строки, поскольку это байпасное кодирование,
             возвращаемое значение идентично входному.
        """
        if bin_value not in [0, 1]:
            raise ValueError("Бинарное значение должно быть 0 или 1 для байпасного кодирования.")

        # В байпасном режиме кодируемый бит не изменяется
        self.buffer.append(bin_value)
        if len(self.buffer) >= self.buffer_limit:
            self.flush_buffer()
        return bin_value

    def flush_buffer(self):
        """
        Записывает содержимое буфера в битовый поток и очищает буфер.
        """
        while len(self.buffer) >= 8:
            # Собираем первые 8 бит из буфера для создания одного байта
            byte_bits = self.buffer[:8]
            byte_value = 0
            for bit in byte_bits:
                byte_value = (byte_value << 1) | bit
            self.buffer = self.buffer[8:]  # Удаляем обработанные биты из буфера

            # Записываем байт в выходной поток
            self.write_byte(byte_value)

        # Если в буфере остались биты, которых недостаточно для формирования байта
        if self.buffer:
            # Собираем оставшиеся биты в байт, добавляя в конец нули
            byte_value = 0
            for bit in self.buffer:
                byte_value = (byte_value << 1) | bit
            byte_value <<= (8 - len(self.buffer))  # Сдвигаем биты влево
            self.write_byte(byte_value)
            self.buffer = []  # Очищаем буфер

    def write_byte(self, byte_value):
        """
        Записывает байт в выходной поток.

        Args:
        byte_value (int): Байт для записи, представленный целым числом.
        """
        # Переводим байт в битовую строку
        bit_string = format(byte_value, '08b')
        # Здесь записываем битовую строку в битовый поток
        self.write_to_bitstream(bit_string)

    def write_to_bitstream(self, bit_string):
        """
        Записывает битовую строку в байтовый массив.

        Args:
        bit_string (str): Строка из нулей и единиц для записи.
        """
        # Дополним битовую строку до полного байта, если она не кратна 8
        while len(bit_string) % 8 != 0:
            bit_string += '0'  # Дополняем нулями до полного байта

        # Преобразовываем битовую строку в байты и добавляем в байтовый поток
        self.bitstream.extend(int(bit_string[i:i+8], 2).to_bytes(1, byteorder='big') for i in range(0, len(bit_string), 8))

    def flush_bitstream(self):
        """
        Записывает байтовый поток в файл или другой выходной интерфейс.
        """
        with open('output.bitstream', 'ab') as f:  # Открываем файл для добавления данных
            f.write(self.bitstream)

        self.bitstream = bytearray()  # Очистим байтовый массив после записи

    def get_bitstream(self):
        """
        Возвращает собранный битовый поток.

        Returns:
        bytearray: Байтовый массив с битовым потоком.
        """
        # Возвращаем копию битового потока, чтобы предотвратить его изменение извне
        return bytearray(self.bitstream)

    def finalize(self):
        # При необходимости очистка буфера при завершении кодирования
        if self.buffer:
            self.flush_buffer()
