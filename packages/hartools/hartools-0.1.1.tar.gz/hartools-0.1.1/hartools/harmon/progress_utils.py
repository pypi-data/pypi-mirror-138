#!/usr/bin/env python3

'''
Some functions to extract data from the timestamps
for the throughput plots
'''

from datetime import datetime
from datetime import timedelta
import pandas as pd
#need this to use it in crontab
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import matplotlib.dates as md
import sys
import re
import time
#Avoid pandas Future warning
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from collections import OrderedDict

import sqlite3
from hartools.harmon.config import harmonconf as harmonconf
from dateutil import relativedelta
BUFFER_DAYS = 30 #number of days to calculate ideal and real speed

def logs_extract(data,project,stream,remove_years):
    '''
    Calculate min and max DTG in data
    cols in data: ['stream', 'logfile', 'timestamp', 'yyyymmdd', 'simdate']
    The DTGS are extracted  from the paths of the logfiles.tar
    '''
    if remove_years == "None":
        #use here ONLY if want to plot the whole thing from the beginning
        logs=data[data['stream']==stream].logfile.tolist() # check log files for this stream
        log_dates=[]
        for log in logs:
            yyyymmddhh ="".join([i for i in log.split("/") if i.isdigit()])
            log_dates.append(yyyymmddhh)
        DTG_max=str(max(log_dates))
        DTG_min,stuff=stream_periods(project,stream) 
    else:
        # extract logs for a given date
        # Get rid of the selected years TOChECK: can I provide several numbers?
        data["remove"]=data["Year/Month/Day"].str.contains(remove_years) 
        data=data[data['remove'] == False] #drop the selected years
        #check for the logs at the beginning of the year:
        current_year = datetime.strftime(datetime.now(),"%Y")
        beg_year = pd.to_datetime(datetime.strptime(current_year+"0101","%Y%m%d"))
        #NOTE: Pandas warning. I will turn off this shit for now
        import warnings
        from pandas.core.common import SettingWithCopyWarning
        warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

        data["times"]=list(pd.to_datetime(data["timestamp"]).values) #so i dont get fucking warning?
        logs=data[data['stream']==stream].logfile.tolist() # check log files for this stream
        log_dates=[]
        for log in logs:
            yyyymmddhh ="".join([i for i in log.split("/") if i.isdigit()])
            log_dates.append(yyyymmddhh)
        #print(f"{stream} and dates found {log_dates} ")
        DTG_max=str(max(log_dates))
        DTG_min=str(min(log_dates))
    return DTG_min,DTG_max

def proglog_user(stream):
    '''
    identify the progress log according to user
    '''
    pfile=os.path.join(*[rdir,stream,'progress.log'])

def test_months_stream(project,stream):
    #sanity check: is this stream finished?
    #Calculate expected number of months
    conf = harmonconf.yaml["PROJECTS"][project]["STREAMS"]
    str_comp,str_end = stream_completed(project,stream)
    if str_comp: print(f"{stream} finished on {str_end}")
    DTG_min,DTG_max = str(conf[stream]["BEG_DATE"]),str(conf[stream]["END_DATE"])
    date1 = datetime.strptime(DTG_min, '%Y%m%d%H')
    date2 = datetime.strptime(DTG_max, '%Y%m%d%H')
    difference = relativedelta.relativedelta(date2, date1)
    months = difference.months
    years = difference.years
    # add in the number of months (12) for difference in years
    months += 12 * difference.years
    print(f"EXPECTED number of months for {stream}:{months}")

def calc_total_months(project):
    '''
    Calculate the total number of months for a project   
    '''
    conf = harmonconf.yaml["PROJECTS"][project]["STREAMS"]
    months2sim = 0
    streams=[key for key in conf.keys()] # Doing it for all
    #ESPECIAL CASE for PANARCTIC
    for st in streams:
        #print("Calling it here?")
        #str_comp,str_end = stream_completed(project,st)
        #if str_comp: print(f"{st} finished on {str_end}")
        DTG_min,DTG_max = str(conf[st]["BEG_DATE"]),str(conf[st]["END_DATE"])
        date1 = datetime.strptime(DTG_min, '%Y%m%d%H')
        date2 = datetime.strptime(DTG_max, '%Y%m%d%H')
        difference = relativedelta.relativedelta(date2, date1)
        months = difference.months
        years = difference.years
        # add in the number of months (12) for difference in years
        months += 12 * difference.years
        months2sim += months
    #print(f"TOTAL EXPECTED number of months for {project} ({streams}):{months2sim}")
    return months2sim

    

