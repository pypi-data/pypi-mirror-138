'''
check the timestamps of the log files under 
directly in ecfs
It will select only the directories containing
logfiles.tar, since this file always has to be
there when a YYYY/MM/DD/HH is completed
'''
import os
import time
from collections import OrderedDict
import pandas as pd
import re
import sys
import subprocess
from hartools.harmon.config import harmonconf as harmonconf
from datetime import datetime
import time
from functools import wraps
import hartools.harmon.progress_utils as pu

def timing(f):
    '''
    Decorator for timing functions
    Usage: include the timing decorator
    before the function defintion as  below

    @timing
    def function(a):
        pass

    @return timing of the function in seconds
    '''
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        #print('function:%r took: %2.2f sec' % (f.__name__,  end - start))
        print('func:%r args:[%r, %r] took: %2.4f sec'%(f.__name__, args, kwargs, end-start))
        return result
    return wrapper

def els_cmd(edir,com="els -l"):
    '''
    Check a particular file. IT must return only one element, otherwise it failed   
    '''
    cmd = com+" "+edir
    try:
        ret=subprocess.check_output(cmd,shell=True)

    except subprocess.CalledProcessError as err:
        print(f"Error in call to subprocess {err}")
        print(f"{cmd} failed")
        rubbish = ["None"] # dummy array with 2 elements
        return rubbish
    ret = ret.decode('utf-8')
    #split listing in lines
    elsdir = ret.split("\n")
    elsdir.remove("") #remove empty elements
    return elsdir

def get_month(elslist,stream,today):
    '''
    Sel month(s) based on the last modified date
    @return: list of months
    '''
    #The split cleans the extra spaces, date and month appear in 
    # places 6 and 7
    this_year = datetime.strftime(datetime.now(),"%Y")
    date_strings = [d.split()[5]+" "+d.split()[6] for d in elslist]
    sel_m = [l.split()[-1] for l in elslist if l.split()[-1].isdigit()]

    if len(sel_m) != 1:
        #print(f"WARNING: more than one directory available on month: {sel_m}")
        sel_month = [d.split()[-1] for d in elslist if today in d]
        if len(sel_month) != 0:
            print(f"Last month modified on {today}: {sel_month}")
        else: #print dates of year directories for control
            lastmod = [l.split()[-1]+" "+l.split()[5]+" "+l.split()[6] for l in elslist if l.split()[-1]]
            print(f"DEBUG: last months modified (month and date): {lastmod}")
       
    
    return sel_m

def get_year(elslist,stream,today):
    '''
    Sel years in directory
    '''
    #The split cleans the extra spaces, date and month appear in 
    # places 6 and 7
    this_year = datetime.strftime(datetime.now(),"%Y")
    date_strings = [d.split()[5]+" "+d.split()[6] for d in elslist]
    sel_y = [l.split()[-1] for l in elslist if l.split()[-1].isdigit()]

    if len(sel_y) != 1:
        #print(f"WARNING: more than one directory available on year: {sel_y}")
        sel_year = [d.split()[-1] for d in elslist if today in d]
        if len(sel_year) != 0:
            print(f"Last dir modified on {today}: {sel_year}")
        else: #print dates of year directories for control
            lastmod = [l.split()[-1]+" "+l.split()[5]+" "+l.split()[6] for l in elslist if l.split()[-1]]
            print(f"DEBUG: last years modified: {lastmod}")
    #sel_y = max(sel_y)
    return sel_y

def get_days(month_ls,today,edir):
    '''
    Search for the days which might contain data
    on today date
    '''
    days = [d.split()[-1] for d in month_ls]
    sel_days=[]
    for day in days:
        ddir = os.path.join(edir,day)
        ls_day = els_cmd(ddir)
        lookuphours = [l for l in ls_day if today in l]
        #debug message
        #if len(lookuphours) != 0: print(f"Found {lookuphours} in {day}")
        if len(lookuphours) != 0: sel_days.append(day)
    return sel_days

def get_dh(elslist,today):
    '''
    Sel days and hours
    '''
    #The split cleans the extra spaces. Date and month appear in 
    # places 6 and 7. The directory in last place
    sel_dir = [d.split()[-1] for d in elslist if today in d]
    #select the year/month, it should be only one!
    sel_dh = [l for l in sel_dir if l.isdigit()]
    return sel_dh
