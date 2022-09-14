from dataclasses import dataclass

@dataclass(frozen=True)
class public_key:
    
    '''Defines a public key'''

    identity : str
    param : dict

    def __str__(self):
        '''Converts public key to a readable formatted string'''
        return "\n\tParameters:\n{}".format(
            "\n".join( ["\t\t" + str(key) + " : " + hex(val) for key, val in self.param.items()])
        )