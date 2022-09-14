import json
from jsonschema import validate, exceptions
from blockchain import blockchain
from core.util.json import json_schema

def banner():
    '''Shows banner'''

    with open("banner", "r") as f:
        print(f.read())

def custom_validate(settings : dict):
    
    '''Makes some checks on settings'''
    
    evil_fair =  settings["general"]['n_evils'] <= settings["general"]['n_miners']
    
    if evil_fair:
        
        mbl = settings["general"]["modulus_bit_length"]
        type = settings["general"]["type"]
        tmp_1 = [ settings["PRNG"]["a"],  settings["PRNG"]["b"]]
        flag_1 = all([ x < 2**mbl for x in tmp_1])
        if flag_1:    
            
            flag_2 = True
            
            if type == "ECDSA" :
                tmp_2 = [ settings["ECDSA"]["Gx"], settings["ECDSA"]["Gy"],
                          settings["ECDSA"]["n"], settings["ECDSA"]["q"]  ]
                flag_2 = all([ x < 2**mbl for x in tmp_2])
            
            if flag_2:
                return True, "Config file OK"
            return False, "ECDSA values invalid"
        
        return False, "PRNG values invalid"

    return False, "n_evils must be less than n_miners"
        


if __name__ == '__main__':
    
    banner()
    with open("config.json", "r") as f:
        settings = json.loads(f.read())

    try:
        validate( instance = settings, schema = json_schema)
        ok, msg = custom_validate(settings)
        if ok :
            print(msg)
            b = blockchain(settings)
            b.start()
        else:
            print(msg)
    except exceptions.ValidationError as err:
        print(err)