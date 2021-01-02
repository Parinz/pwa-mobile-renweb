import requests
from multiprocessing import Process, Manager
from bs4 import BeautifulSoup
import re

def Login(District_Code, Username, Password):
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

                page = c.get(f"https://{Client_Code}.client.renweb.com/pwr/student/index.cfm").text

                soup = BeautifulSoup(page, 'lxml')

                Name = soup.find("div", {"class": "pwr_user-name"}) 

                return Name.text

            else:
                return -1
    except:
        return -2

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
        page = Request_Object.get(f"https://{Client_Code}.client.renweb.com/pwr/student/index.cfm").text
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

        url = f"https://{Client_Code}.client.renweb.com/pwr/NAScopy/Gradebook/GradeBookProgressReport-PW.cfm?District={District_Code}&StudentID={Student_ID}&ClassID={Class_ID}&TermID={Term_ID}&SchoolCode={District_Code.split('-')[0]}"
        
        page = c.get(url).text
        
        return page

def globalGetData(District_Code, Username, Password):
    with Manager() as manager:
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

            Grade_list = manager.list()
            Urls_list = manager.list()
            
            getData_process = Process(target=GetData, args=(Client_Code, c, Grade_list))
            getData_process.start()
            
            gradeBook_process = Process(target=gradeBook, args=(District_Code, c, Urls_list))
            gradeBook_process.start()

            getData_process.join()
            gradeBook_process.join()
            return list(Grade_list), list(Urls_list)  

def globalGetGradeBook(District_Code, Username, Password, Subject: int):
    with Manager() as manager:
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
            
            Urls_list = manager.list()
            
            gradeBook_process = Process(target=gradeBook, args=(District_Code, c, Urls_list))
            gradeBook_process.start()
            

            gradeBook_process.join()
            Urls_list = list(Urls_list)

            Url = Urls_list[Subject]
            
            link = Url.split('?')[1]
            Student_ID, Class_ID, Term_ID = link.split('&')
            Student_ID, Class_ID, Term_ID = Student_ID.split('=')[1], Class_ID.split('=')[1], Term_ID.split('=')[1]
 
            url = f"https://{Client_Code}.client.renweb.com/pwr/NAScopy/Gradebook/GradeBookProgressReport-PW.cfm?District={District_Code}&StudentID={Student_ID}&ClassID={Class_ID}&TermID={Term_ID}&SchoolCode={District_Code.split('-')[0]}"

            page = c.get(url).text
            
            print(url)
            return page
