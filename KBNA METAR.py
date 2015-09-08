import urllib2
import datetime
import smtplib
import time
import getpass
# import argparse
import os


def getMETAR(ICAO="KBNA"):
    url = "http://www.aviationweather.gov/adds/metars/?station_ids={" \
	"}&std_trans=standard&chk_metars=on&hoursStr=most+recent+only" \
        "&submitmet=Submit".format(ICAO)
    page = urllib2.urlopen(url)
    html = page.read()

    start = html.find(ICAO)
    end = html.find("</FONT>")

    msg = html[start:end]
    msg = " ".join(msg.split())

    fetchtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    utctime = datetime.datetime.utcnow().strftime("%d%H%M")

    sms = "\nFetched {} ({}Z)\n{}".format(fetchtime, utctime, msg)

    print sms  # print to console

    return sms
    
def get_epass(eaddress):
    while True:
        print
        print "Email address: {}".format(eaddress)
        epass = getpass.getpass("Email password: ")
        try:
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(eaddress, epass)
        except:
            print "Login failed."
        else:
            print "Login successful."
            return epass


def sendMETAR_SMS(sender, sender_pass, recipient, ICAO="KBNA"):
    METAR_text = getMETAR(ICAO)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender, sender_pass)

    server.sendmail(sender, recipient, METAR_text)

    server.quit()


def wait(target_hour, cur_hour=int(datetime.datetime.now().strftime("%H")),
         cur_minute=int(datetime.datetime.now().strftime("%M")),
         cur_second=int(datetime.datetime.now().strftime("%S"))):
    delta_second = (60 - cur_second)
    delta_minute = (60 - cur_minute) - 1
    delta_hour = (target_hour - cur_hour) % 24 - 1
    delta_t = delta_second + delta_minute * 60 + delta_hour * 3600
    print
    print "Waiting {:.2f} minutes (until {}:{}).".format(delta_t / 60., target_hour,
                                                     "00")
    time.sleep(delta_t)


def main():
    email_address = 
    pass_file_name = "METARpass.txt"
    target_address = 
    dir_of_this_script = os.path.dirname(os.path.realpath(__file__))
    pass_file_path = "{}\{}".format(dir_of_this_script, pass_file_name)
    icao_local = "KBNA"
    beginning_hour = 10
    final_hour = 19
    interval = 1
    hours_list = range(beginning_hour, final_hour + 1, interval)

    getMETAR()
    
    # parser = argparse.ArgumentParser()
    # parser.add_argument("epass", nargs="?", type=str, const="")
    # args = parser.parse_args()
    
    if os.path.isfile(pass_file_path):
        print
        # print "Password file found at {}".format(pass_file_path)
        f = open(pass_file_path, 'r')
        email_pass = f.readline()
        f.close()
        print
        print "Email address: {}".format(email_address)
        try:
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(email_address, email_pass)
        except:
            print "Login failed."
            email_pass = get_epass(email_address)
        else:
            print "Login successful."
    # elif args.epass:
        # email_pass = args.epass
        # print
        # print "Email address: {}".format(email_address)
        # try:
            # smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            # smtpserver.ehlo()
            # smtpserver.starttls()
            # smtpserver.ehlo()
            # smtpserver.login(email_address, email_pass)
        # except:
            # print "Login failed."
            # email_pass = get_epass(email_address)
        # else:
            # print "Login successful."
    else:
        email_pass = get_epass(email_address)
        

    while True:
        print
        hour = int(datetime.datetime.now().strftime("%H"))
        minute = int(datetime.datetime.now().strftime("%M"))
        second = int(datetime.datetime.now().strftime("%S"))
        if (hour in hours_list) and (minute == 0):
            sendMETAR_SMS(sender=email_address, sender_pass=email_pass, 
                          recipient=target_address, ICAO=icao_local)
            print
            print "SMS sent at {}".format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # next highest hour in list, or beginning hour if past final hour
        next_valid_hour = next((h for h in hours_list if h > hour),
                               False)
        if next_valid_hour:
            wait(target_hour=next_valid_hour, cur_hour=hour, cur_minute=minute,
             cur_second=second)
        else:
            break

if __name__ == "__main__":
    main()