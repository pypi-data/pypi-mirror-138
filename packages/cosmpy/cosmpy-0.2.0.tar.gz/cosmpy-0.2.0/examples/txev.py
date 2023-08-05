import re
import time
from dataclasses import dataclass
from threading import Thread
from typing import Any, Dict, List, Optional

from cosmpy.common.rest_client import RestClient
from cosmpy.protos.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest
from cosmpy.protos.cosmwasm.wasm.v1.query_pb2 import QuerySmartContractStateRequest
from cosmpy.protos.cosmwasm.wasm.v1.tx_pb2 import (
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgStoreCode,
)
from cosmpy.tx.rest_client import GetTxsEventRequest, TxRestClient

REST_LOCAL_ENDPOINT = "http://localhost:1317"
REST_CAPRICORN_ENDPOINT = "https://rest-capricorn.fetch.ai:443"


def events_parser(events_list):
    events_dict = {}
    for event in events_list:
        events_dict[event.type] = {}
        for attribute in event.attributes:
            if attribute.key not in events_dict[event.type]:
                events_dict[event.type][attribute.key] = attribute.value
            else:
                if isinstance(events_dict[event.type][attribute.key], list):
                    events_dict[event.type][attribute.key].append(attribute.value)
                else:
                    events_dict[event.type][attribute.key] = [
                        events_dict[event.type][attribute.key],
                        attribute.value,
                    ]
    return events_dict


@dataclass
class ExperimentDetails:
    contract_address: str
    name: str
    votes: Optional[Dict] = None
    current_round: int = 0
    pubkey_submitted: Optional[Dict[str, bool]] = None
    proposers: Optional[Dict] = None
    round_results: Optional[Dict] = None


