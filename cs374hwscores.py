import requests
import bs4
import sys
import getpass
import numpy as np

loginPage = "https://gradescope.com/login"
coursePage = "https://gradescope.com/courses/5822"
toRemove = 9
data =[]
scores =[]
# for i in range(33):
#     scores.append(i)
payload={}

with requests.Session() as s:
    while True:
        usr = input("Email: ")
        pswrd = getpass.getpass()
        response = s.get(loginPage)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        data = soup.select('form input')
        payload = {data[0]["name"]:data[0]["value"], data[1]["name"]:data[1]["value"], data[2]["name"]:usr, data[3]["name"]:pswrd, data[4]["name"]:data[4]["value"], data[5]["name"]:data[5]["value"]}
        response = s.post(loginPage,payload)
        if response.status_code!=200:
            print("Wrong email or password. Try again..")
        else:
            break

    response = s.get(coursePage)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    data = soup.select('span.submissionStatus--score')
for d in data:
    s = float(d.decode_contents(formatter="html").split("/")[0].strip())
    if s>10:
        s/=2
    scores.append(s)
allscores = scores
top24scores = allscores.copy()
scoresAfterDrop = allscores.copy()
n = ['N/a']
s = top24scores
for i in range(toRemove):
    m = min(s)
    if len(s)==25:
        n.append(m)
    if i==8:
        n.append(m)
    s.remove(m)
    if (len(s))==24:
        scoresAfterDrop = top24scores.copy()
        s  = scoresAfterDrop
strings = ["All Availabe Scores", "Top 24 Scores", "Scores After dropping lowest 9"]
s = [allscores,top24scores,scoresAfterDrop]
for i in range(len(strings)):
    scores = s[i]
    print("==="+strings[i]+"===")
    print("Number of graded: "+str(len(scores)))
    print("Scores : "+str(scores))
    print("Worst score: "+str(min(scores)))
    print("Highest dropped score: "+str(n[i]))
    print("Avgerage: "+str(np.mean(scores)))
    print("")
