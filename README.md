# DVSEvents

## dvsfile

dvsfile folder containing file dvs.py who can be used to read dvs datas and use these data with nengo simulator. See [relative Readme.md](dvsFile/Readme.md) for more informations.

## DVSModule

DVSModule folder containing python librairi, which can be installed with *pip*. As dvs.py, DVSModule can be used to rad dvs datas and send these dtata to nengo simulator but add two specific interface to add more user possibility. See [relative Readme.md](DVSModule/Readme.md) for more informations.

# Documentary sources

- https://inivation.github.io/inivation-docs/Software%20user%20guides/AEDAT_file_formats.html#aedat-10 : AER file format documentation
- https://gist.github.com/elijahc/f2444a8eaaf820b939214d8e212f8b55 : Example of python script for loading aerdat file
- https://www.nengo.ai/nengo-loihi/examples/dvs-from-file.html : example of pythopn who load aer data and use these data with nengo simulator
- https://github.com/nengo/nengo-loihi/blob/master/nengo_loihi/dvs.py#L10-L142 : source code of nengo process class who use aer data