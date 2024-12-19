"""Main Description."""

import logging
import os
from typing import Any, Dict

import pandas as pd
from pymongo import MongoClient

LOGGER = logging.getLogger(__name__)


def load_data(collection: str) -> pd.DataFrame:
    """Load the data from MongoDB."""
    pwd = os.environ["MONGODB_PWD"]
    user = os.environ["MONGODB_USER"]
    mongo_database = os.environ["MONGODB_DATABASE"]

    LOGGER.info("Reading data from: %s", mongo_database)

    connection_string = f"mongodb+srv://{user}:{pwd}@cluster0.g0glf.mongodb.net/"
    try:
        client: MongoClient[Dict[str, Any]] = MongoClient(connection_string)
    except Exception as exception:  # pylint: disable=broad-exception-caught
        LOGGER.error("Couldn't connect to MongoDB: %s", exception)
    database_conection = client[mongo_database]
    tmp_collection = database_conection[collection]
    data = tmp_collection.find()
    df = pd.DataFrame(data)

    return df