class EventsPoller:
    """
    Polls the blockchain for new votes in the contracts that it knows about. Polling thread checks votes once per
    second.
    """

    def __init__(self):
        channel = RestClient(REST_CAPRICORN_ENDPOINT)

        self.experiment_details: Dict[str, ExperimentDetails] = dict()
        self.thread = Thread(target=self.main_thread)
        self.tx = TxRestClient(channel)

        self._shutting_down = False
        self.sleep_time = 5

        self.previously_seen: Dict[str, int] = {}

    def main_thread(self):
        while not self._shutting_down:
            self.get_votes()
            self.get_pubkeys()
            self.get_submit_hash()
            self.get_rewards()
            self.get_penalties()
            for _ in range(self.sleep_time):
                time.sleep(1)
                if self._shutting_down:
                    break

    def run(self):
        if self.thread.is_alive() is False:
            self.thread.start()

    def stop(self):
        self._shutting_down = True
        self.thread.join()

    def add_experiment(self, experiment_name):
        contract_address = "fetch18h8ncg9szj3v92cz289qz3ndwqk5zema0ycpyr"
        self.experiment_details[experiment_name] = ExperimentDetails(
            contract_address=contract_address, name=experiment_name
        )

    def remove_experiment(self, experiment_name):
        self.experiment_details.pop(experiment_name, None)

    def get_votes(self):

        for exp in self.experiment_details.values():
            if self._shutting_down:
                break
            event = "wasm.action='vote'"
            event2 = f"wasm._contract_address='{exp.contract_address}'"
            round_index = exp.current_round
            if round_index == 0:
                exp.votes = {}
                exp.round_results = {}

            while not self._shutting_down:
                event3 = f"wasm.round='{round_index}'"
                vote_events = self.get_new_txs_events(
                    events=[event, event2, event3], cache_key="get_votes"
                )

                if len(vote_events) == 0:  # no votes for this round yet
                    exp.current_round = max(0, round_index)
                    break

                round_votes = exp.votes.get(round_index, {})
                for resp in vote_events:
                    evd = events_parser(resp.logs[0].events)
                    round_votes[evd["wasm"]["sender"]] = evd["wasm"]["vote"]
                    if "hash_accepted" in evd["wasm"]:
                        if (
                            exp.round_results.get(round_index, None)
                            != evd["wasm"]["hash_accepted"]
                        ):
                            exp.round_results[round_index] = evd["wasm"][
                                "hash_accepted"
                            ]

                exp.votes[round_index] = round_votes
                round_index += 1

    def get_pubkeys(self):
        for exp in self.experiment_details.values():
            if self._shutting_down:
                break

            # get submit pubkey events
            event = "wasm.action='submit_pubkey'"
            event2 = f"wasm.contract_address='{exp.contract_address}'"
            pubkeys = exp.pubkey_submitted or {}

            events = self.get_new_txs_events(
                events=[event, event2], cache_key="get_pubkeys"
            )
            for resp in events:
                evd = events_parser(resp.logs[0].events)
                pubkeys[evd["wasm"]["sender"]] = True

            # get withdraw pubkey events
            event = "wasm.action='withdraw_pubkey'"

            events = self.get_new_txs_events(
                events=[event, event2], cache_key="get_pubkeys2"
            )
            for resp in events:
                evd = events_parser(resp.logs[0].events)
                pubkeys[evd["wasm"]["sender"]] = False

            exp.pubkey_submitted = pubkeys

    def get_submit_hash(self):
        for exp in self.experiment_details.values():
            if self._shutting_down:
                break

            event = "wasm.action='submit_hash'"
            event2 = f"wasm.contract_address='{exp.contract_address}'"
            proposers = exp.proposers or {}
            if exp.proposers is None:
                exp.proposers = {}

            events = self.get_new_txs_events(
                events=[event, event2], cache_key="submit_hash"
            )
            for resp in events:
                evd = events_parser(resp.logs[0].events)
                proposers[evd["wasm"]["round"]] = (
                    evd["wasm"]["sender"],
                    evd["wasm"]["hash"],
                )

            exp.proposers = proposers

    def get_rewards(self):
        for exp in self.experiment_details.values():
            if self._shutting_down:
                break

            event = "wasm.action='vote'"
            event2 = f"wasm.contract_address='{exp.contract_address}'"

            events = self.get_new_txs_events(
                events=[event, event2], cache_key="get_rewards"
            )
            for resp in events:
                evd = events_parser(resp.logs[0].events)
                # Typical response: {'contract_address': 'fetch1pda040tujlqz634zlwag7wsavm5jzlsx5tgn7q',
                # 'action': 'vote', 'sender': 'fetch1ekte6hj884gmxnxsec3hp3j0mgalruhhdqwfyc', 'vote': 'true',
                # 'round': '7', 'accepted_hash_reward': 'fetch1xateumqmg79vx88ehnvq4utmrx7sa4n0zdhxll:0:Proposal accepted by majority vote',
                # 'hash_accepted': 'true'}
                if "accepted_hash_reward" in evd["wasm"]:
                    if evd["wasm"]["hash_accepted"] == "true":
                        addr, amount, reason = (
                            evd["wasm"]["accepted_hash_reward"] + ":none"
                        ).split(":")[0:3]

    def get_penalties(self):
        for exp in self.experiment_details.values():
            if self._shutting_down:
                break

            event = "wasm.action='submit_hash'"
            event2 = f"wasm.contract_address='{exp.contract_address}'"
            events = self.get_new_txs_events(
                events=[event, event2], cache_key="get_penalties1"
            )

            for resp in events:
                evd = events_parser(resp.logs[0].events)
                if "penalty" in evd["wasm"]:
                    addr, amount, reason = (evd["wasm"]["penalty"] + ":none").split(
                        ":"
                    )[0:3]
                    amount = int(re.search(r"^\d+", amount).group())

            event = "wasm.action='vote'"
            events = self.get_new_txs_events(
                events=[event, event2], cache_key="get_penalties2"
            )

    def get_all_txs_events(self, events: List[str], start_from=0):
        limit = 100

        # find total results
        res = self.tx.GetTxsEvent(
            GetTxsEventRequest(
                events=events,
                pagination=PageRequest(
                    offset=0,
                    limit=1,
                ),
            )
        )
        if res.pagination.total == start_from:
            return [], start_from

        # hack to fix cosmpy's terrible pagination - need to start from a complete page
        start_page = (start_from // limit) * limit
        extras_at_beginning = start_from - start_page

        all_events: List[Any] = []
        offset = start_page
        while len(all_events) < res.pagination.total - start_page:
            res = self.tx.GetTxsEvent(
                GetTxsEventRequest(
                    events=events,
                    pagination=PageRequest(
                        offset=offset,
                        limit=limit,
                    ),
                )
            )
            offset += limit
            all_events.extend(res.tx_responses)

        # remove extra results from beginning (see hack above)
        all_events = all_events[extras_at_beginning:]

        print(
            f"offset {start_from}, total {res.pagination.total}, results returned {len(all_events)}"
        )
        results_seen = res.pagination.total
        return all_events, results_seen

    def get_new_txs_events(self, events: List[str], cache_key: str):
        full_cache_key = "|".join(events + [cache_key])
        if full_cache_key not in self.previously_seen.keys():
            self.previously_seen[full_cache_key] = 0

        new_events, results_seen = self.get_all_txs_events(
            events, start_from=self.previously_seen[full_cache_key]
        )
        self.previously_seen[full_cache_key] = results_seen
        return new_events


poller = EventsPoller()
poller.add_experiment("exp1")
poller.get_votes()
