
class BaseFilter:
    def __init__(self, **kwargs):
        self.types = [str, int, bool]
    
    def __repr__(self):
        return ''
    
    def converter(self, value):
        if type(value) == str:
            return f"'{value}'"
        return value
    

class EqFilter(BaseFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def __repr__(self):
        return '='


class LtFilter(BaseFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def __repr__(self):
        return '<'


class GtFilter(BaseFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.types = [int, str, bool]
    
    def __repr__(self):
        return '>'
    

class NeFilter(BaseFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def __repr__(self):
        return '!='


class GteFilter(BaseFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def __repr__(self):
        return '>='
    

class InFilter(BaseFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def __repr__(self):
        return 'IN'
    
    def converter(self, value):
        if type(value) == list:
            join_str = ''
            for item in value:
                if type(item) == str:
                    join_str += f"'{item}',"
                else:
                    join_str += f"{item},"

            return f"({join_str})"

        elif type(value) == str:
            return f"({value})"

        return f'({value})'
    

class FilterNotSupported(Exception):
    pass

OPERATORS = {
    '$eq': EqFilter,
    '$lt': LtFilter,
    '$gt': GtFilter,
    '$ne': NeFilter,
    '$in': InFilter,
    '$gte': GteFilter,
}
