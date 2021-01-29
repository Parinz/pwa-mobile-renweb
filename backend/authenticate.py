'''
This is a module using to authenticate with the RENWEB Frontend
'''

from multiprocessing import Process, Manager
import re
import requests
from bs4 import BeautifulSoup


class ClassSubject:
    '''
    A class for sorting each subject and choosing the subject. Utilized in subjectGradeBook().
    '''
    def __init__(self, urlList: list, districtCode: str):
        self.districtCode = districtCode
        self.students = []
        self.classes = [[]]
        self.terms = []

        # Variable in order to know how to split up Nested List
        self.tempTerms = 1

        # Looping over each Url in urlList to split up each variable
        for url in urlList:
            self.link = url.split('?')[1]
            self.studentID, self.classID, self.termID = self.link.split('&')
            self.studentID, self.classID, self.termID = self.studentID.split(
                '=')[1], self.classID.split('=')[1], self.termID.split('=')[1]

            self.termID = int(self.termID)

            if self.studentID in self.students:
                pass
            else:
                self.students.append(self.studentID)

            # Checks to see if the incoming classes list for the QUARTER was already existing
            if self.termID == self.tempTerms:
                # If the quarter exists, append class id to the correct nested list
                self.classes[self.termID - 1].append(self.classID)
            else:
                # If the quarter does not exist, set tempTerms to the new termID. Then append an empty nested list and append classID to that.
                self.tempTerms = self.termID
                self.classes.append([])
                self.classes[self.termID - 1].append(self.classID)


    def getGradeUrl(self, student: int, classID: int, termID: int):
        '''
        Function for getting the specific grade book's url of a subject
        '''
        self.Class = self.classes[termID - 1][classID]
        self.Student = self.students[student]
        self.Term = termID

        # Input variables into renweb's url
        self.url = f"https://{self.districtCode.lower()}.client.renweb.com/pwr/NAScopy/Gradebook/GradeBookProgressReport-PW.cfm?District={self.districtCode}&StudentID={self.Student}&ClassID={self.Class}&TermID={self.Term}&SchoolCode={self.districtCode.split('-')[0]}"

        return self.url

    def getGradeList(self):
        '''
        Function which returns the list of classes.
        '''
        return self.classes

def Auth(District_Code: str, Username: str, Password: str, c):
    '''
    Base Auth Method which authenticates the user with the Renweb Servers.
    '''
    District_Code = District_Code.upper()
    Client_Code = District_Code.lower()
    UserType = "PARENTSWEB-PARENT"
    Submit = "Login"
    formMethod = "login"
    url = f"https://{Client_Code}.client.renweb.com/pwr/"
    # Use the request object(c) to get the login form of specific school.
    c.get(url)

    # Data that will be sent to authenticate.
    login_data = {
        "DistrictCode": District_Code,
        "UserName": Username,
        "Password": Password,
        "UserType": UserType,
        "Submit": Submit,
        "formMethod": formMethod,
    }

    # Post the login data to attempt to authenticate
    c.post(url, data=login_data)


def Login(District_Code: str, Username: str, Password: str):
    '''
    The first logon method for authenticating
    '''
    Client_Code = District_Code.lower()
    try:
        # Opens request session
        with requests.Session() as c:

            # Authenticate with Renweb Server
            Auth(District_Code, Username, Password, c)

            # Tries to get a url which will be accessible to AUTHENTICATED users only
            urlpath = c.get(
                f"https://{Client_Code}.client.renweb.com/pwr/student/index.cfm"
            )

            # If not redirected, means you are authenticated
            if (urlpath.url == f"https://{Client_Code}.client.renweb.com/pwr/student/index.cfm"):

                # Pull in page data and parse it
                page = c.get(
                    f"https://{Client_Code}.client.renweb.com/pwr/school/").text

                soup = BeautifulSoup(page, 'lxml')

                # Find the name of the user in text form
                Name = soup.find("div", {"class": "pwr_user-name"}).text

                # Find table of body that includes school events
                eventsRows = soup.find(id='school_events').find("tbody").find_all("tr")

                # Variable for storing events
                eventList = []

                for rows in eventsRows:
                    # For each row, find all the data in each table (td)
                    tds = rows.find_all("td")

                    # Get dates and events in text form
                    date = [i.text for i in tds]

                    # Strip out tabs, newlines, and tabs again (To make it clean)
                    date = list(map(lambda s: s.strip("\t"), date))
                    date = list(map(lambda s: s.strip("\n"), date))
                    date = list(map(lambda s: s.strip("\t"), date))

                    # Date variable will be a list of dates and events ["12/12/2021", "Future"]
                    # Change that into a dictionary and apppend into variable for storing events
                    event = {date[0]: date[1]}
                    eventList.append(event)

                # Return back the real name and eventList
                return Name, eventList

            else:
                # Returns -1 if credentials are incorrect
                return -1
    except:
        # Returns negative 2 if there a Network Error or wrong District Code
        return -2


def GetData(Client_Code, Request_Object, foolist):
    '''
    Get the lists of subjects that the students have
    '''
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

            getData_process = Process(
                target=GetData, args=(District_Code.lower(), c, Grade_list))
            getData_process.start()


            getData_process.join()
            return list(Grade_list)


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
