class Helper:

    @staticmethod
    def find_column_position(line, column_name):
        for i, column in enumerate(line):
            if column.strip().lower() == column_name:
                return i
        print(line)
        raise Exception(f'Could find find {column_name}')
