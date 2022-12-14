import pandas as pd
import logging

df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.debug(df)
