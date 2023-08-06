from typing import Any


class ControlResult:
    def __init__(self, control:dict[str,Any] = None, offenderDetails:list[dict] = None) -> None:
        if control:
            self.control = control
            offenders = self.control['offenders']
            if len(offenders) > 0:
                self.control['offenders'] = set(offenders)
        else:
            self.control = {}
        if offenderDetails:
            self.offenderDetails = offenderDetails
        else:
            self.offenderDetails = []