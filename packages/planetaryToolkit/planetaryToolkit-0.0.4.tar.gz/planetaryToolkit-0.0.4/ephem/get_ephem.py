#!/usr/bin/env python
"""Methods for querying the JPL Horizons database.

This module interacts with the JPL Horizons API
to retrieve ephemeris data on planets, moons, and asteroids.
If you ever experience issues with inputs, ensure a manual call
works here: https://ssd.jpl.nasa.gov/horizons/app.html#/

Usage
-----
To get help with command-line application usage, run:

    $ python get_ephem.py -h

Examples
--------
Query to return useful information about Neptune (code 899) position and orientation as viewed by Keck
    $ python get_ephem.py '899' '568' '2021-10-08 00:00' '2021-10-09 00:00' '30 minutes' '1,3,4,8,9,12,13,14,15,17,19,20'
Query to return all fields on Proteus, where Proteus code is looked up in NAIF table
    $ python get_ephem.py 'Proteus' '-7' '2021-10-08 00:00' '2021-10-09 00:00' '2 hours' 'all'

History
-------
v0: M. Adamkovics
v1: K. de Kleer
v2: 2017-06-15 E. Molter
          added naif_lookup
          adapted to fit into whats_up.py
v3: 2022-02-11 E. Molter
          added arg parser to support command line call
          now returns a pandas dataframe

Notes
-----
Reads in text data located in 
planetaryToolkit/ephem/data/ using pkg_resources

To-Do List
----------
    make it so the output dataframe has a datetime index
    make a Jupyter notebook demonstrating get_ephem
    improve the long_names in horizons_column_name_table.txt
    units column in horizons_column_name_table.txt
"""

from urllib.request import urlopen
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys
import warnings
import argparse
import io
from pkg_resources import resource_string


def parse_arguments(args):

    parser = argparse.ArgumentParser(
        description="Web scraper for JPL Horizons ephemerides"
    )

    parser.add_argument(
        "code", nargs="?", help='JPL Horizons target name or NAIF ID, e.g. "Despina"'
    )
    parser.add_argument(
        "obscode",
        nargs="?",
        help='JPL Horizons observatory code, e.g. "568" for Maunakea',
    )
    parser.add_argument(
        "tstart", nargs="?", help='Observation start time in format "YYYY-MM-DD HH:MM"'
    )
    parser.add_argument(
        "tend",
        nargs="?",
        default=None,
        const=None,
        help='Observation end time in format "YYYY-MM-DD HH:MM"',
    )
    parser.add_argument(
        "stepsize",
        nargs="?",
        default="30 minutes",
        const="",
        help='Time interval between lines of output, e.g. "30 minutes"',
    )
    parser.add_argument(
        "quantities",
        nargs="?",
        default="1,3,4,8,9,12,13,14,15,17,19,20",
        const="1,3,4,8,9,12,13,14,15,17,19,20",
        help='Horizons column IDs (quantities of interest) that will be returned, e.g. "1,3,4,8,9,12,13,14,15,17,19,20"',
    )
    parser.add_argument("--version", action="version", version="0.0.1")

    args = parser.parse_args(args)
    if args.tend is None:
        args.tend = args.tstart

    return args


def read_ephem(ephem_response, quantities):
    """
    Description
    -----------
    converts almost-raw response from Horizons API into pandas dataframe
    gets column names from data/horizons_column_name_table.txt
    
    Parameters
    ----------
    ephem_response : np.ndarray
    quantities : str
    
    Returns
    -------
    pandas.DataFrame
        Horizons data labeled according to data/horizons_column_name_table.txt
    """
    horizons_column_name_table = io.StringIO(
        resource_string(__name__, "data/horizons_column_name_table.txt").decode("utf-8")
    )

    ephem_columns = pd.read_csv(horizons_column_name_table).apply(
        lambda x: x.str.strip() if x.dtype == "object" else x
    )  # strip whitespace

    keys_want = [int(s) for s in quantities.split(",")]
    cols_to_use = ephem_columns["id"].astype(int).isin(keys_want)
    cols_to_use[ephem_columns["id"] == 0] = True
    column_names = ephem_columns[cols_to_use]["short_name"]

    response_df = pd.DataFrame(ephem_response, columns=column_names.values)
    response_df = response_df.set_index(pd.DatetimeIndex(response_df['datetime']))

    return response_df


