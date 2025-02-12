import re

class Lib:
    """
    Class is for various functions
    """
    
    @staticmethod
    def extract_substring_regex(text):
        pattern = r'(?<=\`\`\`sql).*?(?=\`\`\`)'
        match = re.search(pattern, text, flags=re.DOTALL)
        
        if match:
            return match.group()
    
    @staticmethod    
    def add_last_char_if_needed(str,ch):
        if str and (str[-1:] != ch):
            str = str + ch
        return str

    @staticmethod    
    def list_normalize(list_src, symbols_to_replace, char_for_replace):
        
        # Создаем таблицу замен
        trans_table = str.maketrans({symbol: char_for_replace for symbol in symbols_to_replace})
        # Применяем таблицу к каждому элементу списка
        return [item.translate(trans_table) for item in list_src]
    
    @staticmethod    
    def map_without_duplicates(list1, list2):
        return {x : y for x, y in zip(list1, list2) if x != y }