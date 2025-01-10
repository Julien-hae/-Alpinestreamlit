"""Main Description."""

import logging
import os
from typing import Any, Dict

import pandas as pd
from pymongo import MongoClient

from Alpinestreamlit.common.dtypes import dtypes

LOGGER = logging.getLogger(__name__)


def create_client() -> MongoClient[Dict[str, Any]]:
    """Create a client connected to the databse."""
    pwd = os.environ["MONGODB_PWD"]
    user = os.environ["MONGODB_USER"]
    mongo_database = os.environ["MONGODB_DATABASE"]
    LOGGER.info("Create Client for the database: %s", mongo_database)

    connection_string = f"mongodb+srv://{user}:{pwd}@cluster0.g0glf.mongodb.net/test?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true"
    try:
        client: MongoClient[Dict[str, Any]] = MongoClient(connection_string)
    except Exception as exception:  # pylint: disable=broad-exception-caught
        LOGGER.error("Couldn't connect to MongoDB: %s", exception)

    return client


def load_collection(
    collection: str, client: MongoClient[Dict[str, Any]]
) -> pd.DataFrame:
    """Load a collection from MongoDB."""
    LOGGER.info("Reading data from the collection: %s", collection)
    mongo_database = os.environ["MONGODB_DATABASE"]
    database_conection = client[mongo_database]
    tmp_collection = database_conection[collection]
    data = tmp_collection.find()
    df = pd.DataFrame(data).astype(dtype=dtypes)

    return df


def load_data() -> pd.DataFrame:
    """Load all the data from the database."""
    database_name = os.environ["MONGODB_DATABASE"]
    LOGGER.info("Reading data from the database: %s", database_name)
    client = create_client()
    df = pd.DataFrame()
    for coll_name in client[database_name].list_collection_names():
        if df.empty:
            df = load_collection(coll_name, client)
        else:
            df = pd.concat([df, load_collection(coll_name, client)])

    return df
