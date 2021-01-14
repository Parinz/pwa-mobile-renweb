'''
This is a module using to authenticate with the RENWEB Frontend
'''

from multiprocessing import Process, Manager
import re
import requests
from bs4 import BeautifulSoup


class ClassSubject:
    def __init__(self, urlList, districtCode):
        self.districtCode = districtCode
        self.students = set()
        self.classes = set()
        self.terms = set()

        for url in urlList:
            self.link = url.split('?')[1]
            self.studentID, self.classID, self.termID = self.link.split('&')
            self.studentID, self.classID, self.termID = self.studentID.split(
                '=')[1], self.classID.split('=')[1], self.termID.split('=')[1]

            self.students.add(self.studentID)
            self.classes.add(self.classID)
            self.terms.add(self.termID)

        self.students = list(self.students)
        self.classes = list(self.classes)

    def getGradeUrl(self, student: int, classID: int, termID: int):
        self.Class = self.classes[classID]
        self.Student = self.students[student]
        self.Term = termID

        self.url = f"https://{self.districtCode.lower()}.client.renweb.com/pwr/NAScopy/Gradebook/GradeBookProgressReport-PW.cfm?District={self.districtCode}&StudentID={self.Student}&ClassID={self.Class}&TermID={self.Term}&SchoolCode={self.districtCode.split('-')[0]}"

        return self.url

    def getGradeList(self):
        return self.classes


def Login(District_Code, Username, Password):
    '''
    The first logon method for authenticating
    '''
    try:
        with requests.Session() as c:
            District_Code = District_Code.upper()
            Client_Code = District_Code.lower()
            UserType = "PARENTSWEB-PARENT"
            Submit = "Login"
            formMethod = "login"
            url = f"https://{Client_Code}.client.renweb.com/pwr/"
            c.get(url)
            login_data = {
                "DistrictCode": District_Code,
                "UserName": Username,
                "Password": Password,
                "UserType": UserType,
                "Submit": Submit,
                "formMethod": formMethod,
            }
            c.post(url, data=login_data)
            urlpath = c.get(
                f"https://{Client_Code}.client.renweb.com/pwr/student/index.cfm"
            )

            if (urlpath.url == f"https://{Client_Code}.client.renweb.com/pwr/student/index.cfm"):

                page = c.get(
                    f"https://{Client_Code}.client.renweb.com/pwr/student/index.cfm").text

                soup = BeautifulSoup(page, 'lxml')

                Name = soup.find("div", {"class": "pwr_user-name"})

                return Name.text

            else:
                return -1
    except:
        return -2


def Auth(District_Code, Username, Password, c):
    '''
    Base Auth Method
    '''
    District_Code = District_Code.upper()
    Client_Code = District_Code.lower()
    UserType = "PARENTSWEB-PARENT"
    Submit = "Login"
    formMethod = "login"
    url = f"https://{Client_Code}.client.renweb.com/pwr/"
    c.get(url)
    login_data = {
        "DistrictCode": District_Code,
        "UserName": Username,
        "Password": Password,
        "UserType": UserType,
        "Submit": Submit,
        "formMethod": formMethod,
    }
    c.post(url, data=login_data)


def GetData(Client_Code, Request_Object, foolist):
    page = Request_Object.get(
        f"https://{Client_Code}.client.renweb.com/pwr/student/index.cfm"
    ).text
    page = BeautifulSoup(page, 'lxml')
    page = page.find_all("table")
    for tables in page:
        g_list = []
        tableBody = tables.find_all("tbody")
        for tr in tableBody:
            for foo in tr.find_all("tr"):
                td = foo.find_all("td")
                row = [i.text for i in td]
                row = list(map(lambda s: s.strip("\n"), row))
                g_list.append(row)
        foolist.append(g_list)


def gradeBook(District_Code, Request_Object, foolist):
    Client_Code = District_Code.lower()
    page = Request_Object.get(
        f"https://{Client_Code}.client.renweb.com/pwr/student/index.cfm").text
    page = BeautifulSoup(page, 'lxml')
    page = page.find_all("table")
    for tables in page:
        tableBody = tables.find_all("tbody")
        for tr in tableBody:
            for foo in tr.find_all("tr"):
                for link in foo.findAll('a', attrs={'href': re.compile("^grades.cfm")}):
                    link = link.get('href')
                    full_link = f"https://{Client_Code}.client.renweb.com/pwr/student/" + link
                    foolist.append(full_link)
    return foolist


def subjectGradeBook(District_Code, Username, Password, Student_ID, Class_ID, Term_ID):
    with requests.Session() as c:
        Auth(District_Code, Username, Password, c)
        url = f"https://{District_Code.lower()}.client.renweb.com/pwr/NAScopy/Gradebook/GradeBookProgressReport-PW.cfm?District={District_Code}&StudentID={Student_ID}&ClassID={Class_ID}&TermID={Term_ID}&SchoolCode={District_Code.split('-')[0]}"
        page = c.get(url).text

        return page


def globalGetData(District_Code, Username, Password):
    with Manager() as manager:
        with requests.Session() as c:
            Auth(District_Code, Username, Password, c)

            Grade_list = manager.list()
            Urls_list = manager.list()

            getData_process = Process(
                target=GetData, args=(District_Code.lower(), c, Grade_list))
            getData_process.start()

            gradeBook_process = Process(
                target=gradeBook, args=(District_Code, c, Urls_list))
            gradeBook_process.start()

            getData_process.join()
            gradeBook_process.join()
            return list(Grade_list), list(Urls_list)


def globalGetGradeBook(District_Code, Username, Password, Student: int, Subject: int, Term: int):
    with Manager() as manager:
        with requests.Session() as c:
            Auth(District_Code, Username, Password, c)

            Urls_list = manager.list()

            gradeBook_process = Process(
                target=gradeBook, args=(District_Code, c, Urls_list))
            gradeBook_process.start()

            gradeBook_process.join()
            Urls_list = list(Urls_list)

            Sub = ClassSubject(Urls_list, District_Code)
            url = Sub.getGradeUrl(Student, Subject, Term)

            page = c.get(url).text

            print(url)
            return page