#@timing
#This function is only for testing. Note hardcoded project below
def alldates_stream(stream):
    '''
    Go down all year/month/days directories
    for an stream
    This is only to collect the total number of 
    timestamps for a stream. It can take up to 3 h running in
    an slurm script to do the els commands for a whole stream.
    @return a df with all timestamps info
    '''
    project="DANRA"
    user = harmonconf.yaml["PROJECTS"][project]["STREAMS"][stream]["USER"]
    if os.path.isfile(stream+".csv.gz"):
        timestamps = pd.read_csv(stream+".csv.gz",compression="gzip")
        timestamps.drop(columns=["id"],inplace=True)
        return timestamps
       
        #read the data from this file
    #timestamps.to_csv(stream+".csv",sep=",")
    print(f"Doing {stream}")
    estream  = os.path.join("ec:/"+user+"/harmonie",stream)
    this_year = datetime.strftime(datetime.now(),"%Y") # current year
    logs_path=[]
    elsfiles=els_cmd(estream)
    years = [x.split()[-1] for x in elsfiles if x.split()[-1].isdigit()]
    for year in years:
        months = els_cmd(os.path.join(estream,year),"els")
        for month in months:
            days = els_cmd(os.path.join(estream,year,month),"els") 
            for day in days:
                hours = els_cmd(os.path.join(estream,year,month,day),"els") 
                for hour in hours:
                    logfile = os.path.join(estream,year,month,day,hour,"logfiles.tar")
                    test = els_cmd(logfile,"els") 
                    if len(test) != 1 or "None" in test:
                        print(f"{logfile} not found")
                    else:
                        logs_path.append(logfile)
    collect_all =OrderedDict()
    collect_all["stream"] = []
    collect_all["date"] = []
    collect_all["path"] = []
    collect_all["simdate"] = []
    collect_all["timestamp"] = []
    #print("All files found")
    for log in logs_path:
        collect_all["stream"].append(stream)
        logls = els_cmd(log,"els -l")
        if not ":"  in logls[0].split()[7]:
            datestring = " ".join([logls[0].split()[5],logls[0].split()[6],logls[0].split()[7]])
            tstamp = datetime.strptime(datestring,"%b %d %Y")
        else:
            datestring = " ".join([this_year,logls[0].split()[5],logls[0].split()[6],logls[0].split()[7]])
            tstamp = datetime.strptime(datestring,"%Y %b %d %H:%M")
        drf = datetime.strftime(tstamp,"%Y/%m/%d")
        rftstamp = datetime.strftime(tstamp,"%Y-%m-%d %H:%M:%S")
        collect_all["timestamp"].append(rftstamp)
        collect_all["date"].append(drf)
        log_split = log.replace("ec:","").split("/")
        year,month,day = log_split[4],log_split[5],log_split[6]
        collect_all["simdate"].append(os.path.join(year,month,day))
        collect_all["path"].append(log)
        #print(l)
    dates_df = pd.DataFrame(collect_all)
    dates_df.drop_duplicates(subset="simdate",keep="last",inplace=True)
    timestamps = pd.DataFrame({"stream":collect_all["stream"],
                               "logfile":collect_all["path"],
                               "timestamp":collect_all["timestamp"],
                               "yyyymmdd":collect_all["date"],
                               "simdate":collect_all["simdate"]})
    #This one is just for safekeeping in case data is somehow lost
    #in the merge with the old data as happened once
    #Moved to collect_all for the moment
    #timestamps.to_csv(stream+".csv",sep=",")
    return timestamps

