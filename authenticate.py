def Login():
        District_Code = self.district_code.text
        Username = self.username.text
        Password = self.password.text

        try:
            with requests.Session() as c:
                District_Code = District_Code.upper()
                Client_Code = District_Code.lower()
                UserType = "PARENTSWEB-PARENT"
                Submit = "Login"
                formMethod = "login"
                url = f"https://{Client_Code}.client.renweb.com/pwr/"
                c.get(url)
                self.progress.value = 40
                login_data = {
                    "DistrictCode": District_Code,
                    "UserName": Username,
                    "Password": Password,
                    "UserType": UserType,
                    "Submit": Submit,
                    "formMethod": formMethod,
                }
                self.progress.value = 80
                c.post(url, data=login_data)
                urlpath = c.get(
                    f"https://{Client_Code}.client.renweb.com/pwr/student/index.cfm"
                )
                if (
                    urlpath.url
                    == f"https://{Client_Code}.client.renweb.com/pwr/student/index.cfm"
                ):
                    self.progress.value = 100
                    M_App.screen_manager.current = "HomeScreen"

                else:
                    self.progress.value = 0
                    self.dialog.open()

        except:
            self.dialog.open()

        if District_Code != "" and Username != "" and Password != "":
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
            except:
                self.dialog.open()