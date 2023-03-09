from typing import List, Tuple, Optional


def get_flag_value(args: Tuple[str], flag: List[str]) -> Optional[str]:
    """
    Gets the value of a flag in a list of arguments.
    """
    for i, arg in enumerate(args):
        if arg in flag:
            try:
                return args[i + 1]
            except IndexError:
                return None
    return None


def get_flag_bool(args: Tuple[str], flag: str) -> bool:
    """
    Returns True if the flag is in the list of arguments.
    """
    try:
        return args.index(flag) >= 0
    except:
        return False
