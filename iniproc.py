# iniproc.py
# Why use a 1300 line module when all I want is to
#   get values from an ini file?
# This is my module to read and return ini file key values
# Keys are case-sensitive


def striplist(lst):
    ''' strip items in a list and return list '''
    L = [i.strip() for i in lst]
    return L


def read(inifile, *keys):
    ''' Open and read text file having "key = value" lines
        Build a dictionary - use it to build a list of
        values to return in the order received.
    '''

    kv = []  # one key/value item from ini file

    kvs = {}  # key/value dictionary built from ini file

    rtv = []  # return values stored here in kargs order

    with open(inifile) as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            if line.startswith('#'):
                continue
            # Build dictionary line by line from ini file
            kv = line.split('=')
            kv = striplist(kv)
            kvs[kv[0]] = kv[1]  # add to dictionary

    # Append requested key values and return list
    for v in keys:
        try:
            rtv.append(kvs[v])
        except:
            print("Key Error:", v)
            rtv.append(0)

    return rtv
