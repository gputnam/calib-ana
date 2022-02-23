First-Time Setup:

Make a virtual environment:
python3 -m venv env
pip3 install -r requirements.txt
pip3 install -r requirelandau.txt

Producing a HDF5 file for analysis
python make_etau_df.py [output.df] [inputs.root,]

where each input.root file is ca Calibration N-Tuple.
One may also give the second argument as a file which containts a list
of ROOT files. Then, that file must end in .list.

Run the jupyter notebook DriftDirNormalization.ipynb to get the electron lifetime.
