import requests

r = requests.get('https://jobs.rbc.com/ca/en/businessunit/technology-operations-jobs')

with open("txt.txt", 'w') as f:
    f.write(r.text)
