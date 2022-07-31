def student_search(netid, name, year, d):
    name = name.lower() if name else ''
    netid = netid.lower() if netid else ''
    year = int(year)
    if not name and not netid and year==-1: # if all null
        return {} # return empty list
    ret = {}
    for student in d:
        student['grad_year'] = student['grad_year'] if student['grad_year'] else 0 #some grad_year values (cmmorretti) are null instead of 0
        if (name in student['full_name'].lower()) \
                and (netid in student['netid']) \
                and (year == -1 or year%100 == student['grad_year']%100): # some grad_year_values are 24 vs 2024
            ret[student['netid']] = student['full_name']
    return ret
