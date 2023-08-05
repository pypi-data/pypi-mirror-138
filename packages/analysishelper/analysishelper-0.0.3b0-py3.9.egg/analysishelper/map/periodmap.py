#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Chia Wei Lim
# Created Date: 2021-12-08
# version ='1.0'
# ---------------------------------------------------------------------------
"""Module related to appending period time"""
# ---------------------------------------------------------------------------
import pandas as pd
import sys
import logging
import os

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s |  [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=os.environ.get("LOGLEVEL", "INFO").upper(),
    stream=sys.stdout,
)

class PeriodMap:

    def __init__(self):
        pathtofile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "metadata", "period_dict.csv")
        perioddf = pd.read_csv(pathtofile)
        
        #extract column name to remove before merging
        temp_columns = perioddf.filter(like = "_temp").columns

        self.perioddf = perioddf.drop(labels = temp_columns, axis = 1)

        logging.info(f"Reference period df generated")

    def appendperiod(self, df, left_on = "period_code", right_on = "period_code"):
        """
        left_on (str, optional): period column name of input data frame. Implicitly looks for period_code if not defined
        """

        logging.info(f"Merging period with left(input df): {left_on} and right: {right_on}")
        
        if left_on not in df.columns: 

            logging.warning(f"{left_on} not found in dataframe. Cant append period")
            
        # add checking for df[refcolumn] datatype to check if compatible
        
        return self.perioddf.merge(df, left_on = left_on, right_on = right_on)
        