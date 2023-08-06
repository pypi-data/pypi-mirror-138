from .__main__ import IndeterminateStatute, StatuteLabel
from .assigner import assign
from .formula.provisions import ProvisionLabel
from .matcher import (
    match_provision,
    match_provisions,
    match_statute,
    match_statutes,
)
from .spanner import get_statutory_provision_spans
