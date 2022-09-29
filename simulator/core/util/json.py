json_schema = {
        "type" : "object",
        "properties" : {
            "general" : {
                "type" : "object",
                "additionalProperties": False,
                "minProperties": 10,
                "properties" : {
                    "type" : { "enum" : ['RSA', 'ECDSA'] },
                    "distr" : { "enum" : ['uniform', 'binom'] },
                    "n_blocks" : { "type" : "integer",  "minimum" : 0, "maximum" : 500},
                    "n_miners" : { "type" : "integer",  "minimum" : 0, "maximum" : 16},
                    "n_evils" : { "type" : "integer",  "minimum" : 0, "maximum" : 16},
                    "n_users" : { "type" : "integer",  "minimum" : 0, "maximum" : 100},
                    "modulus_bit_length" : { "enum" : [256, 512] },
                    "w" : { "type" : "integer",  "minimum" : 0, "maximum" : 1024},
                    "max_tx" : { "type" : "integer",  "minimum" : 0, "maximum" : 10},
                    "base_diff" : { "type" : "integer",  "minimum" : 0, "maximum" : 20},
                }
            },
            "PRNG" : {
                "type" : "object",
                "additionalProperties": False,
                "minProperties": 3,
                "properties" : {
                    "a" : { "type" : "integer", "minimum" : 0},
                    "b" : { "type" : "integer", "minimum" : 0 },
                    "n" : { "type" : "integer", "minimum" : 0 },
                    "X" : { "type" : "integer", "minimum" : 0,  "minimum" : 0, "maximum" : 100},
                }
            },
            "ECDSA" : {
                        "type" : "object",
                        "additionalProperties": False,
                        "minProperties": 4,
                        "properties" : {
                            "Gx" : {"type" : "integer", "minimum" : 0 },
                            "Gy" : {"type" : "integer", "minimum" : 0 },
                            "n" : {"type" : "integer", "minimum" : 0 },
                            "q" : {"type" : "integer", "minimum" : 0 }
                        }
            },

            "if": {
                "properties": { "general": { "properties": {  "mode" : { "const" : "ECDSA" } } } }
            },
            "then": {
                "required" : ["ECDSA"]
            },
        }
    }

json_alias = {
            "general" : {
                "type" : "Protocol type",
                "distr" : "Fuzzy secret key distribution",
                "n_blocks" : "Number of blocks",
                "n_miners" : "Number of miners",
                "n_evils" : "Number of evil miners",
                "n_users" : "Number of users",
                "w" : "w parameter",
                "X" : "X parameter",
                "modulus_bit_length" : "Modulus bit length",
                "max_tx" : "Maximum number of transactions per block",
                "base_diff" : "Base CPoW difficulty"
            },
            "PRNG" : {
                "a" : "PRNG a parameter",
                "b" : "PRNG b parameter",
                "n" : "PRNG n parameter",
                "X" : "PRNG X parameter",
            },
            "ECDSA" : {
                "Gx" : "ECDSA Gx parameter",
                "Gy" : "ECDSA Gy parameter",
                "n" : "ECDSA n parameter",
                "q" : "ECDSA q parameter",
            }
    }