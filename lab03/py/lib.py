import subprocess as sp
from typing import Dict

SUCCESS: int = 0
NOT_ENOUGH_ARGS: int = 1
TOO_MANY_ARGS: int = 2
WRONG_OPERATION: int = 3
WRONG_KEY: int = 4
FAILED_TO_READ_FILE: int = 5
FAILED_TO_WRITE_FILE: int = 6
CODE_MEANINGS: Dict[int, str] = {
    SUCCESS: "SUCCESS",
    NOT_ENOUGH_ARGS: "NOT ENOUGH ARGS",
    TOO_MANY_ARGS: "TOO MANY ARGS",
    WRONG_OPERATION: "WRONG OPERATION",
    WRONG_KEY: "WRONG KEY",
    FAILED_TO_READ_FILE: "FAILED TO READ FILE",
    FAILED_TO_WRITE_FILE: "FAILED TO WRITE FILE",
}


def code_meaning(code: int) -> str:
    try:
        return CODE_MEANINGS[code]
    except Exception:
        return "UNKNOWN"

    
def do_work(path: str, op: str, key: str, input:str, output: str) -> int:
    p = sp.Popen([path, op, key, input, output])
    p.wait()
    return p.returncode