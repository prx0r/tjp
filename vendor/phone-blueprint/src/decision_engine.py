"""Provider-independent first-pass UK number strategy inference."""
from dataclasses import dataclass
from typing import List

@dataclass
class Intent:
    locality_is_purchase_signal: float = 0.0
    national_identity_value: float = 0.0
    expected_expansion: float = 0.0
    trust_sensitivity: float = 0.5
    free_to_caller_value: float = 0.0
    inbound_call_importance: float = 0.5
    cost_sensitivity: float = 0.5
    sms_required: bool = False
    same_number_sms_required: bool = False
    personal_mobile_identity_value: float = 0.0

def strategy_scores(x: Intent) -> dict:
    local = (
        .40*x.locality_is_purchase_signal
        + .15*x.trust_sensitivity
        - .30*x.expected_expansion
    )
    national = (
        .35*x.national_identity_value
        + .30*x.expected_expansion
        - .20*x.locality_is_purchase_signal
    )
    mobile = (
        .55*(1.0 if x.sms_required else 0.0)
        + .20*x.personal_mobile_identity_value
        - .15*x.trust_sensitivity
    )
    toll_free = (
        .45*x.free_to_caller_value
        + .25*x.inbound_call_importance
        + .15*x.national_identity_value
        - .20*x.cost_sensitivity
    )

    if x.same_number_sms_required:
        # Current Telnyx GB policy makes non-mobile SMS-invalid.
        local -= 10
        national -= 10
        toll_free -= 10

    return {"local": local, "national": national, "mobile": mobile, "toll_free": toll_free}

def recommend_architecture(x: Intent) -> dict:
    scores = strategy_scores(x)
    primary = max(scores, key=scores.get)
    secondary = None
    reason = []
    if x.sms_required and primary in {"local","national","toll_free"}:
        secondary = "mobile"
        reason.append("Separate GB mobile messaging DID because current Telnyx GB guidance does not support SMS on local/national/toll-free.")
    return {"primary": primary, "secondary": secondary, "scores": scores, "reasons": reason}
