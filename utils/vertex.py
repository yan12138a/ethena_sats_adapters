import os
import json
import requests
import time
from dotenv import load_dotenv
from utils.web3_utils import (
    w3_arb,
)

from constants.vertex import VERTEX_SPOT_ENGINE_ADDRESS_ARBITRUM

with open("abi/vertex_spot_engine.json") as f:
    spot_engine_abi = json.load(f)

spot_engine_contract = w3_arb.eth.contract(
    address=VERTEX_SPOT_ENGINE_ADDRESS_ARBITRUM, abi=spot_engine_abi
)


def fetch_subaccounts_with_retry(url: str, address: str, retries: int = 3) -> list:
    start = 0
    LIMIT = 500
    subaccounts = []
    while True:
        req = {
            "subaccounts": {
                "start": start,
                "limit": LIMIT,
            }
        }
        if address is not None:
            req["subaccounts"]["address"] = address
        for t in range(0, retries + 1):
            try:
                resp = requests.post(url, json=req)
            except:
                print("failed to get response of request " + str(req), "retrying...")
                time.sleep(10)
                continue
            break
        resp = json.loads(resp.text)
        for subaccount in resp["subaccounts"]:
            subaccounts.append(subaccount["subaccount"])
        if len(resp["subaccounts"]) < LIMIT:
            break
        start += LIMIT
    return subaccounts
