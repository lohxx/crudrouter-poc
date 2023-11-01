
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
        if not value:
            return '()'
        if type(value) == list:
            join_str = []
            for item in value:
                if type(item) == str:
                    join_str.append(f"'{item}'")
                else:
                    join_str.append(f"{item}")

            return f"({','.join(join_str)})"

        elif type(value) == str:
            return f"({value})"

        return f'({value})'
    

class BetweenFilter(BaseFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def __repr__(self):
        return 'BETWEEN'
    
    def converter(self, value):
        min, max = value
        return f"'{min}' AND '{max}'"

class FilterNotSupported(Exception):
    pass

OPERATORS = {
    '$eq': EqFilter,
    '$lt': LtFilter,
    '$gt': GtFilter,
    '$ne': NeFilter,
    '$in': InFilter,
    '$gte': GteFilter,
    '$between': BetweenFilter,
}
