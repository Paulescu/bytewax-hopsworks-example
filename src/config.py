import os

from src.types import FeatureGroupMetadata

# load Feature Store credentials from environment variables
HOPSWORKS_PROJECT_NAME = os.environ['HOPSWORKS_PROJECT_NAME']
HOPSWORKS_API_KEY = os.environ['HOPSWORKS_API_KEY']

WINDOW_SECONDS = 10
PRODUCT_IDS = [
    "ETH-USD",
    # "BTC-USD",
]

FEATURE_GROUP_METADATA = FeatureGroupMetadata(
    name=f'ohlc_{WINDOW_SECONDS}_sec',
    version=1,
    description=f"OHLC data with technical indicators every {WINDOW_SECONDS} seconds",
    primary_key=['time'], # TODO: add product_id as key if we pull more than one product
    event_time='time',
    online_enabled=True,
)

FEATURE_VIEW_NAME = f'ohlc_{WINDOW_SECONDS}_sec_view'
FEATURE_VIEW_VERSION = 1