def progress_bar(project):
    '''
    TODO
    read the sql file with the stream information
    and calculate current completion percentage.
    It uses this file since I am storing the information
    there.
    '''
    dbase=harmonconf.yaml["PROJECTS"][project]["DBASE"]
    months2sim = calc_total_months(project)
    conn=sqlite3.connect(dbase)
    sql_command = "SELECT * FROM daily_logs"
    data=pd.read_sql(sql_command, conn)
    #current streams running
    conf = harmonconf.yaml["PROJECTS"][project]["STREAMS"]
    #streams=[key for key in conf.keys() if conf[key]["ACTIVE"]]
    streams=[key for key in conf.keys()] # Doing it for all
    progress_stream={}
    months_total=0
    for st in streams:
        DTG_min,DTG_max = logs_extract(data,project,st,"None")
        #print(f"PROG: Min and max for {st}: {DTG_min},{DTG_max}")
        date1 = datetime.strptime(DTG_min, '%Y%m%d%H')
        date2 = datetime.strptime(DTG_max, '%Y%m%d%H')
        difference = relativedelta.relativedelta(date2, date1)
        months = difference.months
        years = difference.years
        # add in the number of months (12) for difference in years
        months += 12 * difference.years
        print(f"Total months simulated for {st}:{months}")
        #test_months_stream(project,st) #TO check number of months in stream
        months_total += months
    total = round(100*months_total/months2sim,2)
    months_total=0
    # This loop is only for printing out some extra info !!!
    for st in streams:
        DTG_min,DTG_max = logs_extract(data,project,st,"None")
        date1 = datetime.strptime(DTG_min, '%Y%m%d%H')
        date2 = datetime.strptime(DTG_max, '%Y%m%d%H')
        difference = relativedelta.relativedelta(date2, date1)
        months = difference.months
        years = difference.years
        # add in the number of months (12) for difference in years
        months += 12 * difference.years
        months_total += months
    print(f"Number of months completed: {months_total}")
    return total

