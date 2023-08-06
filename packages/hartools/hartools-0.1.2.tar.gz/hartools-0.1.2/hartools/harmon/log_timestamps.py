#check the timestamps of the log files under 
# wrkDir=/scratch/ms/dk/nhx/hm_home/
# create files with the latest timestamp for the day.
# Update the final files
import os
import time
from collections import OrderedDict
import pandas as pd
from datetime import datetime
from datetime import timedelta
import re
import sys
import subprocess
import sqlite3

from hartools.harmon.config import harmonconf as harmonconf
from hartools.harmon.count_days_ecfs import count_days as cdays

#Class to store all time stamps for a given stream
class log_timestamps(object):
    def __init__(self, project=None, streams=None, date=None, dbase=None):
        self.project = project
        self.streams = streams # a dict with keys STREAM and USER and a list in each
        self.date = date # date, in format YYYYMMDD
        self.dbase = dbase
        #The date needs to match the format in els!
        #Note the extra space with one digit Jun  8
        # instead of Jun 10
        # This removes the extra zero: datetime.strftime(date_conv,"%b %-d")
        # This adds the extra space: datetime.strftime(date_conv,"%b  %-d")
        if self.date is None:
            today=datetime.today()
            sdigit = datetime.strftime(today,"%-d")
            if len(sdigit) == 1: self.date = datetime.strftime(today,"%b  %-d")
            if len(sdigit) > 1: self.date = datetime.strftime(today,"%b %-d")
        else:
            date_conv = datetime.strptime(self.date,"%Y%m%d")
            sdigit = datetime.strftime(date_conv,"%-d")
            if len(sdigit) == 1: self.date = datetime.strftime(date_conv,"%b  %-d")
            if len(sdigit) > 1: self.date = datetime.strftime(date_conv,"%b %-d")
        self.ts_old = self._read_sql(self.dbase)
        self.counter, self.ts_new = self._new_timestamps(self.project,self.streams,self.date)
        self.ts = self._clean_timestamps(self.ts_old,self.ts_new)

    def _new_timestamps(self,project,streams,date):
        counter,timestamps = cdays(project,streams,date)
        return counter, timestamps

    def save_data(self,dbase):
        conn=sqlite3.connect(dbase)
        self.ts.to_sql("daily_logs",conn, if_exists="replace", index=False)

    def _clean_timestamps(self,df_old,df_new):
        '''
        Merge the old and new data sets, getting
        rid of any duplicates
        @return cleaned data frame
        '''
        dfs=[df_old, df_new]
        merge=pd.concat(dfs,sort=False)
        merge.sort_values('timestamp',inplace=True)
        merge.drop_duplicates(subset=['stream','timestamp'], keep='first',inplace=True)
        merge.sort_values('stream',inplace=True)
        merge.reset_index(drop=True,inplace=True)
        return merge

    def _read_sql(self,sql_file):
        '''
        create table if it does not exist.
        @return dataframe with time stamps
        '''
        if not os.path.isfile(sql_file):
            self.create_table(sql_file)
        conn=sqlite3.connect(sql_file)
        sql_command = "SELECT * FROM daily_logs"
        ts = pd.read_sql(sql_command, conn)
        return ts

    def create_table(self,sql_file,table="daily_logs"):
        """ 
        create the sql table
        """
        create_table_sql   = """CREATE TABLE IF NOT EXISTS """+table+"""
                              ( stream TEXT PRIMARY KEY, 
                                logfile TEXT NOT NULL, 
                                timestamp TEXT NOT NULL, 
    			        yyyymmdd TEXT NOT NULL,
                                simdate TEXT NOT NULL )"""
    
        conn=sqlite3.connect(sql_file)
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def speed_stream(self,stream,winlen):
        '''
        print stream speed for a particular window length
        '''
        #group by stream and real date
        gp=self.ts.groupby(['yyyymmdd','stream'])
        #select the groups for the current date        
        #today=datetime.strftime(datetime.now(),'%Y/%m/%d')
        days=[datetime.today() - timedelta(days=x) for x in range(0,winlen)]
        #Loop through the logfiles for this date and the past days
        #in the winlen window. Extract only the DTG part from logfile name
        count_sim_days=0
        for day in days:
            #select the indices that I need to access for this day
            key=(datetime.strftime(day,'%Y%m%d'), stream)
            if key in gp.groups:
                idxs=gp.groups[key].tolist()
                sim_dates=[]
                for ix in idxs:
                    get_log=self.ts['logfile'][ix]
                    sel_file=os.path.split(get_log)[1]
                    sel_date=os.path.splitext(sel_file)[0].split('_')[-1]
                    yyyymmdd=sel_date[0:8]
                    if yyyymmdd not in sim_dates:
                        sim_dates.append(yyyymmdd)
                count_sim_days=len(sim_dates)+count_sim_days
        if count_sim_days > 0:
            sim_speed = count_sim_days/winlen
        else:
            sim_speed = 0.0

        return sim_speed


if __name__ == "__main__":
    #TESTS: not to be used to collect data!
    project="CARRA"
    streams= [key for key in harmonconf.yaml["PROJECTS"][project]["STREAMS"].keys()]
    #print(f"Collecting data for {streams}")        
    #dbase = harmonconf.yaml["ARXIV"]["DBASE"]
    #timestamps=log_timestamps(project=project,streams=streams,dbase=dbase)
    #timestamps.save_data(dbase=dbase)
    #print(f"Saving data to {outdir}")
    #ts_streams.save_data(outdir=outdir)
