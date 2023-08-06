#!/usr/bin/env python
"""
  Methods for querying the JPL Horizons database. 

  Instructions for keywords and options available here:
    ftp://ssd.jpl.nasa.gov/pub/ssd/horizons_batch_example.long

  Example call to this script:
    python get_ephem.py '899' '568' '2021-10-08 00:00' '2021-10-09 00:00' '30 minutes' '1,3,4,8,9,12,13,14,15,17,19,20'

  v0: M. Adamkovics
  v1: K. de Kleer
  v2: 2017-06-15 E. Molter
            added naif_lookup
            adapted to fit into whats_up.py
  v3: 2022-02-11 E. Molter
            added arg parser to support command line call
TO DO: add parser for output from JPL
    get_ephemerides should return a pd.DataFrame()
    will need dictionary of names for EVERY column ID 
    most of this should be written somewhere in whats_up
"""

from urllib.request import urlopen, urlretrieve
import urllib
import numpy as np
import pandas as pd
from time import strftime, gmtime, time
from datetime import datetime,timedelta
import sys, os, warnings, argparse, io
from pkg_resources import resource_string


def parse_arguments(args):
    
    parser = argparse.ArgumentParser(description='Web scraper for JPL Horizons ephemerides')
    
    parser.add_argument('code', nargs='?', help='JPL Horizons target name or NAIF ID, e.g. "Despina"')
    parser.add_argument('obscode', nargs='?', help='JPL Horizons observatory code, e.g. "568" for Maunakea')
    parser.add_argument('tstart', nargs='?', help='Observation start time in format "YYYY-MM-DD HH:MM"')
    parser.add_argument('tend', nargs='?', default = None, const=None, help='Observation end time in format "YYYY-MM-DD HH:MM". Default one minute after start time, i.e. a single line is returned')
    parser.add_argument('stepsize', nargs='?', default = '30 minutes', const='', help='Time interval between lines of output. Default: "30 minutes"')
    parser.add_argument('quantities', nargs='?', default = '1,3,4,8,9,12,13,14,15,17,19,20', const='1,3,4,8,9,12,13,14,15,17,19,20', help='Horizons column IDs (quantities of interest) that will be returned. Default: "1,3,4,8,9,12,13,14,15,17,19,20"')
    parser.add_argument('--version', action='version', version='0.0.1')
    
    args = parser.parse_args(args)
    if args.tend is None:
        args.tend = args.tstart
    
    return args


def horizons_message_lookup(mess_code, elev='', airmass='', ang_sep='', moon_dist=''):
    '''decodes message codes from JPL Horizons
    o = elevation ok, m = elevation below min, x = elevation above max
    o = airmass ok, x = airmass above max
    o = separation ok, m = separation below min, z = this is parent body, or no data
    o = visibility ok, e = eclipse, c = occultation, t = transit
    example: 'oozc' -> elevation ok, airmass ok, separation not specified, body is occulted by parent
    '''
    #elevation
    message = []
    if mess_code[0] == 'o':
        message.append('Elevation is ok: '+str(elev)+' degrees.')
    elif mess_code[0] == 'm':
        message.append('Elevation is too low: '+str(elev)+' degrees.')
    elif mess_code[0] == 'x':
        message.append('Elevation is too near zenith: '+str(elev)+' degrees.')

    #airmass
    if mess_code[1] == 'o':
        message.append('Airmass is ok: '+str(airmass))
    elif mess_code[1] == 'x':
        message.append('Airmass is too high: '+str(airmass))

    #angular sep
    if mess_code[2] == 'o':
        message.append('Angular separation from host planet is ok: angular separation = '+str(ang_sep)+' arcsec.')
    elif mess_code[2] == 'm':
        message.append('Too close to host planet: angular separation = '+str(ang_sep)+' arcsec.')
    elif mess_code[2] == 'x':
        message.append('Minimum angular separation from parent body not specified (or target is itself a parent body)')
    
    #occultations and eclipses
    if mess_code[3] == 'o':
        message.append('No occultations or eclipses.')
    elif mess_code[3] == 'e':
        message.append('Target is in total or partial eclipse!')
    elif mess_code[3] == 'c':
        message.append('Target is occulted by parent!')
    elif mess_code[3] == 't':
        message.append('Target is transiting parent!')

    #distance from moon
    if mess_code[4] == 'o':
        message.append('Moon distance is ok.')
    elif mess_code[4] == 'm':
        message.append('Target is too close to the moon: angular distance = '+str(moon_dist)+' degrees.')
    elif mess_code[4] == 'x':
        message.append('No minimum moon distance specified.')
        
    return message

    
def read_ephem_line(arr):
    '''converts ephemeris data to float, putting np.nan for "n.a."'''
    arr_out = []
    for s in arr:
        if s.strip() == 'n.a.':
            arr_out.append(np.nan)
        else:
            arr_out.append(float(s))
    return np.asarray(arr_out)
    
    
