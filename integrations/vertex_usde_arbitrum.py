from constants.chains import Chain
from constants.integration_ids import IntegrationID
from models.integration import Integration
from utils.web3_utils import call_with_retry
from utils.vertex import spot_engine_contract, fetch_subaccounts_with_retry
from constants.vertex import (
    VETTEX_USDE_PRODUCT_ID_ARBITRUM,
    VERTEX_USDE_DEPLOYMENT_BLOCK,
    VERTEX_ARCHIVE_URL_ARBITRUM,
)


class VertexIntegration(Integration):
    def __init__(self):
        super().__init__(
            IntegrationID.VERTEX_USDE_ARBITRUM,
            VERTEX_USDE_DEPLOYMENT_BLOCK,
            Chain.ARBITRUM,
            None,
            20,
            1,
            None,
            None,
        )

    def get_balance(self, user: str, block: int) -> float:
        subaccounts = fetch_subaccounts_with_retry(VERTEX_ARCHIVE_URL_ARBITRUM, user)
        sum_balance = 0
        for subaccount in subaccounts:
            balance = call_with_retry(
                spot_engine_contract.functions.getBalance(
                    VETTEX_USDE_PRODUCT_ID_ARBITRUM, subaccount
                ),
                block,
            )[0]
            sum_balance += balance if balance > 0 else 0
        return sum_balance / 1e18

    def get_participants(self) -> list:
        subaccounts = fetch_subaccounts_with_retry(VERTEX_ARCHIVE_URL_ARBITRUM, None)
        addresses = set()
        for subaccount in subaccounts:
            addresses.add(subaccount[0:42])
        self.participants = list(addresses)
        return self.participants


if __name__ == "__main__":
    vertex_integration = VertexIntegration()
    participants = vertex_integration.get_participants()
    print(vertex_integration.get_balance(participants[1], "latest"))
