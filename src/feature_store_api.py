import hsfs
import hopsworks

import src.config as config
from src.types import FeatureGroupMetadata
from src.logger import get_console_logger

logger = get_console_logger()

def get_feature_store() -> hsfs.feature_store.FeatureStore:
    """Connects to Hopsworks and returns a pointer to the feature store

    Returns:
        hsfs.feature_store.FeatureStore: pointer to the feature store
    """
    project = hopsworks.login(
        project=config.HOPSWORKS_PROJECT_NAME,
        api_key_value=config.HOPSWORKS_API_KEY
    )
    return project.get_feature_store()


def get_feature_group(
    feature_group_metadata: FeatureGroupMetadata
) -> hsfs.feature_group.FeatureGroup:
    """Connects to the feature store and returns a pointer to the given
    feature group `name`

    Args:
        name (str): name of the feature group
        version (Optional[int], optional): _description_. Defaults to 1.

    Returns:
        hsfs.feature_group.FeatureGroup: pointer to the feature group
    """
    return get_feature_store().get_or_create_feature_group(
        name=feature_group_metadata.name,
        version=feature_group_metadata.version,
        description=feature_group_metadata.description,
        primary_key=feature_group_metadata.primary_key,
        event_time=feature_group_metadata.event_time,
        online_enabled=feature_group_metadata.online_enabled
    )


def get_or_create_feature_view() -> hsfs.feature_view.FeatureView:
    """"""

    # get pointer to the feature store
    feature_store = get_feature_store()

    # get pointer to the feature group
    from src.config import FEATURE_GROUP_METADATA
    feature_group = feature_store.get_feature_group(
        name=FEATURE_GROUP_METADATA.name,
        version=FEATURE_GROUP_METADATA.version
    )

    # create feature view if it doesn't exist
    try:
        feature_store.create_feature_view(
            name=config.FEATURE_VIEW_NAME,
            version=config.FEATURE_VIEW_VERSION,
            query=feature_group.select_all()
        )
    except:
        logger.info("Feature view already exists, skipping creation.")
    
    # get feature view
    feature_store = get_feature_store()
    feature_view = feature_store.get_feature_view(
        name=config.FEATURE_VIEW_NAME,
        version=config.FEATURE_VIEW_VERSION
    )

    return feature_view