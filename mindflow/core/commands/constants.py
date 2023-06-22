from enum import Enum


class MinimumReservedLength(Enum):
    CHAT = 500
    QUERY = 500
    DIFF = 600


COAUTH_MSG = "Co-authored-by: MindFlow <mf@mindflo.ai>"
