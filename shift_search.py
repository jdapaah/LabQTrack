from wsse.client.requests.auth import WSSEAuth
import requests
import statistics
from auth import username, API_SECRET

wsse_auth = WSSEAuth(username, API_SECRET)

"""
Check for a specific shift, if people are contributing enough. Precisiely,
determine if any Lab_TA are less than 1 std below the mean number of students helped per TA 
"""

def main():
    start_time = "2022-02-21T19:00"
    end_time = "2022-02-21T21:00"
    url = "https://www.labqueue.io/api/v1/requests/query/"
    payload = {"created_after": start_time,
               "created_before": end_time,
               }
    result = requests.get(url, auth=wsse_auth, params=payload)
    d: dict = result.json()

    print("Total victims", d['count'])
    print('-----------------')
    analyze(d['results'])


def analyze(d):
    lab_ta_count = {}
    for victim in d:
        lab_ta: str = victim['acceptor_netid']
        if lab_ta != 'N/A':  # not accetped by a TA, ususally closed quickly by user
            lab_ta_count[lab_ta] = lab_ta_count.get(lab_ta, 0) + 1
    for k, v in lab_ta_count.items():
        print(k, v)
    helped = lab_ta_count.values()
    mu = statistics.mean(helped)
    sigma = statistics.stdev(helped, mu)
    print('-----------------')
    print("mu =", mu)
    print("sigma =", sigma)
    for lab_ta in lab_ta_count:
        if lab_ta_count[lab_ta] < mu - sigma:
            print(lab_ta, "is not pulling their weight: %d vs mean of %f" % (lab_ta_count[lab_ta], mu))


if __name__ == '__main__':
    main()