def naif_lookup(target):
    """
    Description
    -----------
    converts name of target body to naif id
    using lookup table located at data/naif_id_table.txt
    
    Parameters
    ----------
    target : str
    
    Returns
    -------
    str
        naif code
    """

    target = target.upper().strip(", \n")
    naif_id_table = io.StringIO(
        resource_string(__name__, "data/naif_id_table.txt").decode("utf-8")
    )
    naif_df = pd.read_csv(naif_id_table).apply(
        lambda x: x.str.strip() if x.dtype == "object" else x
    )  # strip whitespace
    naif_df["name"] = naif_df["name"].str.strip("'")

    good_idx = naif_df["name"].astype(str).isin([target.upper()])
    code = naif_df[good_idx]["naifid"].values
    if len(code) == 1:
        code = code[0].astype(str)
    else:
        raise ValueError("NAIF lookup did not find the specified target!")

    if len(code) == 7:  # minor body
        if code[0] == "2":  # asteroid
            return code[1:] + ";"
        elif code[0] == "1":  # comet
            raise NotImplementedError(
                "Comets cannot be looked up by NAIF ID; Horizons generates multiple codes for every comet. Try your search in the Horizons Web tool, select the target body you want, and then copy the exact string into this code and it *may* work."
            )
        return code
    return code


def get_ephemerides(
    code, obs_code, tstart, tend, stepsize, quantities="1,3,4,8,9,12,13,14,15,17,19,20"
):
    """
    Description
    -----------
    interacts with the JPL Horizons API to retrieve ephemeris data
    
    Parameters
    ----------
    code : str or int
        naif id of target body
    obs_code : str or int
        observatory code
    tstart : str
        start time, format %Y-%m-%d %H:%M
    tend : str
        end time, format %Y-%m-%d %H:%M
    stepsize : str
        time step between rows of output
        must be readable by Horizons, e.g. '30 minutes'
    quantities : str, optional
        Horizons column ids to query
        Can be list of form '1,2,3,5,8,13' or 'all'
    
    Returns
    -------
    list
        location of observatory in format [lon, lat, elevation]
    pandas.DataFrame
        output from the Horizons query as a labeled data frame
    """

    if quantities == "all":
        quantities = ",".join([str(i) for i in range(1, 49)])
    try:
        int(code)
    except:
        code = naif_lookup(code)

    tstart_obj = datetime.strptime(tstart, "%Y-%m-%d %H:%M")
    tend_obj = datetime.strptime(tend, "%Y-%m-%d %H:%M")
    if tend_obj - tstart_obj <= timedelta(minutes=1):
        warnings.warn(
            "End time before start time. Setting end time to one minute after start time."
        )
        tend_obj = tstart_obj + timedelta(minutes=1)

    tstart_UT = datetime.strftime(tstart_obj, "'%Y-%m-%d %H:%M'")
    tend_UT = datetime.strftime(tend_obj, "'%Y-%m-%d %H:%M'")

    http = "https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1"
    make_ephem = "&MAKE_EPHEM='YES'&TABLE_TYPE='OBSERVER'"
    command = "&COMMAND=" + str(code)
    center = "&CENTER=" + str(obs_code)  # 568 is Mauna Kea, 662 is Lick, etc
    t_start = "&START_TIME=" + tstart_UT
    t_stop = "&STOP_TIME=" + tend_UT
    t_step = "&STEP_SIZE='" + stepsize + "'"
    qs = "&QUANTITIES='%s'" % quantities
    csv = "&CSV_FORMAT='YES'"

    url = http + make_ephem + command + center + t_start + t_stop + t_step + qs + csv
    url = url.replace(" ", "%20")
    url = url.replace("'", "%27")
    try:
        with urlopen(url) as response:
            ephem = response.readlines()
    except:
        raise ValueError(
            "Could not retrieve query from Horizons. Check Internet connection and input URL"
        )

    inephem = False
    data = []
    for i in range(len(ephem)):
        if type(ephem[i]) != str:
            ephem[i] = ephem[i].decode("UTF-8")
        if not inephem:
            # get observatory lon, lat, alt
            if ephem[i].startswith("Center geodetic :"):
                l = ephem[i].split(":")[1]
                latlonalt = l.split()[0]
                [lon, lat, alt] = [float(s.strip(", \n")) for s in latlonalt.split(",")]
                observatory_coords = [lat, lon, alt]
            if ephem[i].startswith("$$SOE"):
                inephem = True
        elif inephem:
            if ephem[i].startswith("$$EOE"):
                inephem = False
            else:
                data.append(ephem[i].split(","))
    try:
        out = np.asarray(data)[:, :-1]
    except:
        raise ValueError(
            "Ephemeris data not found. Check that the target has valid ephemeris data for the specified time range."
        )

    out_pd = read_ephem(out, quantities)

    return out_pd, observatory_coords


if __name__ == "__main__":

    args = parse_arguments(sys.argv[1:])

    response_df, observatory_coords = get_ephemerides(
        args.code, args.obscode, args.tstart, args.tend, args.stepsize, args.quantities
    )
    print(response_df)
