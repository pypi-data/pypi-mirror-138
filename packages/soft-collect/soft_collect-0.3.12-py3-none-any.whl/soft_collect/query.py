import logging

import pandas as pd

from .config import settings
from .db import get_DB_client
from .save import get_save_client
from .utils import elapsed_time

logger = logging.getLogger(__name__)


class Query:
    def __init__(self, save):
        self.db = get_DB_client(settings.dbm)
        self.sh = get_save_client(save)

    def run(self, sql, filename):
        logger.info(f"Reading SQL file in {sql}")

        with open(sql, "r", encoding="utf8", errors="ignore") as f:
            query = f.read()

        logger.info("Running query")
        with elapsed_time as et:
            task = et.add_task("Running your query, elapsed time:")
            cnxn = self.db.set_up_connection()
            df_chunks = pd.read_sql(query, cnxn, coerce_float=False, chunksize=20000)
            et.stop_task(task)

        logger.info("Finished running query")

        print("Saving result in chunks of 20k rows")
        prefix = ""
        for i, df in enumerate(df_chunks):
            print(f"Saving chunk {i+1}...")
            if i > 0:
                prefix = f"{i}-"
            print(f"Saving result to {prefix+filename}.csv")
            logger.info(f"Saving result to {prefix+filename}.csv")
            self.sh.save_meta(df, prefix + filename)
