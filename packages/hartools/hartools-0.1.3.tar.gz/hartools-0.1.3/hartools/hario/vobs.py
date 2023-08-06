"""The vobs class"""
import logging
import datetime
import os, sys
import numpy as np
import pandas as pd
import re
from collections import OrderedDict
from typing import Tuple
logger = logging.getLogger(__name__)

class vobs:
    def __init__(self,period=None, datadir=None, source="asc") -> None:
        """Initialize the vobs class

        Args:
            period ([str], optional): The period to include. String separated by -. Defaults to None.
            datadir ([str], optional): The path with the data. Defaults to None.
            source (str, optional): The source type. Defaults to "asc". No 
        """
        self.flen = 24
        self.period = period.split('-')
        self.datadir = datadir
        self.ifiles,self.dates = self._locate_files(self.datadir,self.period,self.flen)
        self.ftimes = self._dates_expand(self.period,self.flen)
        data_synop, data_temp, accum_synop = self._get_data(self.ifiles)
        self.data_synop = data_synop
        self.data_temp = data_temp
        #self.temp_stations = self._get_temp_station_list(self.data_temp)
        self.accum_synop = accum_synop

    def _locate_files(self,datadir,period,flen):
        """Locate the files available in path datadir

        Args:
            datadir ([str]): The path with the vobs files
            period ([str]): The period in format of two strings with YYYYMMDD, separated by a 
                            single dash
            flen ([int]]): The number of hours. Defaults to 24

        Returns:
            [list]: Two lists with the files and the dates
        """
        
        date_ini=datetime.datetime.strptime(period[0],'%Y%m%d')
        date_end=datetime.datetime.strptime(period[1],'%Y%m%d')
        dates = [date_ini + datetime.timedelta(days=x) for x in range(0, (date_end-date_ini).days + 1)]
        str_dates=[datetime.datetime.strftime(date,'%Y%m%d') for date in dates]
        ifiles = []
        dtgs=[]

        for date in str_dates:
            for hour in range(0,flen):
                date_file = datetime.datetime.strptime(date,'%Y%m%d') + datetime.timedelta(seconds=3600*hour)
                date_file = datetime.datetime.strftime(date_file,'%Y%m%d%H')
                dtgs.append(date_file)
                fname=''.join(['vobs',date_file])
                ifile=os.path.join(datadir,fname)
                if os.path.exists(ifile):
                    ifiles.append(ifile)
                else:
                    ifiles.append('None')
        if (len(ifiles) == 0) or (len(set(ifiles)) == 1): # if all elements equal all None!
            logger.info("WARNING: no data found for dates %s"%(str_dates))
            logger.info(ifiles)
        logger.debug("first file: %s"%(ifiles[0]))
        logger.debug("last file: %s"%(ifiles[-1]))
        return ifiles, dtgs

    def _get_data(self,ifiles):
        '''
        Extract the data from all ifiles in a df for SYNOP and TEMP data
        '''
        data_synop=OrderedDict()
        data_temp=OrderedDict()
        accum_synop =OrderedDict()
        for i,ifile in enumerate(ifiles):
            #date=self.dates[i] #ORIGINAL: now storing in ftimes to match with vfld dates
            date=self.ftimes[i]
            data_synop[date], data_temp[date], accum_synop[date] = self._split_data(ifile)
            # print a warning if synop data is not there:
            # TODO: if no synop, don't include model!
            if len(data_synop[date]) == 0:
                logger.info("WARNING: no synop data for %s!"%(date))
                data_synop[date] = 'None'
            if len(data_temp[date]) == 0:
                logger.info("WARNING: no temp data for %s!"%(date))
                data_temp[date] = 'None'
        return data_synop, data_temp, accum_synop

    def read_synop(infile,varlist) -> pd.DataFrame:
        rawData=pd.read_csv(infile,delimiter=" ")
        if 'FI' in varlist:
            columns = ['stationId','lat','lon'] + varlist
            rawData.columns=columns
            rawData=rawData.rename(columns={'FI': 'HH'})
        else:    
            columns=['stationId','lat','lon','HH']+varlist
            rawData.columns=columns
        if 'PE' in varlist:
            rawData=rawData.rename(columns={'PE':'PE1'})
        return rawData

    def _split_data(self,ifile) -> Tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame]:
        '''
        Split the data from ifile into SYNOP and TEMP
        in two data frames
        '''
        cols_temp = ['PP','FI','TT','RH','DD','FF','QQ','TD'] #this set of temp variables is constant
        header_temp=OrderedDict()
        print(f"Reading {ifile}")
        if ifile != 'None':
            colnames, nsynop_stations, ignore_rows, ntemp_stations, accum_synop = self._get_synop_vars(ifile)
            if nsynop_stations != 0:
                data_synop = pd.read_csv(ifile,sep=r"\s+",engine='python',header=None,index_col=None,
                    dtype=str,skiprows=ignore_rows,nrows=nsynop_stations)
                data_synop.columns=colnames
                nrows_synop = data_synop.shape[0]
            elif nsynop_stations == 0:
                print(f"No synop data: {nsynop_stations}")
                data_synop = "None" #pd.DataFrame(columns = colnames)
                accum_synop = "None"
                nrows_synop = 0
           
            if ntemp_stations != 0:
                #when writing the data in vfld format for monitor in vfld_monitor
                ignore_temp=ignore_rows+nrows_synop+10 #ignore first rows on this  part
                data_temp =  pd.read_csv(ifile,sep=r"\s+",engine='python',header=None,index_col=None,names=cols_temp,
                                      dtype=str,skiprows=ignore_temp)
            elif ntemp_stations == 0:
                print(f"No temp data: {ntemp_stations}")
                data_temp = "None" #pd.DataFrame(columns = cols_temp)
        else:
            data_synop = 'None'
            data_temp = 'None'
            accum_synop = 'None'
    
        return data_synop, data_temp, accum_synop
    
    def _get_synop_vars(self,ifile):
        '''
        Extract information about the SYNOP variables in vfld file
        '''
        #Read this file to determine number of variables in file:
        first_two=[]
        with open(ifile) as f:
            first_two.extend(str(f.readline()).rstrip() for i in range(2))
        nsynop_vars=int(first_two[-1]) # number of variables in synop data
        ntemp_stations=int(first_two[-1]) # number of temp stations in file
        nsynop_stations,ntemp_stations,ver_file =  first_two[0].split() # number of synop stations in file
        nsynop_stations=int(nsynop_stations)
        ntemp_stations = int(ntemp_stations)
    
        lines_header =[]
        with open(ifile) as f:
                lines_header.extend(f.readline().rstrip() for i in range(nsynop_vars+2))
        #this regex is to remove all extrs spaces and replace it with one
        #print(f"check lines before {lines_header}")        
        #Deprecated style, apparently:
        #lines_clean =  [re.sub('\s+',' ',i).strip() for i in lines_header]   
        lines_clean =  [re.sub(' +',' ',i).strip() for i in lines_header]   
        #print(f"check lines after {lines_clean}")     
        vars_synop=[i.split(' ')[0] for i in lines_clean[2:]]
        accum_synop=[i.split(' ')[1] for i in lines_clean[2:]] #accumulation times. Needed to write the data at the end
        if 'FI' in vars_synop:
            colnames= ['stationId','lat','lon'] + vars_synop
            start_col_replace = 3
        else:
            colnames=['stationId','lat','lon','HH'] + vars_synop
            start_col_replace = 4
        ignore_rows = 2 + nsynop_vars # number of rows to ignore before reading the actual synop data
        return colnames, nsynop_stations, ignore_rows, ntemp_stations, accum_synop

    def _dates_expand(self,period,flen) -> list:
        '''
        Expand the dates into YYYYMMDD format
        '''
        date_ini=datetime.datetime.strptime(period[0],'%Y%m%d')
        date_end=datetime.datetime.strptime(period[1],'%Y%m%d')
        dates = [date_ini + datetime.timedelta(days=x) for x in range(0, (date_end-date_ini).days + 1)]
        dtgs=[]
        str_dates=[datetime.datetime.strftime(date,'%Y%m%d') for date in dates]
        for date in str_dates:
            #print(date)
            for hour in range(0,flen):
                dtgs.append(''.join([date[0:8],str(hour).zfill(2)]))
        return dtgs            

    
    def read_temp(time,date):
        '''Read the temp stations. Not yet implemented'''
        pass
        
if __name__ == '__main__':
    period='20220115-20220115'
    datadir='/tmp/vobs/'
    vobs_data = vobs(period=period, datadir=datadir)
    print(vobs_data.data_synop)
