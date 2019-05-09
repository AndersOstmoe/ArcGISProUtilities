import  ssl, smtplib

class Av_gmail():
    """
    Send  email using gmail. Gmail account must have lowered
    security settings. View this video for instructions:  https://realpython.com/lessons/sending-emails-intro-and-account-configuration/
    This class uses ssl/tls from start to end.

    """

    def __init__(self, sender, password):
        smtp_server = 'smtp.gmail.com'
        port = 465
        context = ssl.create_default_context()
        self.sender = sender
        self.server = smtplib.SMTP_SSL(smtp_server,port, context=context)
        self.server.login(sender, password)


    def sendmails(self, receivers, message):
        """
        Sends email to list of receivers

        :param receivers:  list or string. emailadress to recivers.
        commaseparated if string with more than one adress.

        :return:  None
        """
        if type(receivers) == str:
            receivers = receivers.split(',')
        for receiver in receivers:
                self.server.sendmail(self.sender, receiver, message)
        return