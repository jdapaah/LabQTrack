import requests

def student_search(netid, name, year, authenticate):
    url = "https://www.labqueue.io/api/v1/queues/intro-cs-lab/roster/"
    ret = {}
    name = name.lower() if name else name
    netid = netid.lower() if netid else netid
    while url:
        result = requests.get(url, auth=authenticate)
        d: dict = result.json()
        for student in d['results']:
            if (name in student['full_name'].lower()) \
                    and netid in student['netid']\
                    and (not year or year == student['grad_year']):
                ret[student['netid']] = student['full_name']
            url = d['next']
    return ret
