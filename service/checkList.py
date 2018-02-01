import requests, re, json
from bs4 import BeautifulSoup

class SessionGoogle:
    def __init__(self, url_login, url_auth, login, pwd):
        self.ses = requests.session()
        login_html = self.ses.get(url_login)
        soup_login = BeautifulSoup(login_html.content, "html.parser").find('form').find_all('input')
        my_dict = {}
        for u in soup_login:
            if u.has_attr('value'):
                my_dict[u['name']] = u['value']
        # override the inputs without login and pwd:
        my_dict['Email'] = login
        my_dict['Passwd'] = pwd
        self.ses.post(url_auth, data=my_dict)

    def get(self, URL):
        return self.ses.get(URL).text

def createJenkinsList():
    url_login = "https://accounts.google.com/ServiceLogin"
    url_auth = "https://accounts.google.com/ServiceLoginAuth"
    session = SessionGoogle(url_login, url_auth, "testing@exosite.com", "1234eszxcv")
    jenkinsHTML = session.get("https://build.exosite.com/view/Murano%20Pipeline/#")
    soup = BeautifulSoup(jenkinsHTML, "html.parser")
    nowBuildData = soup.select('table.pipelines')[0].text
    startIndex = [i.start() for i in re.finditer('{"id":', nowBuildData)]
    checkList = {'buildNumber':'', 'Uncheck':[], 'Running':[]}
    exceptBuild = ['murano-staging-openshfit']

    for i in startIndex:
        jsonData = json.loads(nowBuildData[i:nowBuildData.find(';',i)])
        if (jsonData['project']['name'] in exceptBuild):
            continue
        if (jsonData['project']['name'] == 'murano_dispatcher'):
            checkList['buildNumber'] = jsonData['build']['displayName']
            continue
        if (jsonData['project']['disabled'] == True):
            continue
        if (jsonData['build']['status'] == 'UNSTABLE'):
            checkList['Uncheck'] += [jsonData['project']['name']]
        if (jsonData['build']['status'] == 'BUILDING'):
            checkList['Running'] += [jsonData['project']['name']]
        if (jsonData['build']['status'] == 'PENDING'):
            checkList['Running'] += [jsonData['project']['name']]

    print ('')
    print ('Jenkins (%s)' % checkList['buildNumber'])
    print ('# Uncheck')
    print '\n'.join(uncheck for uncheck in checkList['Uncheck'])
    print ('# Checking')
    print ('# No Problem')
    print ('# Problem')
    print ('# Running')
    print '\n'.join(running for running in checkList['Running'])
    print ('')

def getLog():
    url_login = "https://accounts.google.com/ServiceLogin"
    url_auth = "https://accounts.google.com/ServiceLoginAuth"
    session = SessionGoogle(url_login, url_auth, "testing@exosite.com", "1234eszxcv")
    jenkinsHTML = session.get("https://build.exosite.com/view/Murano%20Pipeline/job/murano-staging-business/617/robot/report/log.html")
    soup = BeautifulSoup(jenkinsHTML, "html.parser")
    print (soup)
    nowBuildData = soup.select('span.label.fail')
    print (nowBuildData)

if __name__ == '__main__':
    createJenkinsList()
    #getLog()