def read_ephem(ephem_response, quantities):
    '''
    Take in the output from the call to Horizons
    turn it into a Pandas dataframe
    '''
    horizons_column_name_table = io.StringIO(resource_string(__name__, 'data/horizons_column_name_table.txt').decode("utf-8"))
    
    ephem_columns = pd.read_csv(horizons_column_name_table).apply(lambda x: x.str.strip() if x.dtype == "object" else x) #strip whitespace
    
    keys_want = [int(s) for s in quantities.split(',')]
    cols_to_use = ephem_columns['id'].astype(int).isin(keys_want)
    cols_to_use[ephem_columns['id'] == 0] = True
    column_names = ephem_columns[cols_to_use]['short_name']
    
    response_df = pd.DataFrame(ephem_response, columns = column_names.values)
    
    return response_df


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def naif_lookup(target):
    '''looks up NAIF ID for target body in naif_id_table.txt'''
    
    target = target.upper().strip(', \n')
    naif_id_table = io.StringIO(resource_string(__name__, 'data/naif_id_table.txt').decode("utf-8"))
    naif_df = pd.read_csv(naif_id_table).apply(lambda x: x.str.strip() if x.dtype == "object" else x) #strip whitespace
    naif_df['name'] = naif_df['name'].str.strip("'")
    
    good_idx = naif_df['name'].astype(str).isin([target.upper()])
    code = naif_df[good_idx]['naifid'].values
    if len(code) == 1:
        code = code[0].astype(str)
    else:
        raise ValueError('NAIF lookup did not find the specified target!')
    
    if len(code) == 7: #minor body
        if code[0] == '2': #asteroid
            return code[1:]+';'
        elif code[0] =='1': #comet
            raise NotImplementedError('Comets cannot be looked up by NAIF ID; Horizons generates multiple codes for every comet. Try your search in the Horizons Web tool, select the target body you want, and then copy the exact string into this code and it *may* work.')
        return code
    return code
                      
    

def get_ephemerides(code, obs_code, tstart, tend, stepsize, quantities = None):
    """
    input NAIF target code, e.g. 501 for Io, and date in the format:
    'YYYY-MM-DD HH:MM'
    For example: data=get_ephem.get_ephemerides('501','2017-06-09 08:24')
    Returns a list containing (in string format):
    UTdate and time,sun,moon,RA (J2000),DEC (J2000),dra,ddec,azimuth,elevation,Airmass,Extinction,APmag,s-brt,Ang-Diam("),ang-sep("),visibility,Ob-lon,Ob-lat,NP.ang,NP.dist
    """
    if quantities == None:
        quantities = '1,3,4,8,9,12,13,14,15,17,19,20'
    try:
        int(code)
    except:
        code = naif_lookup(code)

    tstart_obj = datetime.strptime(tstart,'%Y-%m-%d %H:%M')
    tend_obj = datetime.strptime(tend,'%Y-%m-%d %H:%M')
    if tend_obj - tstart_obj <= timedelta(minutes = 1):
        warnings.warn('End time before start time. Setting end time to one minute after start time.')
        tend_obj = tstart_obj + timedelta(minutes = 1)
    
    tstart_UT = datetime.strftime(tstart_obj,"'%Y-%m-%d %H:%M'")
    tend_UT = datetime.strftime(tend_obj,"'%Y-%m-%d %H:%M'")

    http = "https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1"
    make_ephem = "&MAKE_EPHEM='YES'&TABLE_TYPE='OBSERVER'"
    command    = "&COMMAND=" + str(code)
    center     = "&CENTER="+str(obs_code)  #568 is Mauna Kea, 662 is Lick, etc
    t_start    = "&START_TIME=" + tstart_UT
    t_stop     = "&STOP_TIME=" + tend_UT
    t_step     = "&STEP_SIZE='" + stepsize + "'"
    qs = "&QUANTITIES='%s'"%quantities
    csv        = "&CSV_FORMAT='YES'"

    url = http+make_ephem+command+center+t_start+t_stop+t_step+qs+csv
    url = url.replace(" ", "%20")
    url = url.replace("'", "%27")
    try:
        with urlopen(url) as response:
            ephem = response.readlines()  
    except:
        raise ValueError('Could not retrieve query from Horizons. Check Internet connection and input URL')

    inephem = False
    data = []
    for i in range(len(ephem)) :
        if type(ephem[i]) != str:
            ephem[i] = ephem[i].decode('UTF-8')
        if inephem == False:
            #get observatory lat, lon, alt for later
            if ephem[i].startswith('Center geodetic :'):
                l = ephem[i].split(':')[1]
                latlonalt = l.split()[0]
                [lon,lat,alt] = [float(s.strip(', \n')) for s in latlonalt.split(',')]
                observatory_coords = [lat,lon,alt]
            if ephem[i].startswith('$$SOE') :
                inephem=True
                #data = [ephem[i+1].decode('UTF-8').split(',')]
        elif inephem == True:
            if ephem[i].startswith("$$EOE") :
                inephem=False
            else:
                data.append(ephem[i].split(','))
    try:
        out = np.asarray(data)[:,:-1]
    except:
        raise ValueError('Ephemeris data not found. Check that the target has valid ephemeris data for the specified time range.')
        
    out_pd = read_ephem(out, quantities)
    
    return out_pd, observatory_coords
        
if __name__ == "__main__":
    
    args = parse_arguments(sys.argv[1:])
        
    response_df, observatory_coords = get_ephemerides(args.code, args.obscode, args.tstart, args.tend, args.stepsize, args.quantities)
    print(response_df)
    
    ## TO DO: make this output as a pandas dataframe that looks nice!
    
    
        
        