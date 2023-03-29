from time import sleep

# import hopsworks

from src.feature_store_api import get_feature_group
from src.config import FEATURE_GROUP_METADATA
import src.config as config

# project = hopsworks.login(
#     project=config.HOPSWORKS_PROJECT_NAME,
#     api_key_value=config.HOPSWORKS_API_KEY
# )
# print(f'{config.HOPSWORKS_PROJECT_NAME=}')
# print(f'{config.HOPSWORKS_API_KEY=}')
# feature_store = project.get_feature_store()

print(f'{FEATURE_GROUP_METADATA=}')

feature_group = get_feature_group(FEATURE_GROUP_METADATA)

data = [
    {'time': 1, 'open': 45},
    {'time': 2, 'open': 47},
    {'time': 3, 'open': 47},
    {'time': 4, 'open': 47},
    {'time': 5, 'open': 47},
    {'time': 6, 'open': 47},
    {'time': 7, 'open': 47},
]
import pandas as pd

job = None
for d in data:
    job, _ = feature_group.insert(pd.DataFrame.from_records([d]),
                                  write_options={"start_offline_backfill": False})

import hsfs
job_api = hsfs.core.job_api.JobApi()
print(f'Launching job {job.name}')
job_api.launch(name=job.name)