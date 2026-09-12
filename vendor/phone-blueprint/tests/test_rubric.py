from src.scorer import memorability_score, spoken_score
from src.decision_engine import Intent, recommend_architecture

def test_pattern_beats_random():
    assert memorability_score("+44330112244") > memorability_score("+44330583719")

def test_local_trade_with_sms_splits_channels():
    x = Intent(
        locality_is_purchase_signal=.95,
        national_identity_value=.3,
        expected_expansion=.2,
        trust_sensitivity=.9,
        sms_required=True,
        same_number_sms_required=False,
    )
    r = recommend_architecture(x)
    assert r["primary"] == "local"
    assert r["secondary"] == "mobile"

def test_same_number_sms_pushes_mobile():
    x = Intent(
        locality_is_purchase_signal=.9,
        national_identity_value=.2,
        expected_expansion=.2,
        trust_sensitivity=.8,
        sms_required=True,
        same_number_sms_required=True,
    )
    assert recommend_architecture(x)["primary"] == "mobile"

def test_national_brand_prefers_national():
    x = Intent(
        locality_is_purchase_signal=.05,
        national_identity_value=.95,
        expected_expansion=.95,
        trust_sensitivity=.7,
        sms_required=True,
    )
    assert recommend_architecture(x)["primary"] == "national"
