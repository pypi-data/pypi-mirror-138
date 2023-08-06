__author__ = "Zedikon"
__copyright__ = "Copyright zedikon 2022, all rights reserved."
__version__ = "1.0.23"
__emal__ = "mrzedikon@gmail.com"

stack = []

# lexems

tokens = {
    "meaning": ":",
    "string": "str:",
    "integer": "int:",
    "eval": "do:",
    "hex": "hex:",
    "float": "float:",
    "comments": "//",
    "next": ";"
}

# lexer

def load(variable):
    try:
        stack.append(variable)
        strstack = tokens["next"].join(stack)
        global result
        result = strstack.split()
        global positionscomments
        positionscomments = result.index(tokens["comments"])
    except Exception:
        return f"PECF: Sorry, but i can't find {variable} variable"

# parser

def decode(name):
    try:
        positions = result.index(name + ":")
    except Exception:
        return f"PECF: Sorry, but i can't find {name} variable"
    try:
        try:
            result.pop(positionscomments + 1)
            result.pop(positionscomments)
            result.append("SUCESSZ_TOKENSSS05_0320421")
            endcomments = result.index("SUCESSZ_TOKENSSS05_0320421")
            result.pop(endcomments)
        except Exception:
            pass
        if result[positions + 1] == tokens["string"]:
            res = str(result[positions + 2])
            return res
        try:
            if result[positions + 1] == tokens["integer"]:
                res = int(result[positions + 2])
                return res

            if result[positions + 1] == tokens["eval"]:
                res = eval(result[positions + 2])
                return res

            if result[positions + 1] == tokens["float"]:
                res = float(result[positions + 2])
                return res
        except Exception:
            return "PECF: Sorry, but invalid value entered!"
        try:
            if result[positions + 1] == tokens["hex"]:
                res = int(result[positions+2])
                return hex(res)
        except Exception:
            try:
                res = result[positions + 2]
                return int(res, 16)
            except Exception:
                return "PECF: Sorry, but invalid value entered!"
        else:
            return result[positions + 1]
    except Exception:
            return "PECF: Sorry, but critical error in PECF script!"