def html_table_carra(rfile,project,stream,TOAstream,speed_30d,speed_7d):
    '''
    rfile[output]: the name of the html file to write 
    #FFFF00 yellow
    #33FF38 green
    #FFA500 orange
    #FF0000 red
    #FFFFFF white
    '''
    #Check final data for project
    end_proj = harmonconf.yaml["PROJECTS"][project]["END_DATE"]
    #Set this by default to white and no remark
    extra_remark = ""
    bgcolor = "#FFFFFF"
    if speed_7d == 0.0:
        #print(f"{stream} not active for past week")
        extra_remark = "Inactive the past week"
        bgcolor = "#FFFF00"
    if speed_7d  == 0.0 and speed_30d  < 1.0: # and stream != "carra_pan":
        #print(f"{stream} not active for past week")
        extra_remark = "Currently suspended"
        bgcolor = "#FFFF00"
    #if speed_30d < 3.0 and stream != "carra_pan":
    #    extra_remark = "Delayed due to production issues"
    #    bgcolor = "#FFFF00"
    if speed_30d == 0.0 and speed_7d == 0.0:
        str_comp,str_end = stream_completed(project,stream)
        if str_comp: 
            extra_remark = "Stream finished"
            bgcolor = "#33FF38"
        else:
            extra_remark = "Currently suspended"
            bgcolor = "#FFFF00"
    #ALWAYS CHECK if the stream is finished!!!
    str_comp,str_end = stream_completed(project,stream)
    if str_comp: 
        extra_remark = "Stream finished"
        bgcolor = "#33FF38"

    #The orange color should always superseed all others
    if (TOAstream.isnumeric() 
        and int(TOAstream[0:8]) > end_proj 
        and not any(x in extra_remark for x in ["suspended","finished"])):
        #and "suspended" not in extra_remark:
        print(f"WARNING: {stream} is ending after project end {end_proj}")
        extra_remark = f"Completion date after project end ({end_proj})"
        bgcolor = "#FFA500"
    #elif TOAstream == "Inactive":
    #    extra_remark = "Currently suspended"
    #    bgcolor = "#FFFF00"
    #    print(f"WARNING: {stream} is inactive")
    #else:
    #    extra_remark = ""
    #    bgcolor = "#FFFFFF"
    extra_flag=""
    progCARRA=progress_bar("CARRA")
    progPA=progress_bar("PANARCTIC")
    exists = os.path.isfile(rfile)
    header='<!doctyle html><html><head><title>Estimated completion dates for all streams</title></head><body>'
    maintitle='<h1>Estimated completion dates and simulation speeds</h1>'
    description='<p>Stream (production) completion date based on 30d (7d) moving avg speed</p>'
    #extranote='<p> (*) Stream active for less than 5 days in the current month (completion date based on 7d avg). (**) Stream completed. (***) Stream suspended. Completion date undetermined. </p>'
    explanation='<p><a href="https://docs.google.com/document/d/1zDKAxuEXYnWWYzT3SZnZwY5WW8nodUMeYRjAGz46coc/edit#">Details of the calculation of the completion dates</a></p>'
    lastchanged='<p>Last update: '+datetime.now().strftime('%Y/%m/%d %H:%M:%S')+' UTC</p>'
    completed='<p>Total progress CARRA: '+str(progCARRA)+'% <a href="https://hirlam.org/portal/CARRA/Progress/GanntChart_CARRA.html"> (see detailed progress meter in Gantt chart) </a></p>'
    compPA='<p>Total progress PANARCTIC: '+str(progPA)+'% </p>'
    waittimes='<p><a href="https://hirlam.org/portal/CARRA/Progress/waiting_times.html"> Queue waiting times for all streams</a></p>'
    marsarxiv='<p><a href="https://hirlam.org/portal/CARRA/Progress/mars_status.html"> MARS archive throughput </a></p>'
    body = '<html><table border="1"><tr><th>expId</th><th>Current assimilated date</th><th>End date of stream </th><th> Completion date</th><th> Avg. throughput (7d) </th> <th>Avg. throughput (30d) </th> <th> Remarks</tr>'
    footer='</table></body></html>'
    cdate=get_DTG(project,stream)
    end_date = harmonconf.yaml["PROJECTS"][project]["STREAMS"][stream]["END_DATE"]
    wspeed = "("+str(speed_7d)+") days/day"
    mspeed = "("+str(speed_30d)+") days/day"
    EXTRA="TEST"
    if exists==True:
        with open(rfile, 'a') as f:
            f.write(f'<tr bgcolor="{bgcolor}"><td>{stream}</td><td>{cdate}</td><td>{end_date}</td><td>{TOAstream}</td><td>{wspeed}</td><td>{mspeed}</td><td>{extra_remark}</tr>\n')
    else:
        with open(rfile, 'w') as f:
            f.write(header+"\n")
            f.write(maintitle+"\n")
            f.write(description+"\n")
            #f.write(extranote+"\n")
            f.write(explanation+"\n")
            f.write(lastchanged+"\n")
            f.write(completed+"\n")
            f.write(compPA+"\n")
            f.write(waittimes+"\n")
            f.write(marsarxiv+"\n")
            f.write(body+"\n")
            f.write(f'<tr bgcolor="{bgcolor}"><td>{stream}</td><td>{cdate}</td><td>{end_date}</td><td>{TOAstream}</td><td>{wspeed}</td><td>{mspeed}</td><td>{extra_remark}</tr>\n')



