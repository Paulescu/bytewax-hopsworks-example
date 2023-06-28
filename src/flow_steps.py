from typing import Tuple, Dict, List, Generator, Any
import json
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
from websocket import create_connection
from bytewax.inputs import ManualInputConfig
from bytewax.dataflow import Dataflow
from bytewax.window import EventClockConfig, TumblingWindowConfig
from bytewax.outputs import ManualOutputConfig

from src.config import PRODUCT_IDS
from src.types import Ticker, FeatureGroupMetadata
from src.date_utils import str2epoch, epoch2datetime
from src.feature_store_api import get_feature_group
from src.logger import get_console_logger

logger = get_console_logger()

def connect_to_input_socket(flow: Dataflow):
    """Connects the given dataflow to the Coinbase websocket

    Args:
        flow (Dataflow): _description_
    """
    def ws_input(product_ids: List[str], state) -> Generator[Tuple[Any, Any], None, None]:
        """Python generator that yields data coming for the websocket for the
        given `product_ids`

        Args:
            product_ids (List[str]): _description_
            state (_type_): _description_

        Yields:
            Generator[Tuple[Any, Any]]: _description_
        """
        ws = create_connection("wss://ws-feed.pro.coinbase.com")
        ws.send(
            json.dumps(
                {
                    "type": "subscribe",
                    "product_ids": product_ids,
                    "channels": ["ticker"],
                }
            )
        )
        # The first msg is just a confirmation that we have subscribed.
        print(ws.recv())
        while True:
            yield state, ws.recv()

    def input_builder(worker_index, worker_count, resume_state):
        """Returns Python generator for each worker

        Args:
            worker_index (_type_): _description_
            worker_count (_type_): _description_
            resume_state (_type_): _description_

        Returns:
            _type_: _description_
        """
        state = resume_state or None
        prods_per_worker = int(len(PRODUCT_IDS) / worker_count)
        product_ids = PRODUCT_IDS[
            int(worker_index * prods_per_worker) : int(
                worker_index * prods_per_worker + prods_per_worker
            )
        ]
        return ws_input(product_ids, state)

    flow.input("input", ManualInputConfig(input_builder))

def parse_string_to_dict(flow: Dataflow):

    flow.map(json.loads)

def set_product_id_as_key(flow: Dataflow):

    def key_on_product(data: Dict) -> Tuple[str, Ticker]:
        """Transform input `data` into a Tuple[product_id, ticker_data]
        where `ticker_data` is a `Ticker` object.

        Args:
            data (Dict): _description_

        Returns:
            Tuple[str, Ticker]: _description_
        """
        ticker = Ticker(
            product_id=data['product_id'],
            ts_unix=str2epoch(data['time']),
            price=data['price'],
            size=data['last_size']
        )
        return (data["product_id"], ticker)

    flow.map(key_on_product)

def add_tumbling_window(flow: Dataflow, window_seconds: int):

    def get_event_time(ticker: Ticker) -> datetime:
        """
        This function instructs the event clock on how to retrieve the
        event's datetime from the input.
        """
        return epoch2datetime(ticker.ts_unix)

    def build_array() -> np.array:
        """_summary_

        Returns:
            np.array: _description_
        """
        return np.empty((0,3))

    def acc_values(previous_data: np.array, ticker: Ticker) -> np.array:
        """
        This is the accumulator function, and outputs a numpy array of time and price
        """
        return np.insert(previous_data, 0,
                        np.array((ticker.ts_unix, ticker.price, ticker.size)), 0)

    # Configure the `fold_window` operator to use the event time
    cc = EventClockConfig(get_event_time, wait_for_system_duration=timedelta(seconds=10))

    start_at = datetime.now(timezone.utc)
    start_at = start_at - timedelta(
        seconds=start_at.second, microseconds=start_at.microsecond
    )
    wc = TumblingWindowConfig(start_at=start_at,length=timedelta(seconds=window_seconds))

    flow.fold_window(f"{window_seconds}_sec", cc, wc, build_array, acc_values)

def aggregate_raw_trades_as_ohlc(flow: Dataflow):

    # compute OHLC for the window
    def calculate_features(ticker_data: Tuple[str, np.array]) -> Tuple[str, Dict]:
        """Aggregate trade data in window

        Args:
            ticker__data (Tuple[str, np.array]): product_id, data

        Returns:
            Tuple[str, Dict]: product_id, Dict with keys
                - time
                - open
                - high
                - low
                - close
                - volume
        """
        ticker, data = ticker_data
        ohlc = {
            "time": data[-1][0],
            "open": data[:,1][-1],
            "high": np.amax(data[:,1]),
            "low":np.amin(data[:,1]),
            "close":data[:,1][0],  
            "volume": np.sum(data[:,2])
        }
        return (ticker, ohlc)

    flow.map(calculate_features)

def compute_tech_indicators(flow: Dataflow):

    # compute technical-indicators
    from src.technical_indicators import BollingerBands
    flow.stateful_map(
        "technical_indicators",
        lambda: BollingerBands(3),
        BollingerBands.compute
    )

def tuple_to_dict(flow: Dataflow):

    def _tuple_to_dict(key__dict: Tuple[str, Dict]) -> Dict:
        key, dict = key__dict
        dict['product_id'] = key

        # TODO: fix this upstream
        dict['time'] = int(dict['time'])

        return dict
     
    flow.map(_tuple_to_dict)


def save_output_to_feature_store(
    flow: Dataflow,
    feature_group_metadata: FeatureGroupMetadata
) -> None:

    class HopsworksOutputConfig(ManualOutputConfig):

        def __new__(cls, feature_group_metadata: FeatureGroupMetadata):
            """In classes defined by PyO3 we can only use __new__, not __init__"""

            # cls.feature_group = get_feature_group(feature_group_metadata)

            def output_builder(wi, wc):

                feature_group = get_feature_group(feature_group_metadata)

                def output_handler(item: Dict):
                    
                    logger.info(f'Saving {item} to online feature store...')

                    # Dict to DataFrame
                    df = pd.DataFrame.from_records([item])

                    # Insert data to online feature store only. No backfill.
                    feature_group.insert(
                        df,
                        write_options={"start_offline_backfill": False}
                    )   

                return output_handler

            return super().__new__(cls, output_builder)
    
    flow.capture(HopsworksOutputConfig(feature_group_metadata))