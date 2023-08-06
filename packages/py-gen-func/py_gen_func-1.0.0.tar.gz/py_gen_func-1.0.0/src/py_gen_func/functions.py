import logging
import pandas as pd
import re

from .Exceptions import GenException

logger = logging.getLogger("py_gen_func")


def pd_merge_wrap(df1: pd.DataFrame, df2:pd.DataFrame, raise_exception: bool = False, 
                  **kwargs) -> pd.DataFrame:
    """Wrapper function around the pd.merge function. Checks for different 
    dimensionality based on df1 
        
    Args:
        df1 (pd.DataFrame): Dataframe on the left handside of the join
        df2 (pd.DataFrame): Dataframe on the right handside of the join
        raise_exception (bool): Option whether an exception should be raised if the 
        dimensions are different
        
    Returns:
        pd.DataFrame: Joined version of df1 and df2 
    """
    pre_join_dim = df1.shape[0]
    res = pd.merge(left=df1, right=df2, **kwargs)
    post_join_dim = res.shape[0]
    
    if pre_join_dim != post_join_dim:
        logger.warning("Dimensions post join are different")
        
        if raise_exception:
            raise GenException("Dimensions post join are different")
            
    return res

def flatten_pd_dataframe_multi_col(df_cols:list) -> list:
    """Function to flatten the columns of a dataframe with multiindex columns

    Args:
        df_cols (list): list type object i.e. could be df.columns

    Returns:
        list: list of flatten column values
    """
    df_cols = [' '.join(col).strip() for col in df_cols.values]
    df_cols = [re.sub("_$", "", col) for col in df_cols]
    return df_cols