from flask.templating import render_template_string
import requests
from bs4 import BeautifulSoup
from flask import url_for

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
                return [District_Code, Username, Password]

            else:
                return -1
    except:
        return -2

def GetData():
  if District_Code != "" and Username != "" and Password != "":
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
            page = c.get(
                f"https://{Client_Code}.client.renweb.com/pwr/student/index.cfm"
            ).text
            page = BeautifulSoup(page)
            page = page.find("table")

            tablerows = page.find_all("tr")
            for tr in tablerows:
                td = tr.find_all("td")
                row = [i.text for i in td]
                row = tuple(list(map(lambda s: s.strip("\n"), row)))
                g_list.append(row)
                print(row)