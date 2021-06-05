# Importing the modules needed for the code
import random
import time
import datetime
import MySQLdb

global ismember
global iscustomer
global customerid
global bookingoff

ismember = False
iscustomer = False


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def main():
    def menu():
        global ismember
        print(" ")
        print("\t\t\t B: Book your room\n")
        print("\t\t\t C: View current bookings\n")
        print("\t\t\t V: View previous bookings\n")
        print("\t\t\t D: View my details\n")
        # if ismember == True:
        #     print("\t\t\t U: Upgrade membership\n")
        #     print("\t\t\t R: Renew membership\n")
        if ismember == False:
            print("\t\t\t M: Become a member\n")
        print("\t\t\t E: Exit\n")

        choice = str(input("Enter a letter: ")).upper()
        if choice == 'B':
            print(" ")
            booking()
            repeat()

        elif choice == 'C':
            print(" ")
            currentBookings()
            repeat()

        elif choice == 'V':
            print(" ")
            viewPast()
            repeat()

        elif choice == 'D':
            print(" ")
            viewDetails()
            repeat()

        # elif choice == 'U':
        #     print(" ")
        #     upgradeMembership()
        #     repeat()
        #
        # elif choice == 'R':
        #     print(" ")
        #     renewMembership()
        #     repeat()

        elif choice == 'M':
            print(" ")
            becomeMember()
            repeat()

        elif choice == 'E':
            quit()

        else:
            if ismember == True:
                print("Please only enter the letters: B, C, V, D, U, R or E.")
                menu()
            elif ismember == False:
                print("Please only enter the letters: B, C, V, D, M or E")
                menu()

    def getRecords(tablename):
        cursor = ""
        db = ""
        try:
            db = MySQLdb.connect(host='localhost', user='root', password='Sweethome@1405', port=3306)
            cursor = db.cursor()
            cursor.execute("USE HOTEL")
            sql = "Select * from " + tablename + " order by Id asc"
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Error as error:
            print(error)
        finally:
            cursor.close()
            db.close()

    def retrieveRoomInfo():
        roomInfoRecords = getRecords('RoomInfo')

        print(color.BOLD + "-" * 85 + color.END)
        print(color.BOLD + "|", "ROOM TYPE", " " * 11, "|", "AMENITIES", " " * 31, "|", "COST per DAY",
              " |" + color.END)
        print(color.BOLD + "-" * 85 + color.END)

        for roomInfoRecord in roomInfoRecords:
            space1 = 20 - len(roomInfoRecord[1])
            space2 = 40 - len(roomInfoRecord[2])
            space3 = 12 - len(str(roomInfoRecord[3]))
            print("|", roomInfoRecord[1], " " * space1, "|", roomInfoRecord[2], " " * space2, "|", roomInfoRecord[3],
                  " " * space3, "|")
            print("-" * 85)

    def booking():
        print("\t\t\t\t\t\t*o*o*o*  BOOKING YOUR ROOMS  *o*o*o*")
        print(" ")
        print("**** Now Choose a Room Type ****")
        retrieveRoomInfo()
        selectedroom = str(input("Enter Room Type (Single, King, Twin..): ")).upper()
        startdate = str(input("Please enter start date (yyyy/mm/dd): "))
        enddate = str(input("Please enter end date (yyyy/mm/dd): "))

        from datetime import datetime
        end_date = datetime.strptime(enddate, "%Y/%m/%d")
        start_date = datetime.strptime(startdate,"%Y/%m/%d")
        totaldays = (end_date - start_date).days

        db = MySQLdb.connect(host='localhost', user='root', password='Sweethome@1405', port=3306)
        cursor = db.cursor()
        cursor.execute("USE HOTEL")

        roomsql = "SELECT * from RoomInfo where roomtype = %s;"
        cursor.execute(roomsql, (selectedroom,))
        selectedroominfo = cursor.fetchall()

        sql = "INSERT INTO booking (customerid, roomtypeid, amount, startdate, enddate)" \
              " VALUES (%s,%s,%s,%s,%s); "
        percentoff = 1.0 - float(bookingoff) / 100
        val = (customerid, selectedroominfo[0][0], float(selectedroominfo[0][3]) * totaldays * percentoff, startdate, enddate)
        cursor.execute(sql, val)
        db.commit()

        cursor.close()
        db.close()

        print("\t\t\t\t\t-------- YOUR ROOM IS SUCCESSFULLY BOOKED ----------")

        print(" ")
        print(" Wishing you a pleasant stay at StarDust Hotels! ")

    def currentBookings():
        print("\t\t\t\t\t\t*o*o*o*  BELOW ARE YOUR UPCOMING BOOKING DETAILS  *o*o*o*")
        db = MySQLdb.connect(host='localhost', user='root', password='Sweethome@1405', port=3306)
        cursor = db.cursor()
        cursor.execute("USE HOTEL")

        curbookings_sql = "select r.RoomType, b.StartDate, b.EndDate, b.Amount from booking b " \
                           "inner join customer c on b.customerid = c.Id " \
                           "inner join RoomInfo r on b.roomtypeid = r.Id " \
                           "where c.Id = %s and b.StartDate > curdate() ;"
        cursor.execute(curbookings_sql, (customerid,))
        curBookingInfos = cursor.fetchall()

        print(color.BOLD + "-" * 85 + color.END)
        print(color.BOLD + "|", "ROOM TYPE", " " * 11, "|", "START DATE", " " * 10, "|", "END DATE", " " * 10, "|",
              "AMOUNT",
              " |" + color.END)
        print(color.BOLD + "-" * 85 + color.END)

        for curBookingInfo in curBookingInfos:
            space1 = 20 - len(str(curBookingInfo[0]))
            space2 = 20 - len(str(curBookingInfo[1]))
            space3 = 18 - len(str(curBookingInfo[2]))
            print("|", curBookingInfo[0], " " * space1, "|", curBookingInfo[1], " " * space2, "|", curBookingInfo[2],
                  " " * space3, "|", curBookingInfo[3], "|")
            print("-" * 85)

    def viewPast():
        print("\t\t\t\t\t\t*o*o*o*  BELOW ARE YOUR PREVIOUS BOOKING DETAILS  *o*o*o*")
        db = MySQLdb.connect(host='localhost', user='root', password='Sweethome@1405', port=3306)
        cursor = db.cursor()
        cursor.execute("USE HOTEL")

        prevbookings_sql = "select r.RoomType, b.StartDate, b.EndDate, b.Amount from booking b "\
                            "inner join customer c on b.customerid = c.Id "\
                            "inner join RoomInfo r on b.roomtypeid = r.Id "\
                            "where c.Id = %s and b.StartDate < curdate() ;"
        cursor.execute(prevbookings_sql, (customerid,))
        prevBookingInfos = cursor.fetchall()

        print(color.BOLD + "-" * 85 + color.END)
        print(color.BOLD + "|", "ROOM TYPE", " " * 11, "|", "START DATE", " " * 10, "|", "END DATE", " " * 10, "|", "AMOUNT",
              " |" + color.END)
        print(color.BOLD + "-" * 85 + color.END)

        for prevBookingInfo in prevBookingInfos:
            space1 = 20 - len(str(prevBookingInfo[0]))
            space2 = 20 - len(str(prevBookingInfo[1]))
            space3 = 18- len(str(prevBookingInfo[2]))
            print("|", prevBookingInfo[0], " " * space1, "|", prevBookingInfo[1], " " * space2, "|", prevBookingInfo[2],
                  " " * space3, "|", prevBookingInfo[3], "|")
            print("-" * 85)

    def viewDetails():
        print("\t\t\t\t\t\t*o*o*o*  BELOW ARE YOUR DETAILS  *o*o*o*")

        db = MySQLdb.connect(host='localhost', user='root', password='Sweethome@1405', port=3306)
        cursor = db.cursor()
        cursor.execute("USE HOTEL")

        customer_sql = "SELECT * from Customer where ID = %s;"
        cursor.execute(customer_sql, (customerid,))
        customerinfos = cursor.fetchall()

        print(color.BOLD + "-" * 250 + color.END)
        print(color.BOLD + "|", "Customer Number", "|", "Firstname", " " * 10, "|",
              "Lastname", " " * 10, "|", "Age", "|", "Gender", "|",
              "Phone", " " * 8, "|", "Email", " " * 15, "|", "Address", " " * 50, "|",
              "Identification Type", "|", "Identification Number", " |" + color.END)
        print(color.BOLD + "-" * 250 + color.END)

        for customerinfo in customerinfos:
            space1 = 4
            space2 = 18 - len(str(customerinfo[2]))
            space3 = 18 - len(str(customerinfo[4]))
            space4 = 1
            space5 = 3 - len(str(customerinfo[6]))
            space6 = 10 - len(str(customerinfo[7]))
            space7 = 15 - len(str(customerinfo[8]))
            space8 = 50 - len(str(customerinfo[9]))
            space9 = 1
            space10 = 1
            print("|", customerinfo[1], " " * space1, "|", customerinfo[2], " " * space2, "|", customerinfo[4],
                  " " * space3, "|", customerinfo[5], " " * space4, "|", customerinfo[6], " " * space5, "|",
                  customerinfo[7],
                  " " * space6, "|", customerinfo[8], " " * space7, "|", customerinfo[9], " " * space8, "|",
                  customerinfo[10],
                  " " * space9, "|", customerinfo[11], " " * space10, "|")
            print("-" * 250)

    def becomeMember():
        print(" ")
        getMembershipPlans = getRecords('MembershipPlans')

        print("-" * 174)
        print(color.BOLD + "|", "MEMBERSHIP PLANS", "|", "MEALS", " " * 25, "|", "BOOKING BENEFITS", " " * 21, "|",
              "OTHER AMENITIES", " " * 11, "|", "ELIGIBILITY", " " * 19, "|", "RENEWAL COST", "|" + color.END)
        print("-" * 174)

        for getMembershipPlan in getMembershipPlans:
            space1 = 15 - len(getMembershipPlan[1])
            space2 = 30 - len(getMembershipPlan[2])
            space3 = 37 - len(getMembershipPlan[3])
            space4 = 26 - len(getMembershipPlan[4])
            space5 = 30 - len(getMembershipPlan[5])
            space6 = 11 - len(str(getMembershipPlan[6]))
            print("|", getMembershipPlan[1], " " * space1, "|", getMembershipPlan[2], " " * space2, "|",
                  getMembershipPlan[3], " " * space3, "|", getMembershipPlan[4], " " * space4, "|",
                  getMembershipPlan[5], " " * space5, "|", getMembershipPlan[6], " " * space6, "|")
            print("-" * 174)

        def member_errorhandling():
            member_yesno = ("Would you like to become a StarDust Member (yes or no)?: ").lower()
            member_yesno = member_yesno.strip()
            if member_yesno == 'yes' or member_yesno == 'y':
                member_type = str(input("Which membership plan would you like to join?: ")).upper()
                member_type = member_type.strip()

                db = MySQLdb.connect(host='localhost', user='root', password='Sweethome@1405', port=3306)
                cursor = db.cursor()
                cursor.execute("USE HOTEL")

                membersql = "SELECT * from RoomInfo where roomtype = %s;"
                cursor.execute(membersql, (member_type,))
                selectMembership = cursor.fetchall()

                global customerid
                sql = "INSERT INTO booking(CustomerId, MembershipPlanId)" \
                      " VALUES (%s, %s); "
                val = (customerid, selectMembership)
                cursor.execute(sql, val)
                db.commit()

                cursor.close()
                db.close()
            elif member_yesno == 'no' or member_yesno == 'n':
                print("Memberships have great benefits, especially if you visit StarDust hotels often.")
                time.sleep(1)
                print(
                    color.BOLD + "Remember that you can always buy a membership from this application if you change your mind! :)" + color.END)
            else:
                print("Please enter either yes or no.")
                member_errorhandling()

        member_errorhandling()


    def repeat():
        wish = input("Would you like to re-run the program?: ").upper()
        if wish == 'YES' or wish == 'Y':
            time.sleep(0.5)
            main()
        elif wish == 'NO' or wish == 'N':
            time.sleep(0.5)
            print("Thank you soo much for using this program!")
            time.sleep(2)
            print("We hope to see you soon!!!")
            time.sleep(1)
        else:
            print("Can you please type 'Yes' or 'No'.")
            time.sleep(1)
            repeat()

    menu()


