"""Telnyx integration skeleton.

Keep this thin. The official SDK/OpenAPI is the source of truth; do not invent fields.
This file intentionally does not execute live spend.
"""
import os

def search_filters(*, number_type: str, locality: str|None=None,
                   features: list[str]|None=None, limit: int=100,
                   reservable: bool=True, exclude_held: bool=True) -> dict:
    f = {
        "country_code": "GB",
        "phone_number_type": number_type,
        "limit": limit,
        "reservable": reservable,
        "exclude_held_numbers": exclude_held,
    }
    if locality:
        f["locality"] = locality
    if features:
        f["features"] = features
    return f

def live_search_example():
    # from telnyx import Telnyx
    # client = Telnyx(api_key=os.environ["TELNYX_API_KEY"])
    # return client.available_phone_numbers.list(filter=search_filters(number_type="national"))
    raise RuntimeError("Example only: wire to official Telnyx SDK after validating current SDK parameter shape.")

def order_example(phone_number: str, *, connection_id=None, messaging_profile_id=None,
                  customer_reference=None):
    # MUST execute only after human approval + fresh search + compliance preflight.
    # client.number_orders.create(
    #     phone_numbers=[{"phone_number": phone_number}],
    #     connection_id=connection_id,
    #     messaging_profile_id=messaging_profile_id,
    #     customer_reference=customer_reference,
    # )
    raise RuntimeError("Spend path intentionally disabled in blueprint.")
