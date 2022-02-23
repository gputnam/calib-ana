First-Time Setup:

To get the right python on the FNAL servers:
`source /cvmfs/icarus.opensciencegrid.org/products/icarus/setup_icarus.sh`
`setup python v3_9_9`

Make a virtual environment (with python >= 3):
python -m venv env
. env/bin/activate
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
pip install -r requirelandau.txt

Producing a HDF5 file for analysis
`python make_etau_df.py [output.df] [inputs.root,]`

where each input.root file is ca Calibration N-Tuple.
One may also give the second argument as a file which containts a list
of ROOT files. Then, that file must end in .list.

Run the jupyter notebook ELifetime.ipynb to get the electron lifetime.
NOTE: always run nbstripout before commiting updates to notebooks:

`nbstripout *.ipynb`
