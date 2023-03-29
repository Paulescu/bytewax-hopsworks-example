# pylint: disable=missing-module-docstring
from argparse import ArgumentParser

from bytewax.dataflow import Dataflow
from bytewax.execution import run_main
from bytewax.outputs import StdOutputConfig

from src import config
from src.flow_steps import (
    connect_to_input_socket,
    parse_string_to_dict,
    set_product_id_as_key,
    add_tumbling_window,
    aggregate_raw_trades_as_ohlc,
    compute_tech_indicators,
    tuple_to_dict,
    save_output_to_feature_store,
)
from src.logger import get_logger

def get_dataflow(
    window_seconds: int,
) -> Dataflow:
    """Constructs and returns a ByteWax Dataflow

    Args:
        window_seconds (int)

    Returns:
        Dataflow:
    """
    flow = Dataflow()
    connect_to_input_socket(flow)
    parse_string_to_dict(flow)
    set_product_id_as_key(flow)
    add_tumbling_window(flow, window_seconds)
    aggregate_raw_trades_as_ohlc(flow)
    compute_tech_indicators(flow)
    tuple_to_dict(flow)
    return flow

if __name__ == "__main__":
    
    logger = get_logger()
    
    logger.info('Parsing command line arguments...')
    parser = ArgumentParser()
    parser.add_argument('--dev', action='store_true')
    parser.set_defaults(dev=False)
    args = parser.parse_args()

    # Test inputs/outputs for debugging
    # WINDOW_SECONDS = 5
    logger.info('Generating dataflow')
    test_flow = get_dataflow(window_seconds=config.WINDOW_SECONDS)
    
    if args.dev:
        test_flow.capture(StdOutputConfig())
    else:
        from src.config import FEATURE_GROUP_METADATA
        save_output_to_feature_store(test_flow, FEATURE_GROUP_METADATA)
    
    logger.info('Running dataflow')
    run_main(test_flow)
    