from dataclasses import dataclass

@dataclass(frozen=True)
class signature:
    '''Defines a signature'''

    param : dict

    def get_hex_param(self):
        '''Returns signature parameters in hexadecimal format'''
        return { key : hex(val) for key, val in self.param.items() }