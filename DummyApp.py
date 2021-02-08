import tkinter as tk
from tkinter import messagebox
from tkinter import IntVar
from pymongo import MongoClient
import re
import datetime
from bson.objectid import ObjectId

# connecting to our database
app_cluster = MongoClient("")
app_db = app_cluster["mainappdb"]
user_data_collection = app_db["UserData"]

"""
// Sum Notes
"DummySocialMediaApp - Login"
"DummySocialMediaApp - Sign Up"
"DummySocialMediaApp - HomePage"
"DummySocialMediaApp - SearchedUserPage"
"""

# ======================== Declaring Some Global Variables That I Will Need ========================
largefont = 150
# the props for giving the user data to the homepage
usedinloginusername = ""
usedinloginpassword = ""
# the searched usersname for accesing it from db
g_searchedusername = ""
# ==================================================================================================

# Multi Page Function
class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (LoginPage, SignUpPage, HomePage, SearchedUserPage, ChatPage, SettingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoginPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#====================================================================================
#====================================================================================
'''  IMPORTANT   '''
'''  global userdata variable for accesing later  '''
'''  THIS WILL BE USED ALL THROUGHOUT THE APP SO ITS REALLY IMPORTANT  '''

# LoginPage / first page
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        controller.geometry("450x600")
        controller.resizable(False, False)
        controller.title("DummySocialMediaApp")

        """ -- LoginPage Code -- """

        # Login Function
        def loginf(usernamepar, passwordpar):
            # checking if the usernamepar and passwordpar are eligible of being sent to the database
            if(len(usernamepar) < 8 or len(passwordpar) < 8):
                tk.messagebox.showerror("Error", "Username and Password Have to be at Least 8 Characters Long")
            else:
                # checking for the data on the database
                userdata = user_data_collection.find_one({"username": str(usernamepar), "password": str(passwordpar)})
                if userdata == None:
                    tk.messagebox.showerror("Error",
                                           "Account Not Found\nMake Sure You Entered The\nUsername and Password Correctly")
                else:
                    usernameentry.delete(0, "end")
                    passwordentry.delete(0, "end")
                    controller.show_frame(HomePage)
                    global usedinloginusername
                    global usedinloginpassword
                    global allowedtogotohp
                    usedinloginusername = str(usernamepar)
                    usedinloginpassword = str(passwordpar)
                    allowedtogotohp = True

        def gotosigninpagef():
            controller.show_frame(SignUpPage)

        ''' Messing With The Views '''
        def viewpasswordf():
            passwordentry.config(show="")
            viewpassbtn.config(command=lambda : dontviewpasswordf(), text="Hide Password")

        def dontviewpasswordf():
            passwordentry.config(show="*")
            viewpassbtn.config(command=lambda: viewpasswordf(), text="View Password")

        """ -- LoginPage Design"""
        # The Header Text
        tk.Label(self, text="DummySocialMediaApp", font=largefont, bg="lightgray").place(x=150, y=25)

        # Login Box
        loginboxframe = tk.Frame(self, padx=80, pady=150, bg="gray")
        tk.Label(self, text="Login Below", font=largefont, bg="lightgray").place(x=170, y=150)

        tk.Label(loginboxframe, text="__________________", font=largefont, bg="gray").pack()
        loginboxframe.place(x=65, y=100)

        # the entries for the personal data
        # username
        tk.Label(self, text="Username Below :  ", bg="gray", font=largefont).place(x=150, y=200)
        usernameentry = tk.Entry(self, width=25)
        usernameentry.place(x=150, y=240)
        # email
        tk.Label(self, text="Password Below :  ", bg="gray", font=largefont).place(x=150, y=280)
        passwordentry = tk.Entry(self, width=25, show="*")
        passwordentry.place(x=150, y=320)
        # view password button
        viewpassbtn = tk.Button(self, text="View Password", width=10, height=1, command=lambda : viewpasswordf())
        viewpassbtn.place(x=310, y=317)

        # Login Button
        loginbutton = tk.Button(self, text="Login", bg="white", width=10, height=3, command=lambda: loginf(usernameentry.get(), passwordentry.get()))
        loginbutton.place(x=190, y=360)

        """ ======= extra info part ======= """
        extrastuffframe = tk.Frame(self, padx=186, pady=50, borderwidth=1, bg="gray", highlightbackground="black", highlightthickness=4)
        tk.Label(extrastuffframe, text="_______", font=largefont, bg="gray", fg="gray")\
            .pack()
        extrastuffframe.place(x=0, y=480)
        # extra info part design below
        tk.Label(self, text="Dont have an account? SignUp with this button --> ", font=largefont, bg="lightgray").place(x=10, y=490)
        gotosignuppagebutton = tk.Button(self, text="Signup", font=largefont, width=8, height=1, fg="darkblue", command=lambda: gotosigninpagef())
        gotosignuppagebutton.place(x=364, y=487)

#====================================================================================
#====================================================================================
# signup page in case user doesnt have account
class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        controller.geometry("450x600")
        controller.resizable(False, False)
        controller.title("DummySocialMediaApp")

        """ -- SignUpPage Page Code -- """

        # code for reading the license agreement
        def readthelicenseagreementf():
            license_agreement_win = tk.Tk()
            license_agreement_win.geometry("300x300")
            license_agreement_win.title("DummySocialMediaApp License Agreement")
            license_agreement_win.resizable(False, False)
            licenseagreementtext = "USING THIS APP FOR PROFIT\n/ADVERTISMENT/SELLING\n IT WITHOUT PERMISION\n IN ANY CASE \nWILL BE AGAINST THE\n RULES AND THE \nPROPER ACTION\n WILL BE TAKEN.\n" \
                                   "REUSING THIS APP \nAND CLAIMING THIS \nAPP WILL ALSO GET \nYOU IN TROUBLE, \nTHE CREATOR OF THIS\n APP IS \"ADAK CELINA\" AND\n ANY CLAIMS OTHERWISE \nWILL GET YOU IN TROUBLE "
            tk.Label(license_agreement_win, text=licenseagreementtext, bg="gray", fg="aqua", font=largefont).place(x=35, y=5)
            license_agreement_win.mainloop()
        # ======================================

        # The actual signup function below
        def signupf():
            # getting the data from the inputs
            email_gotten_su = signup_emailentry.get()
            username_gotten_su = signup_usernameentry.get()
            birthyear_gotten_su = signup_birthyearentry.get()
            password_gotten_su = signup_passwordentry.get()
            passwordconfirmation_gotten_su = signup_passwordconfirmationentry.get()

            # checking if the user accepted the license agreement
            if licenseagreementaccepted.get() == 0:
                tk.messagebox.showerror("Error", "You Need To Accept The License Agreement To Use This App")
            else:
                # checking if the data is valid for signup trial
                regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                # checking email as the first step
                if re.search(regex, email_gotten_su):
                    # checking the username as the second step
                    if(len(username_gotten_su) > 7):
                        # checking if the birthyear is 4digits / proper as the third step
                        if(len(str(birthyear_gotten_su)) == 4):
                            # checking if the given birth year is a proper number as the third and a halfth step
                            #   ===========================================
                            #   ||                 INFO                  ||
                            #   ||  The Birthday Check Needs Some Fixes  ||
                            #   ||          It isn't that stable         ||
                            #   ===========================================
                            try:
                                birthyear_gotten_su = int(birthyear_gotten_su)
                                docontinueafternumcheck = True
                            except:
                                tk.messagebox.showerror("Error", "Please Enter a Valid Birth Year (enter numbers)")
                                docontinueafternumcheck = False
                            if docontinueafternumcheck == True:
                                # =================================
                                # =================================
                                # checking if the given password is proper as the fourth step
                                if (len(password_gotten_su) > 7):
                                    # checking if the password confirmation matches the password as
                                    # the fifth and the last step of signup trial
                                    if str(passwordconfirmation_gotten_su) == str(password_gotten_su):
                                        # ==================================================================
                                        # ||    at this point the signup trial is over, we need to        ||
                                        # ||    check if the data is valid for the database upload now    ||
                                        # ||    (example : is there existing data etc)                    ||
                                        # ==================================================================
                                        """ Checking If The Username and Email are already used on the database"""
                                        databaseemailcheckresult = user_data_collection.find_one(
                                            {"email": str(email_gotten_su)})
                                        if databaseemailcheckresult == None:
                                            databaseusernamecheckresult = user_data_collection.find_one(
                                                {"username": str(username_gotten_su)})
                                            if databaseusernamecheckresult == None:
                                                # the account is eligible for being created
                                                # ==============================================
                                                """ THE ACTUAL APP CODE STARTS HERE """
                                                theusertoinsert = {
                                                    "email": email_gotten_su,
                                                    "username": username_gotten_su,
                                                    "birthyear": birthyear_gotten_su,
                                                    "password": password_gotten_su,
                                                    "friendsamount": 0,
                                                    "friends": "",
                                                    "userbio": "",
                                                    "createdon": datetime.datetime.now()
                                                }
                                                # the account put to the database
                                                user_data_collection.insert_one(theusertoinsert)
                                                # creating the user $set for $addtoset later
                                                user_data_collection.update_one({"username": str(username_gotten_su)}, {
                                                    "$set": {"friends": [
                                                        {
                                                            "friend_id": "firstfriendtestid",
                                                            "friend_username": "firstfriendtestusn",
                                                        }
                                                    ]}})
                                                # telling the user the acccount has been created succesfully
                                                tk.messagebox.showinfo("Sucess",
                                                                       "Your Account Has Been Created Succesfully")

                                                # clearing the entries
                                                signup_emailentry.delete(0, 'end')
                                                signup_usernameentry.delete(0, 'end')
                                                signup_birthyearentry.delete(0, 'end')
                                                signup_passwordentry.delete(0, 'end')
                                                signup_passwordconfirmationentry.delete(0, 'end')

                                            else:
                                                tk.messagebox.showerror("Error",
                                                                        "Account Can't be Created as the Username is Already in Use in Another Account")
                                        else:
                                            tk.messagebox.showerror("Error",
                                                                    "Account Can't be Created as the Email is Already in Use in Another Account")
                                    else:
                                        tk.messagebox.showerror("Error",
                                                                "Password Confirmation Doesnt Match The Password")
                                else:
                                    tk.messagebox.showerror("Error",
                                                            "The Password Has To be at Least 8 characters long")
                            else:
                                pass
                        else:
                            tk.messagebox.showerror("Error", "Please Enter a Valid Birth Year")
                    else:
                        tk.messagebox.showerror("Error", "The Username Has to Be at Least 8 Characters Long")
                else:
                    tk.messagebox.showerror("Error", "Invalid Email")

        """ -- SignUpPage Page Design"""
        # The Frame for the box of the page
        signuppageframe = tk.Frame(self, padx=192, pady=200, highlightbackground="black", highlightthickness=4, bg="gray")
        tk.Label(signuppageframe, text="---", bg="gray", fg="gray")\
            .pack()
        signuppageframe.place(x=20, y=50)
        tk.Label(self, text="Enter Personal Information Below", font=largefont, borderwidth=5, width=30, height=2, bg="black", fg="white")\
            .pack()
        # Personal Information Entry Locations
        tk.Label(self, text="Email ---->", font=largefont, bg="lightgray", width=17).place(x=50 ,y=100)
        tk.Label(self, text="Username ---->", font=largefont, bg="lightgray", width=17).place(x=50 ,y=150 )
        tk.Label(self, text="Birth Year ---->", font=largefont, bg="lightgray", width=17).place(x=50 ,y=200 )
        tk.Label(self, text="Password ---->", font=largefont, bg="lightgray", width=17).place(x=50 ,y=250 )
        tk.Label(self, text="Confirm Password ---->", font=largefont, bg="lightgray", width=17).place(x=50 ,y=300 )

        #email entry
        signup_emailentry = tk.Entry(self, font=largefont, bg="white", width=21)
        signup_emailentry.place(x=220 ,y=101)

        # username entry
        signup_usernameentry = tk.Entry(self, font=largefont, bg="white", width=21)
        signup_usernameentry.place(x=220 ,y=151)

        # birthyear entry
        signup_birthyearentry = tk.Entry(self, font=largefont, bg="white", width=21)
        signup_birthyearentry.place(x=220 ,y=201)

        # password entry
        signup_passwordentry  = tk.Entry(self, font=largefont, bg="white", show="*", width=21)
        signup_passwordentry.place(x=220 ,y=251)

        # password confirmation entry
        signup_passwordconfirmationentry = tk.Entry(self, font=largefont, bg="white", show="*", width=21)
        signup_passwordconfirmationentry.place(x=220 ,y=301)

        """ terms of service place"""
        tk.Label(self, text="Do You Agree To The Terms Of Service?", font=largefont, bg="lightgray",highlightbackground="black", highlightthickness=4, width=40).place(x=45, y=400)
        licenseagreementaccepted = IntVar()
        agreetotoscb = tk.Checkbutton(self, width=1, height=1, variable=licenseagreementaccepted, bg="lightgray")
        tk.Label(self, text="I Agree To The Terms Of Service").place(x=40, y=440)
        agreetotoscb.place(x=220, y=438)
        #readd license agreement button
        readlicenseagreementbutton = tk.Button(self, text="Read The License Agreement", fg="blue", command=lambda: readthelicenseagreementf())
        readlicenseagreementbutton.place(x=260, y=438)

        # Sign Up Button
        signupbutton = tk.Button(self, text="SIGNUP", bg="gray", fg="aqua", font=largefont, width=12, height=3, command=lambda: signupf())
        signupbutton.place(x=165, y=490)

        # Go To HomePage From Signup Button
        gotohomepgefromsignupbtn = tk.Button(self, text="Go to Login Page", bg="gray", fg="aqua", font=largefont, width=14, height=2, command=lambda: controller.show_frame(LoginPage))
        gotohomepgefromsignupbtn.place(x=312, y=548)

#====================================================================================
#====================================================================================
# Main page with users own data

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        controller.geometry("450x600")
        controller.resizable(False, False)
        controller.title("DummySocialMediaApp")
        self.config(bg="gray")
        # getting the user data global

        """ HomePage -- Page Code -- Pre Refresh"""
        """====SEARCHING FOR USERS===="""

        def searchusersf():
            global usedinloginusername
            # getting the searched data from the username search entry
            searchedusername_nong = searcheduserentry.get()
            # checking if the username exists
            searchedusernamedata = user_data_collection.find_one({"username": str(searchedusername_nong)})
            if searchedusernamedata == None:
                tk.messagebox.showerror("ERROR", "USERNAME DOESNT EXIST")
                # checking if the user searched their own name lol
            elif searchedusername_nong == usedinloginusername:
                tk.messagebox.showerror("ERROR", "YOU CANT SEARCH YOUR OWN NAME :P")
            else:
                # the username exists so assigning it to the global variable to be used in the SearchedUserPage for data
                global g_searchedusername
                g_searchedusername = str(searchedusername_nong)
                # clearing the entry
                searcheduserentry.delete(0, 'end')
                # sending the user to the searched user page
                controller.show_frame(SearchedUserPage)

        # checking for the data on the database // more info on "Line 366"
        def refreshhpf():
            """ The Actual HomePage Code -- Post Refresh"""
            now = datetime.datetime.now()
            global usedinloginusername
            global usedinloginpassword
            # getting the current user data
            curuserdata = user_data_collection.find_one({"username": str(usedinloginusername), "password": str(usedinloginpassword)})
            # getting the current users info
            curuseruserid = curuserdata["_id"]
            curuseremail = curuserdata["email"]
            curuserusername = curuserdata["username"]
            curuserbirthyear = curuserdata["birthyear"]
            curuserpasword = curuserdata["password"]
            curuserfriendsamount = curuserdata["friendsamount"]
            curuserfriends = curuserdata["friends"]
            curuserbio = curuserdata["userbio"]

            # below is the code of entire data being printed for troubleshooting in case i get some data errors later
            '''print(str(curuseruserid) +"\n\n"+ str(curuseremail) +"\n\n"+ str(curuserusername) +"\n\n"+
                  str(curuserbirthyear) +"\n\n"+ str(curuserpasword) +"\n\n"+ str(curuserfriendsamount)
                  + "\n\n" + str(curuserfriends) +"\n\n"+ str(curuserbio)
                  )'''

            # calculating their current age
            curuserage = (int(now.year) - int(curuserbirthyear))

            # function for going to the messages page
            def gotomessages():
                print("MESSAGES")

            # function for going to the settings page
            def gotosettings():
                controller.show_frame(SettingsPage)

            def editbio():
                writebiowindow = tk.Tk()
                writebiowindow.title("Write Bio")
                writebiowindow.geometry("300x300")
                writebiowindow.resizable(False, False)
                writebiowindow.config(bg="gray")
                # ============================
                '''  EDIT BIO WINDOW CODE  '''
                def cancelbioedit():
                    writebiowindow.destroy()
                def savebio():
                    # getting the data from the edit bio box
                    thetexttoinserttobio = biotext.get("1.0", "end")
                    # checking if the string is < || == 250 :P
                    if len(thetexttoinserttobio) <= 250:
                        # updating the database
                        user_data_collection.update_one({"_id": ObjectId(str(curuseruserid))},
                                                        {"$set": {"userbio": str(thetexttoinserttobio)}})
                        # refreshing the page to see the changes
                        refreshhpf()
                        writebiowindow.destroy()
                    else:
                        tk.messagebox.showerror("ERROR", "THE BIO SHOULD BE LESS THAN 250 CHARACTERS LONG \nWHILE "
                                                         "YOUR BIO IS " + str(len(thetexttoinserttobio))) + "CHARACTERS LONG"

                # ============================
                '''  EDIT BIO WINDOW DESIGN  '''
                tk.Label(writebiowindow, text="Edit Your Bio Below\n Max length = 250", bg="lightgray", font=largefont)\
                    .place(x=75, y=5)
                # THE BIO TEXT ENTRY BELOW
                biotext = tk.Text(writebiowindow, width=35, heigh=12)
                biotext.place(x=8, y=50)
                biotext.insert(1.0, str(curuserbio))
                # SAVE BIO BUTTON
                tk.Button(writebiowindow, text="SAVE CHANGES", bg="lightgray", width=12, height=2, command=lambda: savebio())\
                    .place(x=40, y=250)
                # CANCEL BIO EDIT BUTTON
                tk.Button(writebiowindow, text="CANCEL", bg="lightgray", width=12, height=2, command=lambda: cancelbioedit()) \
                    .place(x=150, y=250)


                writebiowindow.mainloop()

            '''   ==========================================   '''
            '''   ==========================================   '''
            """ The Actual HomePage Design -- Post Refresh"""
            # clearing the app first
            userdataframe = tk.Frame(self, padx=183, pady=200, highlightbackground="black", highlightthickness=4, bg="gray")
            tk.Label(userdataframe, text="-------", bg="gray", fg="gray") \
                .pack()
            userdataframe.place(x=18, y=130)
            # starting with the fresh design now
            userpersonaldataframe = tk.Frame(self, padx=167, pady=60, highlightbackground="black", highlightthickness=2, bg="lightgray")
            tk.Label(userpersonaldataframe, text="---------", bg="lightgray", fg="lightgray")\
                .pack()
            userpersonaldataframe.place(x=30, y=142)

            # the user data design below
            # username label
            usernamelabel = tk.Label(self, text="Username -- " + curuserusername, bg="lightgray", font=largefont)
            usernamelabel.place(x=35, y=150)
            # user age label
            useragelabel = tk.Label(self, text="Age -- " + str(curuserage), bg="lightgray", font=largefont)
            useragelabel.place(x=35, y=175)
            # user friends label
            userfriendslabel = tk.Label(self, text="Friends -- " + str(curuserfriendsamount), bg="lightgray", font=largefont)
            userfriendslabel.place(x=35, y=200)

            # go to messages button
            gotomessagesbutton = tk.Button(self, text="Messages", bg="white", fg="blue",
                                           font=largefont, width=10, height=2, command=lambda: gotomessages())
            gotomessagesbutton.place(x=65, y=230)

            # go to settings button
            gotosettingsbutton = tk.Button(self, text="Settings", bg="white", fg="blue",
                                           font=largefont, width=10, height=2, command=lambda: gotosettings())
            gotosettingsbutton.place(x=175, y=230)

            # write a bio post button
            editbiobutton = tk.Button(self, text="Edit Bio", bg="white", fg="blue",
                                       font=largefont, width=10, height=2, command=lambda: editbio())
            editbiobutton.place(x=285, y=230)

            # Bio Location
            thebiotext = tk.Text(self, width=35, height=7, font=("helvetica", 15))
            thebiotext.insert(1.0, str(curuserbio))
            thebiotext.config(state="disabled")
            # max bio length should be 250
            thebiotext.place(x=30, y=295)

            # cancel bio edit

        """ HomePage -- Page Design -- Pre Refresh/Start"""
        '''  The external user search place  '''
        # search place frame
        externalusersearchframe = tk.Frame(self, padx=183, pady=25, highlightbackground="black", highlightthickness=2, bg="lightgray")
        tk.Label(externalusersearchframe, text="-------", bg="lightgray", fg="lightgray").pack()
        externalusersearchframe.place(x=19, y=8)
        # search place inner stuff
        tk.Label(self, text="Search for users by their username below : ", bg="lightgray", font=largefont)\
            .place(x=25, y=15)
        # the entry for searching users -- !THIS SHIT IS IMPORTANT REMEMBER IT MOTHERFUCKER!
        searcheduserentry = tk.Entry(self, bg="white", font=largefont, width=33)
        searcheduserentry.place(x=25, y=40)
        # search button
        #  ==========================================================
        #  || INFO : REMEMBER TO MAKE THE FUNCTION OF SEARCH LATER ||
        #  ||      MARK THIS DONE WHEN YOU DO IT //Not Done\\      ||
        #  ==========================================================
        searchbutton = tk.Button(self, text="Search User", bg="white", fg="blue", width=10, height=2, command=lambda: searchusersf())
        searchbutton.place(x=330, y=22)

        '''  The actual personal page below  '''
        # showing its the homepage so people know
        tk.Label(self, text="This Is Your Homepage", bg="white", fg="red", font=largefont, width=30, height=1)\
            .place(x=82, y=85)
        # the user data frame
        userdataframe = tk.Frame(self, padx=183, pady=200, highlightbackground="black", highlightthickness=4, bg="gray")
        tk.Label(userdataframe, text="-------", bg="gray", fg="gray")\
            .pack()
        userdataframe.place(x=18, y=130)
        # the user data info to place now (finaly)
        
        # refresh button for both refreshing and starting the page
        refreshbutton = tk.Button(self, text="Refresh", bg="aqua", width=8, heigh=1, command=lambda: refreshhpf())
        refreshbutton.place(x=365, y=85)
        tk.Label(self, text="PAGE NOT LOADED, PLEASE REFRESH!", font=largefont).place(x=65, y=300)

#====================================================================================
#====================================================================================
# Displaying the externaluser the current user searched for
class SearchedUserPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        controller.geometry("450x600")
        controller.resizable(False, False)
        controller.title("DummySocialMediaApp")
        self.config(bg="gray")

        """ SearchedUserPage -- Pre View Page Code -- """

        def viewuserf():
            """ SearchedUserPage -- Post View Page Code -- """
            # getting the global searched username
            global g_searchedusername
            now = datetime.datetime.now()
            # creating the userdata from the searched username
            spuserdata = user_data_collection.find_one({"username": str(g_searchedusername)})

            # creating the needed data to see on the SearchedUser only
            spuserid = spuserdata["_id"]
            spuserusername = spuserdata["username"]
            spuserbirthyear = spuserdata["birthyear"]
            spuserfriendsamount = spuserdata["friendsamount"]
            spuserfriends = spuserdata["friends"]
            spuserbio = spuserdata["userbio"]
            spuserage = str(int(now.year) - int(spuserbirthyear))

            def addfriendf():
                # as the first part of adding a friend first checking if we are friends with the user
                ''' getting the current users data to see if the current user is friends with the searched user'''
                global usedinloginusername
                global usedinloginpassword
                global g_searchedusername
                # creating user data for the current user
                curuserdata = user_data_collection.find_one(
                    {"username": str(usedinloginusername), "password": str(usedinloginpassword)})
                # getting the current users info
                curuseruserid = curuserdata["_id"]
                curuserusername = curuserdata["username"]
                '''curuseremail = curuserdata["email"]
                curuserbirthyear = curuserdata["birthyear"]
                curuserpasword = curuserdata["password"]
                curuserfriendsamount = curuserdata["friendsamount"]
                curuserfriends = curuserdata["friends"]
                curuserbio = curuserdata["userbio"]'''
                # checking if the current user is friends with the searched user
                isfriendsorno = user_data_collection.find_one({"_id": ObjectId(str(curuseruserid)),
                                                               "friends": {
                                                                   "$elemMatch": {
                                                                       "friend_id": ObjectId(str(spuserid))
                                                                   }
                                                               }})
                print(isfriendsorno)
                # TODO =================================================================
                if isfriendsorno == None:
                    # TODO ==== ADDING FRIEND ====
                    print("friend addded")
                    ''' updating the data of the current user '''
                    user_data_collection.update_one({"_id": ObjectId(str(curuseruserid))}, {
                        "$addToSet": {
                            "friends": {
                                "friend_id": str(spuserid),
                                "friend_username": str(spuserusername)
                            }
                        }
                    })
                    user_data_collection.update_one({"_id": ObjectId(str(curuseruserid))}, {
                        "$inc": {
                            "friendsamount": 1
                        }
                    })

                    # =============================================
                    """updating the data of the other user"""
                    user_data_collection.update_one({"_id": ObjectId(str(spuserid))}, {
                        "$addToSet": {
                            "friends": {
                                "friend_id": str(curuseruserid),
                                "friend_username": str(curuserusername)
                            }
                        }
                    })
                    user_data_collection.update_one({"_id": ObjectId(str(spuserid))}, {
                        "$inc": {
                            "friendsamount": 1
                        }
                    })

                    '''======================================================================================================='''''''''
                    ''' CODE HERE IS REQUIRED TO CHECK IF YOU ARE FRIENDS WITH THIS USER OR NOT TO DISPLAY THE BUTTON PROPERLY'''''''''
                    addfriendbuttontext = ""
                    addfriendbuttonbgcolor = ""
                    addfriendbuttonfgcolor = ""
                    # checking if the current user is friends with the searched user
                    curuserdata = user_data_collection.find_one({'_id': ObjectId(str(curuseruserid))},
                        {"username": str(usedinloginusername), "password": str(usedinloginpassword)})
                    # getting the current users info
                    curuserusername = curuserdata["username"]
                    # checking if the user is friends with the other user
                    isfriendsorno = user_data_collection.find_one({"_id": ObjectId(str(curuseruserid)),
                                                                   "friends": {
                                                                       "$elemMatch": {
                                                                           "friend_id": ObjectId(str(spuserid))
                                                                       }
                                                                   }})
                    if isfriendsorno == None:
                        add_remove_friendbutton.config(text="Add Friend", bg="white", fg="blue")
                    else:
                        add_remove_friendbutton.config(text="Remove Friend", bg="red", fg="aqua")

                    '''======================================================================================================='''
                    '''======================================================================================================='''

                    # Bio Location
                    thebiotext = tk.Text(self, width=35, height=7, font=("helvetica", 15))
                    thebiotext.insert(1.0, str(spuserbio))
                    thebiotext.config(state="disabled")
                    # max bio length should be 250
                    thebiotext.place(x=30, y=275)

                    # go to homepage button
                    gotohpbtn = tk.Button(self, text="Go To HomePage", bg="lightgray", fg="blue", width=49, height=2,
                                          font=largefont,
                                          command=lambda: controller.show_frame(HomePage))
                    gotohpbtn.place(x=0, y=550)
                else:
                    # TODO ==== REMOVING FRIEND ====
                    print("friend removed")
                    ''' updating the data of the current user '''
                    user_data_collection.update_one({"_id": ObjectId(str(curuseruserid))}, {
                        "$pull": {
                            "friends": {
                                "friend_id": str(spuserid),
                                "friend_username": str(spuserusername)
                            }
                        }
                    })
                    user_data_collection.update_one({"_id": ObjectId(str(curuseruserid))}, {
                        "$inc": {
                            "friendsamount": -1
                        }
                    })

                    # =============================================
                    """updating the data of the other user"""
                    user_data_collection.update_one({"_id": ObjectId(str(spuserid))}, {
                        "$pull": {
                            "friends": {
                                "friend_id": str(curuseruserid),
                                "friend_username": str(curuserusername)
                            }
                        }
                    })
                    user_data_collection.update_one({"_id": ObjectId(str(spuserid))}, {
                        "$inc": {
                            "friendsamount": -1
                        }
                    })
                    '''======================================================================================================='''''''''
                    ''' CODE HERE IS REQUIRED TO CHECK IF YOU ARE FRIENDS WITH THIS USER OR NOT TO DISPLAY THE BUTTON PROPERLY'''''''''
                    addfriendbuttontext = ""
                    addfriendbuttonbgcolor = ""
                    addfriendbuttonfgcolor = ""
                    # checking if the current user is friends with the searched user
                    curuserdata = user_data_collection.find_one(
                        {"username": str(usedinloginusername), "password": str(usedinloginpassword)})
                    # getting the current users info
                    curuserusername = curuserdata["username"]
                    # checking if the user is friends with the other user
                    isfriendsorno = user_data_collection.find_one({"_id": ObjectId(str(curuseruserid)),
                                                                   "friends": {
                                                                       "$elemMatch": {
                                                                           "friend_id": ObjectId(str(spuserid))
                                                                       }
                                                                   }})
                    # print(isfriendsorno)
                    if isfriendsorno == None:
                        add_remove_friendbutton.config(text="Add Friend", bg="white", fg="blue")
                    else:
                        add_remove_friendbutton.config(text="Remove Friend", bg="red", fg="aqua")

                # TODO =================================================================

            ''' SEARCHING FOR USERS ON THE SEARCHED USER PAGE AYY '''
            def searchusersf():

                def gotohomepagef():
                    # TODO == SAME CODE AS THE PRE-VIEW-PAGE TO REFRESH IT WHEN WE GO TO HP
                    controller.show_frame(HomePage)
                    global g_searchedusername
                    g_searchedusername = ""

                global usedinloginusername
                global g_searchedusername
                # getting the searched data from the username search entry
                g_searchedusername = searcheduserentry.get()
                # checking if the username exists
                searchedusernamedata = user_data_collection.find_one({"username": str(g_searchedusername)})
                if searchedusernamedata == None:
                    tk.messagebox.showerror("ERROR", "USERNAME DOESNT EXIST")
                    # checking if the user searched their own name lol
                elif g_searchedusername == usedinloginusername:
                    tk.messagebox.showerror("ERROR", "YOU CANT SEARCH YOUR OWN NAME :P")
                else:
                    # the username exists so assigning it to the global variable to be used in the SearchedUserPage for data
                    # clearing the entry
                    searcheduserentry.delete(0, 'end')
                    ''' refreshing the search page before reloading it with the new users data '''
                    refreshframe = tk.Frame(self, padx=450, pady=600, bg="gray")
                    tk.Label(refreshframe, text="---------", bg="gray", fg="gray", font=largefont).pack()
                    refreshframe.place(x=0, y=0)
                    """  BASICALLY COPYPASTING THE CODE  (TOO LAZY FOR ANY OTHER FIX)"""
                    sp_externalusersearchframe = tk.Frame(self, padx=183, pady=25, highlightbackground="black",
                                                          highlightthickness=2, bg="lightgray")
                    tk.Label(sp_externalusersearchframe, text="-------", bg="lightgray", fg="lightgray").pack()
                    sp_externalusersearchframe.place(x=19, y=8)
                    # USER FOUN LABEL
                    tk.Label(self, text="USER FOUND", bg="lightgray", font=largefont) \
                        .place(x=170, y=15)
                    # viewuserbutton rather than refresh haha *_c_l_e_v_e_r_*
                    viewuserbutton = tk.Button(self, text="View User", bg="white", fg="blue", font=largefont, width=10,
                                               height=1, command=lambda: viewuserf())
                    viewuserbutton.place(x=175, y=37)

                    # go to homepage button
                    gotohpbtn = tk.Button(self, text="Go To HomePage", bg="lightgray", fg="blue", width=49, height=2,
                                          font=largefont,
                                          command=lambda: gotohomepagef())
                    gotohpbtn.place(x=0, y=550)
                    userfriendslabel.config(text="Friends -- " + str(spuserfriendsamount))

                    # sending the user to the searched user page
                    controller.show_frame(SearchedUserPage)


            """ SearchedUserPage -- Post View -- Page Design"""
            # creating the user search bar on top of the user post view frame
            externalusersearchframe = tk.Frame(self, padx=183, pady=25, highlightbackground="black",
                                               highlightthickness=2, bg="lightgray")
            tk.Label(externalusersearchframe, text="-------", bg="lightgray", fg="lightgray").pack()
            externalusersearchframe.place(x=19, y=8)
            # search place inner stuff
            tk.Label(self, text="Search for users by their username below : ", bg="lightgray", font=largefont) \
                .place(x=25, y=15)
            # the entry for searching users -- !THIS SHIT IS IMPORTANT REMEMBER IT MOTHERFUCKER!
            searcheduserentry = tk.Entry(self, bg="white", font=largefont, width=33)
            searcheduserentry.place(x=25, y=40)
            # search button
            #  ==========================================================
            #  || INFO : REMEMBER TO MAKE THE FUNCTION OF SEARCH LATER ||
            #  ||      MARK THIS DONE WHEN YOU DO IT //Not Done\\      ||
            #  ==========================================================
            searchbutton = tk.Button(self, text="Search User", bg="white", fg="blue", width=10, height=2, command=lambda: searchusersf())
            searchbutton.place(x=330, y=22)

            # creating the post view frame
            suuserdataframe = tk.Frame(self, padx=183, pady=170, highlightbackground="black", highlightthickness=4,
                                     bg="lightgray")
            tk.Label(suuserdataframe, text="-------", bg="lightgray", fg="lightgray") \
                .pack()
            suuserdataframe.place(x=18, y=118)
            # creating the user info shit
            # username label
            usernamelabel = tk.Label(self, text="Username -- " + spuserusername, bg="lightgray", font=largefont)
            usernamelabel.place(x=35, y=133)
            # user age label
            useragelabel = tk.Label(self, text="Age -- " + str(spuserage), bg="lightgray", font=largefont)
            useragelabel.place(x=35, y=165)

            # user friends label
            userfriendslabel = tk.Label(self, text="Friends -- " + str(spuserfriendsamount), bg="lightgray",
                                        font=largefont)
            userfriendslabel.place(x=35, y=191)

            # message user button
            gotomessagesbutton = tk.Button(self, text="Message This User", bg="white", fg="blue",
                                           font=largefont, width=15, height=2)
            gotomessagesbutton.place(x=65, y=213)

            '''======================================================================================================='''''''''
            ''' CODE HERE IS REQUIRED TO CHECK IF YOU ARE FRIENDS WITH THIS USER OR NOT TO DISPLAY THE BUTTON PROPERLY'''''''''
            addfriendbuttontext = ""
            addfriendbuttonbgcolor = ""
            addfriendbuttonfgcolor = ""
            #checking if the current user is friends with the searched user
            global usedinloginusername
            global usedinloginpassword
            curuserdata = user_data_collection.find_one(
                {"username": str(usedinloginusername), "password": str(usedinloginpassword)})
            # getting the current users info
            curuseruserid = curuserdata["_id"]
            # checking if the user is friends with the other user
            isfriendsorno = user_data_collection.find_one({"_id": ObjectId(str(curuseruserid)),
                                                           "friends": {
                                                               "$elemMatch": {
                                                                   "friend_id": ObjectId(str(spuserid))
                                                               }
                                                           }})
            # print(isfriendsorno)
            if isfriendsorno == None:
                addfriendbuttontext = "Add Friend"
                addfriendbuttonbgcolor = "white"
                addfriendbuttonfgcolor = "blue"
            else:
                addfriendbuttontext = "Remove Friend"
                addfriendbuttonbgcolor = "red"
                addfriendbuttonfgcolor = "aqua"

            # Add friend/unfriendbutton
            add_remove_friendbutton = tk.Button(self, text=str(addfriendbuttontext), bg=str(addfriendbuttonbgcolor), fg=str(addfriendbuttonfgcolor),
                                                font=largefont, width=15, height=2, command=lambda: addfriendf())
            add_remove_friendbutton.place(x=250, y=213)
            userfriendslabel.config(text="Friends -- " + str(spuserfriendsamount))

            '''======================================================================================================='''
            '''======================================================================================================='''

            # Bio Location
            thebiotext = tk.Text(self, width=35, height=7, font=("helvetica", 15))
            thebiotext.insert(1.0, str(spuserbio))
            thebiotext.config(state="disabled")
            # max bio length should be 250
            thebiotext.place(x=30, y=275)

            # go to homepage button
            def gotohomepagef():
                # TODO == SAME CODE AS THE PRE-VIEW-PAGE TO REFRESH IT WHEN WE GO TO HP
                global g_searchedusername
                g_searchedusername = ""

                '''   CLEARING THE BG BEFORE DISPLAYING THE VIEW/ETC THINGS'''
                bgclearingframe = tk.Frame(self, bg="gray", padx=450, pady=600)
                tk.Label(bgclearingframe, text="-----", bg="gray", fg="gray").pack()
                bgclearingframe.place(x=0, y=0)

                # user found place frame
                sp_externalusersearchframe = tk.Frame(self, padx=183, pady=25, highlightbackground="black",
                                                      highlightthickness=2, bg="lightgray")
                tk.Label(sp_externalusersearchframe, text="-------", bg="lightgray", fg="lightgray").pack()
                sp_externalusersearchframe.place(x=19, y=8)
                # USER FOUN LABEL
                tk.Label(self, text="USER FOUND", bg="lightgray", font=largefont) \
                    .place(x=170, y=15)
                # viewuserbutton rather than refresh haha *_c_l_e_v_e_r_*
                viewuserbutton = tk.Button(self, text="View User", bg="white", fg="blue", font=largefont, width=10,
                                           height=1, command=lambda: viewuserf())
                viewuserbutton.place(x=175, y=37)
                # go to homepage button
                gotohpbtn = tk.Button(self, text="Go To HomePage", bg="lightgray", fg="blue", width=49, height=2,
                                      font=largefont,
                                      command=lambda: controller.show_frame(HomePage))
                gotohpbtn.place(x=0, y=550)
                controller.show_frame(HomePage)
            gotohpbtn = tk.Button(self, text="Go To HomePage", bg="lightgray", fg="blue", width=49, height=2, font=largefont,
                                  command=lambda: gotohomepagef())

            gotohpbtn.place(x=0, y=550)

        """ SearchedUserPage Pre View -- Page Design"""
        # user found place frame
        sp_externalusersearchframe = tk.Frame(self, padx=183, pady=25, highlightbackground="black", highlightthickness=2, bg="lightgray")
        tk.Label(sp_externalusersearchframe, text="-------", bg="lightgray", fg="lightgray").pack()
        sp_externalusersearchframe.place(x=19, y=8)
        # USER FOUN LABEL
        tk.Label(self, text="USER FOUND", bg="lightgray", font=largefont)\
            .place(x=170, y=15)
        # viewuserbutton rather than refresh haha *_c_l_e_v_e_r_*
        viewuserbutton = tk.Button(self, text="View User", bg="white", fg="blue", font=largefont, width=10, height=1, command=lambda: viewuserf())
        viewuserbutton.place(x=175, y=37)
        # go to homepage button
        gotohpbtn = tk.Button(self, text="Go To HomePage", bg="lightgray", fg="blue", width=49, height=2,
                              font=largefont,
                              command=lambda: controller.show_frame(HomePage))
        gotohpbtn.place(x=0, y=550)

#====================================================================================
#====================================================================================
# The Chat Page
class ChatPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        controller.geometry("450x600")
        controller.resizable(False, False)
        controller.title("DummySocialMediaApp")

        """ ChatPage -- Page Code -- """

        """ ChatPage -- Page Design"""

# ====================================================================================
# ====================================================================================
# The Chat Page
class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        controller.geometry("450x600")
        controller.resizable(False, False)
        controller.title("DummySocialMediaApp")
        self.config(bg="gray")

        """ SettingsPage -- Page Code -- """
        # logout function
        def logoutf():
            global usedinloginusername
            global usedinloginpassword
            global g_searchedusername
            usedinloginusername = ""
            usedinloginpassword = ""
            g_searchedusername = ""
            controller.show_frame(LoginPage)

        """ SettingsPage -- Page Design"""
        settingsframe = tk.Frame(self, padx=192, pady=250, highlightbackground="black", highlightthickness=2, bg="lightgray")
        tk.Label(settingsframe, text="-------", bg="lightgray", fg="lightgray", font=largefont).pack()
        settingsframe.place(x=10, y=10)

        # its settings page label
        tk.Label(self, text="SETTINGS", width=20, height=3, font=largefont, bg="gray", fg="white")\
            .place(x=140, y=50)

        # the logout Button
        logoutbutton = tk.Button(self, text="Logout", width=16, height=3, bg="gray", fg="blue", command=lambda: logoutf())
        logoutbutton.place(x=175, y=120)

        # go to homepage button
        gotohpbtn = tk.Button(self, text="Go To HomePage", bg="lightgray", fg="blue", width=49, height=2,
                              font=largefont,
                              command=lambda: controller.show_frame(HomePage))
        gotohpbtn.place(x=0, y=550)
        
app = tkinterApp()
app.mainloop()
