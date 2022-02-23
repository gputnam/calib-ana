First-Time Setup:

Make a virtual environment:
python -m venv env
. env/bin/activate
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
pip install -r requirelandau.txt

Producing a HDF5 file for analysis
python make_etau_df.py [output.df] [inputs.root,]

where each input.root file is ca Calibration N-Tuple.
One may also give the second argument as a file which containts a list
of ROOT files. Then, that file must end in .list.

Run the jupyter notebook DriftDirNormalization.ipynb to get the electron lifetime.