def getdate_els(elslist,project,stream,today):
    '''
    Collect all dates for a given stream.
    It is supposed to be used only with currently running streams
    '''

    # Clean the els listing and extract dates for each file
    this_year = datetime.strftime(datetime.now(),"%Y")
    #go through year and month
    years = get_year(elslist,stream,today)

    #Only check currrent year and last year in list above (in case this happened on same day)
    csd = pu.get_DTG(project,stream)
    csd_year = csd[0:4]
    years = [years[-2], csd_year]
    #TODO: need to add hear an extra loop for month, since there
    #can be a change of month here on the same day!
    # Include a loop??
    collect_all =OrderedDict()
    collect_all["stream"] = []
    collect_all["date"] = []
    collect_all["path"] = []
    collect_all["simdate"] = []
    collect_all["timestamp"] = []
    user = harmonconf.yaml["PROJECTS"][project]["STREAMS"][stream]["USER"]
    for year in years:
        edir  = os.path.join("ec:/"+user+"/harmonie",stream,year)
        print(f"Checking {edir}")
        ls_year = els_cmd(edir)
        sel_month = get_month(ls_year,stream,today)
        for month in sel_month:
            edir  = os.path.join("ec:/"+user+"/harmonie",stream,year,month)
            print(f"Checking {edir}")
            ls_month = els_cmd(edir)
            #print(ls_month)
            #go through days and hours
            #if month == "05" and year == "1995":
            sel_day = get_days(ls_month,today,edir)
            #else:
            #    sel_day = get_dh(ls_month,today)
            for day in sel_day:
                edir  = os.path.join("ec:/"+user+"/harmonie",stream,year,month,day)
                #print(edir)
                ls_day = els_cmd(edir)
                sel_hour = get_dh(ls_day,today)
                print(f"Hours in day {day}: {sel_hour}")
                for hour in sel_hour:
                    edir  = os.path.join("ec:/"+user+"/harmonie",stream,year,month,day,hour)
                    #print(f"check day: {edir}")
                    ls_hour = els_cmd(edir)
                    log = [l for l in ls_hour if "logfiles.tar" in l]
                    if len(log) != 0:
                        log = log[0]
                        # The datestring can also be of the form
                        # Mar 24  2020 for past years. It will only contain
                        # form mmm dd HH:MM for current year
                        if not ":"  in log.split()[7]:
                            datestring = " ".join([log.split()[5],log.split()[6],log.split()[7]])
                            tstamp = datetime.strptime(datestring,"%b %d %Y")
                        else:
                            datestring = " ".join([this_year,log.split()[5],log.split()[6],log.split()[7]])
                            tstamp = datetime.strptime(datestring,"%Y %b %d %H:%M")
                        drf = datetime.strftime(tstamp,"%Y/%m/%d")
                        rftstamp = datetime.strftime(tstamp,"%Y-%m-%d %H:%M:%S")
                        collect_all["date"].append(drf)
                        collect_all["timestamp"].append(rftstamp)
                        collect_all["stream"].append(stream)
                        collect_all["simdate"].append(os.path.join(year,month,day))
                        addpath = os.path.join(edir,"logfiles.tar")
                        collect_all["path"].append(addpath)
                        print(f"Found {addpath} with timestamp: {datestring}")
    #Now select only the last item in a given day
    dates_df = pd.DataFrame(collect_all)
    dates_df.drop_duplicates(subset="simdate",keep="last",inplace=True)
    timestamps = pd.DataFrame({"stream":collect_all["stream"],
                               "logfile":collect_all["path"],
                               "timestamp":collect_all["timestamp"],
                               "yyyymmdd":collect_all["date"],
                               "simdate":collect_all["simdate"]})
    return dates_df["date"], timestamps
     

def count_days(project,streams,today):
    '''
    Count latest files with els in the harmonie directories
    @today: string format, ie Jan 12
    '''
    counter=OrderedDict()
    counter["ndays"] = []
    counter["stream"] = []
    ts_streams = []
    for stream in streams: 
        print(f"Cheking {stream} on {today}")
        user = harmonconf.yaml["PROJECTS"][project]["STREAMS"][stream]["USER"]
        edir  = "ec:/"+user+"/harmonie/"+stream
        elsfiles=els_cmd(edir)
        dates,tstamps = getdate_els(elsfiles,project,stream,today)
        ndays = dates.shape[0]
        print(f"Simdays completed for {stream} on {today}: {ndays}")
        counter["ndays"].append(ndays)
        counter["stream"].append(stream)
        ts_streams.append(tstamps)
    merge=pd.concat(ts_streams,sort=False)
    merge.sort_values('timestamp',inplace=True)
    merge.reset_index(drop=True,inplace=True)
    return counter,merge
if __name__=="__main__":
    #TESTS:
    project="CARRA"
    streams = [key for key in harmonconf.yaml["PROJECTS"][project]["STREAMS"].keys()]
    #streams = ["carra_NE_4","carra_NE_5","carra_NE_6",
    #           "carra_IGB_4","carra_IGB_5","carra_IGB_6"]
    #provide input as date of form YYYYMMDD
    #Otherwise it will use today. It will convert to format
    # Month (3 letters) day, to match what els prints
    if len(sys.argv) == 2:
        today_in = sys.argv[1]
        #The date format needs to match what is printed by ls -l
        #Extra space for 1 digit: June  8 (cf Jun 10)
        date = datetime.strptime(today_in,"%Y%m%d")
        sdigit = datetime.strftime(date,"%-d")
        if len(sdigit) == 1: today = datetime.strftime(date,"%b  %-d")
        if len(sdigit) > 1:  today = datetime.strftime(date,"%b %-d")
    else:
        sdigit = datetime.strftime(datetime.now(),"%-d")
        if len(sdigit) == 1: today = datetime.strftime(datetime.now(),"%b  %-d")
        if len(sdigit) > 1:  today = datetime.strftime(datetime.now(),"%b %-d")
    counter,streams_ts = count_days(project,streams,today)
    print(f"Summary of days simulated on {today}")
    print(counter)
    
    print(f"Extraction based on counting numbers in dataframe")
    for stream in streams:
        count = streams_ts[streams_ts.stream == stream].drop_duplicates(subset="simdate",keep="last").shape[0]
        print(f"{count} days on {today} for {stream}")
