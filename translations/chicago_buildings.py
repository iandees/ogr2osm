'''
A translation function for City of Chicago building footprints data. 

The shapefiles are availble under "Public" license as "building footprints" from Cook County:
https://data.cityofchicago.org/Buildings/Building-Footprints/w2v3-isjw

The following fields are used:    

Field           Used for            Reason
STORIES         building:levels=*
BLDG_NAME1      name=*
F_ADD1          addr:housenumber=*
T_ADD1          ^
PRE_DIR1        addr:street=*
ST_NAME1        ^
ST_TYPE1        ^
SUF_DIR1        ^
YEAR_BUILT      start_date=*

'''
suffixlookup = {
'AVE':'Avenue',
'RD':'Road',
'ST':'Street',
'PL':'Place',
'CRES':'Crescent',
'BLVD':'Boulevard',
'DR':'Drive',
'LANE':'Lane',
'CRT':'Court',
'GR':'Grove',
'CL':'Close',
'RWY':'Railway',
'DIV':'Diversion',
'HWY':'Highway',
'TER':'Terrace',
'CONN': 'Connector',
'E':'East',
'S':'South',
'N':'North',
'W':'West'}
    
def translateName(rawname):
    '''
    A general purpose name expander.
    '''

    return (suffixlookup[rawname]) if rawname in suffixlookup else rawname

    
def filterTags(attrs):
    if not attrs:
        return
    tags = {}

    tags['building'] = 'yes'
    tags['cookcounty:building_id'] = attrs['BLDG_ID']
    
    if len(attrs['ST_NAME1']) > 0:
        prefix = translateName(attrs['PRE_DIR1'])
        if prefix:
            tags['addr:street:prefix'] = prefix

        street_name = attrs['ST_NAME1']
        if street_name:
            tags['addr:street:name'] = street_name.title()

        street_type = translateName(attrs['ST_TYPE1'])
        if street_type:
            tags['addr:street:type'] = street_type

        suffix = translateName(attrs['SUF_DIR1'])
        if suffix:
            tags['addr:street:suffix'] = suffix

        name = ("%s %s %s %s" % (prefix, street_name, street_type, suffix)).strip().title()

        tags['addr:street'] = name
        
    if attrs['F_ADD1'] != '0' and attrs['T_ADD1'] != '0':
        from_addr = attrs['F_ADD1']
        to_addr = attrs['T_ADD1']

        if from_addr == to_addr:
            tags['addr:housenumber'] = from_addr
        elif from_addr < to_addr:
            tags['addr:from'] = from_addr
            tags['addr:to'] = to_addr
                   
    return tags
