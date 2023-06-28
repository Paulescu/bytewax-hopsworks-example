import pandas as pd
import streamlit as st

from bytewax.outputs import ManualOutputConfig
from bytewax.execution import run_main

from src.plot import get_candlestick_plot
from src.date_utils import epoch2datetime

from src.config import WINDOW_SECONDS
from src.logger import get_console_logger

logger = get_console_logger()

st.set_page_config(layout="wide")
st.title(f"ETH/USD OHLC data every {WINDOW_SECONDS} seconds")

# here we store the data our Stream processing outputs
df = pd.DataFrame()

placeholder = st.empty()

import pandas as pd
def load_ohlc_data_from_feature_store() -> pd.DataFrame:
    """"""
    from src.feature_store_api import get_or_create_feature_view
    feature_view = get_or_create_feature_view()

    # get current epoch in seconds
    from time import time
    current_epoch_sec = int(time())

    # read time-series data from the feature store
    fetch_data_to = current_epoch_sec
    fetch_data_from = current_epoch_sec - 24*60*60

    logger.info(f'Fetching data from {fetch_data_from} to {fetch_data_to}')
    
    from datetime import datetime
    fetch_data_to = int(pd.to_datetime(datetime.utcnow()).timestamp())
    fetch_data_from = fetch_data_to - 1*60*60 # 1 hour
    
    ohlc_data = feature_view.get_feature_vectors(
        entry = [{"time": t} for t in range(fetch_data_from, fetch_data_to)]
    )

    # list of lists to Pandas DataFrame
    ohlc_data = pd.DataFrame(ohlc_data)
    ohlc_data.columns = ['upper_band', 'mid_band', 'lower_band', 'time', 'open', 'high', 'low', 'close', 'volume', 'product_id']
    ohlc_data.sort_values(by=['time'], inplace=True)

    return ohlc_data

while True:

    df = load_ohlc_data_from_feature_store()

    with placeholder.container():
        p = get_candlestick_plot(df, WINDOW_SECONDS)
        st.bokeh_chart(p, use_container_width=True)