def html_table_danra(rfile,project,stream,TOAstream,expectedDTG,speed_7d,speed_30d,streams_per_user):
    '''
    Prints a the html file using the DANRA format

    rfile[output]: the name of the html file to write 
    '''
    prog2021=progress_bar()
    progress2021='<p>Total progress: '+str(prog2021)+'% for the scheduled delivery in 2021</p>'

    gantt='<p> <a href="https://hirlam.org/portal/DKREA/Progress/GanttChart_DKREA.html"> Gantt chart showing detailed progress meter </a></p>'
    goback='<p> <a href="https://hirlam.org/portal/oprint/WebgraF/DKREA/"> Return to DKREA monitoring interface </a></p>'

    rdir='/home/ms/dk/'+streams_per_user[stream]+'/hm_home' #this is where to look for progress.log
    dtgbeg,dtgend = stream_periods(project,stream)
    pfile=os.path.join(*[rdir,stream,'progress.log'])
    exists = os.path.isfile(rfile)
    header='<!doctyle html><html><head><title>Estimated completion dates for all streams</title></head><body>'
    maintitle='<h1>Estimated completion dates and simulation speeds</h1>'
    description='<p>Stream completion date based on 30d (7d for newer runs). Set to 0 for simulations with < 7d </p>'
    lastchanged='<p>Last update: '+datetime.now().strftime('%Y/%m/%d %H:%M:%S')+' UTC</p>'

    body = '<html><table border="1"><tr><th>expId</th><th>Current assimilated date</th><th>End date of stream </th><th> Completion date</th><th> Avg. throughput (7d) </th> <th>Avg. throughput (30d) </th> </tr>'
    footer='</table></body></html>'
    with open(pfile, 'r') as f:
        lines=f.readlines()
        cdate=re.search('DTG=(.*) export',lines[0]).group(1)
    if exists==True:
        with open(rfile, 'a') as f:
            f.write('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(stream,cdate,dtgend,TOAstream,"("+str(speed_7d)+") days/day","("+str(speed_30d)+") days/day"))
            #f.write('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(stream,cdate,dtgend,TOAstream,expectedDTG, "("+str(speed_7d)+") days/day","("+str(speed_30d)+") days/day"))
    else:        
        with open(rfile, 'w') as f:
            f.write(header+"\n")
            f.write(maintitle+"\n")
            f.write(progress2021+"\n")
            f.write(gantt+"\n")
            f.write(goback+"\n")
            f.write(description+"\n")
            f.write(lastchanged+"\n")
            f.write(body+"\n")
            #f.write('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(stream,cdate,dtgend,TOAstream,expectedDTG, "("+str(speed_7d)+") days/day","("+str(speed_30d)+") days/day"))
            f.write('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(stream,cdate,dtgend,TOAstream,"("+str(speed_7d)+") days/day","("+str(speed_30d)+") days/day"))

def stream_periods(project,stream):
    '''
    Periods to run for each stream
    '''
    conf = harmonconf.yaml["PROJECTS"][project]["STREAMS"]
    beg_date = str(conf[stream]["BEG_DATE"])
    end_date = str(conf[stream]["END_DATE"])
    return beg_date,end_date


def DTG_bydate(sim,bydate,csd,avg_speed):
    '''
    Determine which simulation date we will reach for a stream by a given date (bydate)
		'''
    today=datetime.today()
    final_date = datetime.strptime(bydate,'%Y%m%d')
    togo = (final_date - today).days
    #print(f"Days to go until {final_date}: {togo}")
    if avg_speed != 0:
        days_to_simulate = avg_speed*togo # days to simulate at current speed
        DTG_expected = datetime.strptime(csd,'%Y%m%d%H') + timedelta(days=days_to_simulate)
        DTG = datetime.strftime(DTG_expected,'%Y%m%d%H')
        end_date = datetime.strftime(final_date,'%Y%m%d')
        if DTG_expected > final_date:
            print(f"WARNING: final date by {bydate} is in the future! Final date expected: {DTG}")
            print(f"Setting an upper limit equal to {bydate}-30 days")
            DTG_expected = final_date - timedelta(days=30)
            DTG = datetime.strftime(DTG_expected,'%Y%m%d%H')
        print(f"Estimated DTG by {end_date}: {DTG}")
    return DTG

def TOA_stream(project,stream,csd,cur_avg_speed,beg_date,end_date):
    '''
    Calculation of the TOA for the whole stream
    '''
    today=datetime.today()
    #stoday = datetime.strftime(datetime.today,'%Y%m%d')
    total = datetime.strptime(end_date,'%Y%m%d%H')-datetime.strptime(beg_date,'%Y%m%d%H')
    time_to_simulate=total.days
    total = datetime.strptime(csd,'%Y%m%d%H') - datetime.strptime(beg_date,'%Y%m%d%H')
    time_simulated=total.days #number of simulated days

    still_todo = time_to_simulate - time_simulated
    #still_todo_again = datetime.strptime(end_date,'%Y%m%d%H')-datetime.strptime(csd,'%Y%m%d%H')
    #print("Calc again time todo (current: %s) %d"%(csd,still_todo_again.days))
    if cur_avg_speed != 0:
        togo=still_todo/cur_avg_speed #real amount of days to go
        print("simulated time still todo %d"%still_todo)
        print("time to simulate %g"%togo)
        TOA = today + timedelta(days=togo) # the date when all should be finished at current avg speed
        TOA_print = datetime.strftime(TOA,"%Y%m%d%H")
    else:
        #check if stream is unactive because if finished
        str_comp,str_end = stream_completed(project,stream)
        if str_comp:
            print(f"{stream} ended on {str_end}")
            TOA_print=f"Finished on {str_end}"
        else:
            TOA_print="Inactive"

    return TOA_print


def get_DTG(project,stream):
    '''
    get current DTG
    '''
    user = harmonconf.yaml["PROJECTS"][project]["STREAMS"][stream]["USER"]
    local_path = "/home/ms/dk/"+user+"/hm_home"
    stream_path = os.path.join(local_path,stream)
    pfile=os.path.join(stream_path,'progress.log')

    with open(pfile, 'r') as f:
        lines=f.readlines()
        cdate=re.search('DTG=(.*) export',lines[0]).group(1)
    return cdate

def stream_completed(project,stream):
    '''
    Check a stream to see if completed,
    and return completion date
    '''
    stream_is_finished = False
    completion_date = None
    end_date = harmonconf.yaml["PROJECTS"][project]["STREAMS"][stream]["END_DATE"]
    cdate=int(get_DTG(project,stream))
    user = harmonconf.yaml["PROJECTS"][project]["STREAMS"][stream]["USER"]
    local_path = "/home/ms/dk/"+user+"/hm_home"
    stream_path = os.path.join(local_path,stream)
    pfile=os.path.join(stream_path,'progress.log')
    if cdate >= end_date:
         mtime=os.path.getmtime(pfile)
         completion_date=time.strftime('%Y%m%d',time.localtime(mtime))
         stream_is_finished = True
         print(f"from stream_completed: {stream} finished on {completion_date}")
    return stream_is_finished,completion_date

def production_start(project,stream):
    '''
    Returns the date when the production started, and a boolean if production was started
    (that is, when the warmup year was completed)
    '''
    stream_prod = False
    prod_start = None
    beg_prod = harmonconf.yaml["PROJECTS"][project]["STREAMS"][stream]["BEG_PROD"]
    csd = get_DTG(project,stream)
    dtgcur=datetime.strptime(csd,'%Y%m%d%H')
    dtgprod=datetime.strptime(beg_prod,'%Y%m%d%H')
    if dtgcur >= dtgprod:
        conn=sqlite3.connect(dbase)
        sql_command = "SELECT * FROM daily_logs"
        data=pd.read_sql(sql_command, conn)
        search_string = "/".join([csd[0:4],csd[4:6],csd[6:8]])
        get_date=data.logfile.str.contains(search_string)
        if get_date.empty:
            print(f"Date {search_string} not found in record for {stream}")
            sys.exit(1)
        prod_start = get_date["yyymmdd"]
        stream_prod = True
        
    return stream_prod,prod_start


def sim_speed_total(use_streams,project,cur_avg_speed):
    '''
    Calculates real and ideal speed (target and min speed)
    for the whole project (all streams) or a selected subset
    Takes into account the warmup period
    Returns min and target speed based on the length of each stream
    Also provides an estimate of the TOA for the end of the warm-up year, but this can be changed
    based on the current 1-week moving-average.
    '''
    buffer_days = BUFFER_DAYS
    from dateutil import relativedelta
    sim_total = 0
    if use_streams is None:
        streams = [key for key in harmonconf.yaml["PROJECTS"][project]["STREAMS"].keys()]
    elif "," in use_streams:
        streams = use_streams.split(",")

    for stream in streams:
        csd = get_DTG(project,stream)
        beg_date = str(harmonconf.yaml["PROJECTS"][project]["STREAMS"][stream]["BEG_DATE"])
        end_date = str(harmonconf.yaml["PROJECTS"][project]["STREAMS"][stream]["END_DATE"])
        beg_prod = str(harmonconf.yaml["PROJECTS"][project]["STREAMS"][stream]["BEG_PROD"])
        warmupdays2sim = (datetime.strptime(end_date,'%Y%m%d%H') - datetime.strptime(beg_prod,"%Y%m%d%H")).days
        sim_total += (datetime.strptime(end_date,'%Y%m%d%H') - datetime.strptime(csd,"%Y%m%d%H")).days
    print(f"Total number of days simulated so far for all streams {sim_total}")
    today=datetime.today()
    #These are dates for the whole project
    beg_proj = str(harmonconf.yaml["PROJECTS"][project]["BEG_DATE"])
    end_proj = str(harmonconf.yaml["PROJECTS"][project]["END_DATE"])
    #total number of project days
    pdays = (datetime.strptime(end_proj,'%Y%m%d')-datetime.strptime(beg_proj,'%Y%m%d')).days
    #Number of warmup days
    #total number of days to simulate for this stream
    pdays_passed = (today - datetime.strptime(beg_proj,'%Y%m%d')).days#number of days already spent
    pdays_left = pdays - pdays_passed
    print(f"Project days remaining {pdays_left}")
    
    min_speed = sim_total/pdays_left #min speed we need to have to end the project
    if pdays_left > buffer_days:
        target_speed = sim_total/(pdays_left-buffer_days) #same as above, but accounting for 2 months buffer
    elif pdays_left >= 10:
        target_speed = sim_total/(pdays_left-10) #same as above, but accounting for 10 days
    else:
        print("Simulation has been running for less than 10 days, target_speed is the same as min_speed")
        target_speed = sim_total/pdays_left
    print(f"min and target speed: {min_speed},{target_speed}")
    #Simulated days
    #csd = get_DTG(stream)
    #days_to_simulate=datetime.timedelta(days=warmupdays2sim)
    #dtgcur=datetime.strptime(csd,'%Y%m%d%H')
    #time_simulated = datetime.strptime(csd,'%Y%m%d%H') - datetime.strptime(beg_date,'%Y%m%d%H')
    #time_to_simulate = days_to_simulate.days - time_simulated.days
    #print("Remaining days in %s stream %d for warmup phase: %d (last DTG read: %s)"%(domain,slabel,time_to_simulate,dtgcur))
    #if cur_avg_speed != 0 and not stream_completed(stream):
    #    togo=time_to_simulate/cur_avg_speed #days to go for warmup at current speed
    #    if time_to_simulate < 0:
    #        print("Warmup year already completed for %s stream %d"%(domain,slabel))
    #        togo = 0
    #        TOAproduction = production_start(stream)
    #    else:
    #        TOAproduction = today + datetime.timedelta(days=togo) # the date when all should be finished at current avg speed and the production should start
    #elif completed_streams[streamname]:
    #    TOAproduction=datetime.strptime(completed_streams_dates[streamname],'%Y%m%d')
    #    min_speed = 0.0
    #    target_speed = 0.0
    #else:
    #    TOAproduction=datetime(2099,12,31,0,0,0) #"9999"
    return min_speed, target_speed #, TOAproduction

def days2go(project,stream):
    '''
    Calculation of days to go for a stream
    '''
    beg_date = str(harmonconf.yaml["PROJECTS"][project]["STREAMS"][stream]["BEG_DATE"])
    end_date = str(harmonconf.yaml["PROJECTS"][project]["STREAMS"][stream]["END_DATE"])
    csd = get_DTG(project,stream)
    today=datetime.today()
    total = datetime.strptime(end_date,'%Y%m%d%H')-datetime.strptime(beg_date,'%Y%m%d%H')
    total_simulated = datetime.strptime(csd,'%Y%m%d%H') - datetime.strptime(beg_date,'%Y%m%d%H')
    days_togo = total.days - total_simulated.days
    print(f"Total number of days to simulate in {stream} = {total.days}")
    print(f"Still to go in {stream} = {days_togo}")
    print(f"Progress so far: {total.days-days_togo}")
    return days_togo


def speed_stream(project,stream):
    '''
    returns the min and target speed
    '''
    
    #update project days to go as of today
    today=datetime.today()
    end_real = str(harmonconf.yaml["PROJECTS"][project]["END_DATE"])
    finalday_real = datetime.strptime(end_real,'%Y%m%d')

    end_real_date = datetime.strptime(end_real,"%Y%m%d")
    finalday_ideal = end_real_date - timedelta(days=BUFFER_DAYS)  

    projdays_ideal = (finalday_ideal - today).days
    projdays_real = (finalday_real - today).days

    #update days to go in current stream
    togo_sim = days2go(project,stream)
    print(f"Days still to simulated in {stream}:{togo_sim}")
    print(f"Days remaining in project: {finalday_real}")
    min_speed = togo_sim/projdays_real #same as above, but accounting for 2 months buffer
    target_speed = togo_sim/projdays_ideal #total number of project days remaining from 20190626
    return min_speed,target_speed



