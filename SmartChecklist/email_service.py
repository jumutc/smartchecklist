import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_message(to_, _from, text):
    from_ = 'info@thesmartestchecklist.com'

    msg = MIMEText(text)
    msg['Subject'] = 'You have a message from ' + _from
    msg['From'] = from_
    msg['To'] = to_

    try:
        server = smtplib.SMTP('localhost')
        server.sendmail(from_, to_, msg.as_string())
        server.quit()

        return 'Your message was successfully sent!'
    except Exception:
        return 'Error: unable to send message!'

def send_checklist_mail(to_, html, text):
    from_ = 'info@thesmartestchecklist.com'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Your Smartest Checklist'
    msg['From'] = from_
    msg['To'] = to_

    part1 = MIMEText(text)
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    msg.add_header('Content-Disposition', 'inline')

    try:
        server = smtplib.SMTP('localhost')
        server.sendmail(from_, to_, msg.as_string())
        server.quit()

        return 'Your checklist was successfully sent!'
    except Exception:
        return 'Error: unable to send checklist!'


def send_confirmation_mail(user, host):
    from_ = 'info@thesmartestchecklist.com'

    text = """
                Dear user!

                We are very pleased to welcome you as a newcomer of "The Smartest
                Checklist" service.
                Please proceed by the following link
                <http://"""+ host + '/activate_user.html?id=' + str(user.id) +"""> to
                activate your account.

                Yours sincerely,
                "The Smartest Checklist" project team

                ------------------------------------------------------------------------

                If you are not registered for this service, just don't respond to the letter.
            """

    body =  """
            <html>
              <head>
              </head>
              <body>
                Dear """+user.username+"""!<br>
                <div class="gmail_quote">
                  <div>
                    <div class="h5">
                      <div>
                        <p>We are very pleased to welcome you as a newcomer of "The
                          Smartest Checklist" service.<br>
                          Please proceed by the following
                          <a href="http://"""+ host + '/activate_user.html?id=' + str(user.id) +"""\">link</a>
                            to activate your account.<br>
                          <br>
                          Yours sincerely,<br>
                          "The Smartest Checklist" project team<br>
                        </p>
                        <hr><br>
                        If you are not registered for this service, just don't
                        respond to the letter.</div>
                    </div>
                  </div>
                </div>
                <br>
                <br>
              </body>
            </html>
            """

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Your Activation Link for "The Smartest Checklist"'
    msg['To'] = user.email
    msg['From'] = from_

    part1 = MIMEText(text)
    part2 = MIMEText(body, 'html')

    msg.attach(part1)
    msg.attach(part2)
    msg.add_header('Content-Disposition', 'inline')

    try:
        server = smtplib.SMTP('localhost')
        server.sendmail(from_, user.email, msg.as_string())
        server.quit()

        return 'Your activation link was successfully sent!'
    except Exception:
        return 'Error: unable to send activation link!'