from typing import List, Tuple, Optional


def get_flag_values_from_args(args: Tuple[str], flag: List[str]) -> Optional[str]:
    for i, arg in enumerate(args):
        if arg in flag:
            try:
                return args[i + 1]
            except IndexError:
                return None
    return None
