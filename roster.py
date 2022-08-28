def student_search(netid, name, year, roster):
    name = name.lower().strip() if name else ''
    netid = netid.lower().strip() if netid else ''
    year = int(year)

    if not name and not netid and year == -1:  # if all null
        return 2, {}  # return empty list
    ret = {}
    for full_netid in roster:
        student = roster[full_netid]
        if (name in student['name'].lower()) \
                and (netid in full_netid) \
                and (year == -1 or year == student['year']):
            ret[full_netid] = student['name']
            if len(ret) > 15:
                return 1, {}
    if len(ret) == 0:
        return 2, {}
    return 0, ret
