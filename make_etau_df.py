import sys
import datetime as dt
from lib.ntuple_glob import NTupleGlob
from lib import branches
import numpy as np
import pandas as pd

# load constants
from lib.constants import *

NCHUNK = 10
PLANE = 2
SPNAME = "p"

plane2branches = [
    "h.%s.x" % SPNAME, "h.%s.y" % SPNAME, "h.%s.z" % SPNAME, "h.time", "h.tpc", "h.wire", "h.channel", "h.integral", "pitch", "h.sumadc", "i_snippet", "h.width"
]
plane2branches = ["hits%i.%s" % (PLANE, s) for s in plane2branches]

truehitbranches = [
    "channel", "ndep", "nelec", "e", "pitch",
]
truehitbranches = ["truth.p.truehits%i.%s" % (PLANE, s) for s in truehitbranches]

def isTPCE(df):
    return df.tpc <= 1

def reduce_df(df, truedf=None):
    # Select anode + cathode crossing tracks
    select_track = df.selected == 1

    hits = df["hits%i" % PLANE]
    
    df = df[(hits.pitch > 0) & select_track].copy()
    df["chunk"] = df.index.get_level_values(1) // NCHUNK
    df["tpcE"] = isTPCE(hits.h)
    # Ignore hits that are not the first in a snippet on a track.
    # In the aggregation function (median) below, these entries will
    # be skipped in the computation
    df.loc[hits.i_snippet > 0, ("h", "sumadc", "", "")] = np.nan 

    # Add in truth if we can
    if truedf is not None:
        truedf = truedf.truth.p["truehits%i" % PLANE]
        truedf.columns = pd.MultiIndex.from_tuples([("true_" + s, '', '', '') for s in truedf.columns]) 
        df = df.merge(truedf, left_on=['entry', ('hits%i' % PLANE, 'h', 'channel', '')], 
                                          right_on=['entry', ('true_channel', '', '', '')],
                                          how="left", validate="many_to_one")
    else:
        df["true_nelec"] = -1.
        df["true_e"] = -1.

    hitsname = "hits%i" % PLANE

    outdf = df.groupby(["entry", "chunk"])[[(hitsname, 'h', 'integral', ''),
                                            ('h', 'sumadc', '', ''),
                                            ('pitch', '', '', ''),
                                            ('true_nelec', '', '', ''),
                                            ('true_e', '', '', ''),
                                          ]].sum()

    outdf = outdf.join(df.groupby(["entry", "chunk"])[[(hitsname, 'h', SPNAME, 'x'),
                                                      (hitsname, 'h', SPNAME, 'y'),
                                                      (hitsname, 'h', SPNAME, 'z'),
                                                      (hitsname, 'pitch', '', ''),
                                                      (hitsname, 'h', 'time', ''),
                                                      (hitsname, 'h', 'width', ''),
                                                     ]].mean())
    
    outdf.columns = ["charge", "sumadc", 'pitch', 'true_nelec', 'true_e', "x", "y", "z", "pitch", "time", "width"]

    # dt along chunk
    if NCHUNK > 1:
        dt = df.groupby(["entry", "chunk"])[[(hitsname, "h", "time", "")]].diff()
        dt.columns = ["dt"]
        dt = dt.join(df.chunk)
        dt = dt.groupby(["entry", "chunk"]).dt.mean()
        outdf = outdf.join(dt)
    else:
        outdf["dt"] = np.nan
    
    # TPC/Cryo info
    outdf["tpcE"] = df.groupby(["entry", "chunk"]).tpcE.all()
    outdf["tpcW"] = (~outdf.tpcE) & (df.groupby(["entry", "chunk"]).tpcE.nunique() == 1)

    # Save T0
    outdf["pandora_t0"] = df.groupby(["entry", "chunk"]).t0.first()
    # also save the cryostat number
    outdf["cryostat"] = df.groupby(["entry", "chunk"]).cryostat.first()
    # And run number
    outdf["run"] = df.groupby(["entry", "chunk"])[[('meta', 'run', '', ''),]].first()

    # Only save chunks that are all in one TPC
    outdf = outdf[outdf.tpcE | outdf.tpcW].drop(columns=["tpcW"])
   
    return outdf


def main(output, inputs):
    ntuples = NTupleGlob(inputs, branches.trkbranches + plane2branches + truehitbranches)
    df = ntuples.dataframe(nproc="auto", f=reduce_df)
    df.to_hdf(output, key="df", mode="w")

if __name__ == "__main__":
    printhelp = len(sys.argv) < 3 or sys.argv[1] == "-h"
    if printhelp:
        print("Usage: python make_etau_df.py [output.df] [inputs.root,]")
    else:
        main(sys.argv[1], sys.argv[2:])