print("\t\t\t\t\t\t *--*--*--*--*  WELCOME TO HOTEL STARDUST  *--*--*--*--* \n")
print("\t\t\t\t\t\t  ---------------------*  New Delhi  *-------------------      \n")
print(" ")


def elseyesno():
    global ismember
    global iscustomer
    global customerid
    global bookingoff

    existingcustomer = str(input("Are you an existing customer?: ")).lower()
    existingcustomer = existingcustomer.strip()
    if existingcustomer == 'yes' or existingcustomer == 'y':
        customernum = str(input("Please enter your Customer Number?: "))
        try:
            db = MySQLdb.connect(host='localhost', user='root', password='Sweethome@1405', port=3306)
            cursor = db.cursor()
            cursor.execute("USE HOTEL")
            sql = "select c.id, " \
                  "concat(c.firstname,' ', c.surname) as customerFullname, " \
                  "mp.membershiptype, mp.bookingbenefits from customer c " \
                  "inner join member m on m.CustomerId = c.id " \
                  "inner join membershipplans mp on mp.id = m.MembershipPlanId " \
                  "where c.CustomerNumber = %s;"
            cursor.execute(sql, (customernum,))
            results = cursor.fetchall()
            if len(results) == 0:
                ismember = False
                db = MySQLdb.connect(host='localhost', user='root', password='Sweethome@1405', port=3306)
                cursor = db.cursor()
                cursor.execute("USE HOTEL")
                sql = "select c.id, concat(c.firstname,' ', c.surname) as customerFullname" \
                      " from customer c where c.CustomerNumber = %s;"
                cursor.execute(sql, (customernum,))
                results_customer = cursor.fetchall()
                if len(results_customer) == 0:
                    iscustomer = False
                    print("Cannot find the Customer Number. Please re-enter")
                    elseyesno()
                else:
                    iscustomer = True
                    customerid = results_customer[0][0]
                    print(f"Welcome {results_customer[0][1]}!")
            else:
                ismember = True
                customerid = results[0][0]
                bookingoff = results[0][3].strip("%")[0]

                print(f"Welcome {results[0][1]}!")
                print(f"You are our esteemed {results[0][2]} Member!")
        except Error as error:
            print(error)
        finally:
            cursor.close()
            db.close()
    elif existingcustomer == 'no' or existingcustomer == 'n':
        print("Please enter your details")
        firstname_verification = str(input("Enter your firstname: "))
        middlename_verification = str(input("Enter your middle name (optional): "))
        surname_verification = str(input("Enter your lastname: "))
        age_verification = str(input("Enter your age: "))
        gender_verification = str(input("Enter your gender: "))
        phone_verification = str(input("Enter your contact number: "))
        email_verification = str(input("Enter your email: "))
        address_verification = str(input("Enter your address: "))
        vertype_verification = str(input("Enter your identification type (Passport, Aadhar and etc.): "))
        vernumber_verification = str(input("What is the identification number (Passport ID, Aadhar Number and etc.)"
                                           ": "))

        customernum = random.randint(1000000000, 9999999999)

        db = MySQLdb.connect(host='localhost', user='root', password='Sweethome@1405', port=3306)
        cursor = db.cursor()

        cursor.execute("USE HOTEL")
        sql = "INSERT INTO customer (customernumber, firstname, middlename, surname" \
              ", age, gender, phone, email, address, identificationtype, identificationnumber) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); "
        val = (customernum, firstname_verification, middlename_verification, surname_verification, age_verification,
               gender_verification, phone_verification, email_verification, address_verification, vertype_verification,
               vernumber_verification)
        cursor.execute(sql, val)
        db.commit()

        customerid = cursor.lastrowid

        cursor.close()
        db.close()

        print("Your information has been saved successfully!")
        print(f"Your Customer Number is: {customernum}")
        print("Welcome to the StarDust Family!")
        print(color.BOLD + "*Please save customer number for future reference*" + color.END)
        ismember = False
    else:
        print("Please enter only yes or no. Re-enter.")
        elseyesno()


elseyesno()
main()
