"""
This is a module using to authenticate with the RENWEB Frontend
"""
import re
import requests
from typing import Union
from bs4 import BeautifulSoup


class ClassSubject:
    """
    A class for sorting each subject and choosing the subject. Utilized in subjectGradeBook().
    """

    def __init__(self, urlList: list, districtCode: str):
        self.districtCode = districtCode
        self.students = []
        self.classes = [[]]
        self.terms = []

        # Variable in order to know how to split up Nested List
        self.tempTerms = 1

        # Looping over each Url in urlList to split up each variable
        for url in urlList:
            self.link = url.split("?")[1]
            self.studentID, self.classID, self.termID = self.link.split("&")
            self.studentID, self.classID, self.termID = (
                self.studentID.split("=")[1],
                self.classID.split("=")[1],
                self.termID.split("=")[1],
            )

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

        print(self.classes)

    def getGradeUrl(self, student: int, classID: int, termID: int):
        """
        Function for getting the specific grade book's url of a subject
        """
        self.Class = self.classes[termID - 1][classID]
        self.Student = self.students[student]
        self.Term = termID

        self.Class

        # Input variables into renweb's url
        self.url = f"https://{self.districtCode.lower()}.client.renweb.com/pwr/NAScopy/Gradebook/GradeBookProgressReport-PW.cfm?District={self.districtCode}&StudentID={self.Student}&ClassID={self.Class}&TermID={self.Term}&SchoolCode={self.districtCode.split('-')[0]}"

        return self.url

    def getGradeList(self):
        """
        Function which returns the list of classes.
        """
        return self.classes


def Auth(District_Code: str, Username: str, Password: str, c: requests.Session) -> None:
    """
    Base Auth Method which authenticates the user with the Renweb Servers.
    """
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


def Login(District_Code: str, Username: str, Password: str) -> Union[int, tuple, list]:
    """
    The first logon method for authenticating
    """
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
            if (
                urlpath.url
                == f"https://{Client_Code}.client.renweb.com/pwr/student/index.cfm"
            ):

                # Pull in page data and parse it
                page = c.get(
                    f"https://{Client_Code}.client.renweb.com/pwr/school/"
                ).text

                soup = BeautifulSoup(page, "lxml")

                # Find the name of the user in text form
                Name = soup.find("div", {"class": "pwr_user-name"}).text

                # Find table of body that includes school events
                eventsRows = soup.find(id="school_events").find("tbody").find_all("tr")

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


def getSubjectUrls(District_Code: str, Request_Object: requests.Session) -> list:
    """
    Get every subject's url in order to access the gradebook
    """
    # Initiate variable that stores list for every quarter
    foolist = []

    # Get Website Address and access it
    Client_Code = District_Code.lower()
    page = Request_Object.get(
        f"https://{Client_Code}.client.renweb.com/pwr/student/index.cfm"
    ).text

    # Use BeautifulSoup to parse the web page
    page = BeautifulSoup(page, "lxml")

    # Find the tables storing links to gradebook.  page = page.find_all("table")
    for tables in page:
        # Find the table body (<tbody> tag in HTML)
        tableBody = tables.find_all("tbody")
        for tr in tableBody:
            # Find every row in the table body
            for foo in tr.find_all("tr"):
                # Find all link tags (<a>) that links to the specifc *grades.cfm document* that gradebooks are stored
                # Using Regex
                for link in foo.findAll("a", attrs={"href": re.compile("^grades.cfm")}):

                    # For each <a> tag get the href that has the actuall link
                    link = link.get("href")
                    foolist.append(link)
    return foolist


def getSubjectList(District_Code: str, Request_Object: requests.Session) -> list:
    """
    Get the lists of subjects that the students have
    """
    # Initialize Varible for storing subject list
    foolist = []

    # Get school's website address and access it
    page = Request_Object.get(
        f"https://{District_Code.lower()}.client.renweb.com/pwr/student/index.cfm"
    ).text

    # Put the html into a parser
    page = BeautifulSoup(page, "lxml")

    # Find every table in the web page.
    page = page.find_all("table")
    for tables in page:
        # Temporary list that will be used to store grades for one quarter (one table)
        g_list = []

        # Find every table in the tables
        tableBody = tables.find_all("tbody")

        for tr in tableBody:
            # For each table body find all rows
            for foo in tr.find_all("tr"):
                # Find the tabl data in each row
                td = foo.find_all("td")

                # Get the text version of the table data
                row = [i.text for i in td]

                # Strip of newline characters
                row = list(map(lambda s: s.strip("\n"), row))

                # Similar to getSubjectUrls()
                for link in foo.findAll("a", attrs={"href": re.compile("^grades.cfm")}):
                    link = link.get("href")

                    # We only want class ID from the url
                    classID = int(link.split("&")[1].split("=")[1])

                    # Append the class ID to each of the rows
                    row.append(classID)

                    # Append the row (class and grade) to the list
                    g_list.append(row)

        # Sort classes list according to the last element of the list which is the classID
        g_list.sort(key=lambda element: element[-1])

        # Remove the classID after sorting
        for grades in g_list:
            grades.pop()

        # Finally append the sorted list into the final list
        foolist.append(g_list)

    # Return the list
    return foolist


def getAllClassesList(District_Code: str, Username: str, Password: str) -> list:
    """
    Main function that will be utilized to Authenticate and pull data from Renweb Servers
    """
    # Open a request session
    with requests.Session() as c:
        # Authenticate with Renweb server
        Auth(District_Code, Username, Password, c)

        # Get the subject list
        classGradeList = getSubjectList(District_Code, c)

        # Return the subject's list
        return classGradeList


def getSubjectGradeBook(
    District_Code: str,
    Username: str,
    Password: str,
    Student: int,
    Subject: int,
    Term: int,
) -> str:
    """
    Get the html of the specific subject grade book.
    """
    # Open a request session
    with requests.Session() as c:
        # Authenticate with renweb servers
        Auth(District_Code, Username, Password, c)

        # Initialize Urls_list varible to store the url
        Urls_list = getSubjectUrls(District_Code, c)

        # Put the urlList and district code into the ClassSubject class.
        Sub = ClassSubject(Urls_list, District_Code)

        # Get the subject grade book's url from the class using the index
        url = Sub.getGradeUrl(Student, Subject, Term)

        # Access the url and store it in a variable
        page = c.get(url).text

        # Return the raw html
        return page
