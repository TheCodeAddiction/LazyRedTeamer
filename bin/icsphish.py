#!/usr/bin/env python3
import argparse
import os
import time
import codecs
import smtplib
import datetime
import sys
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate

EMAIL_SUBJECT = "HR Meeting"

EVENT_SUMMARY = "HR meeting"

ORGANIZER_NAME = "HR Team Corp1"
ATTENDEES = ["ceo@corp1.com", "cto@corp1.com"]

EVENT_TEXT = """
Dear colleague,

We would like to inform you about an important HR meeting regarding recent company-wide changes and policies. Your attendance is highly encouraged as we will be discussing essential updates that impact all employees.

Topics will include:

- Organizational restructuring
- New employee benefits package
- Updates to leave policies
- Changes to the remote work policy

This meeting is a priority and will be your opportunity to ask any questions or raise concerns.

We look forward to your participation.

Best regards,
HR Team
"""

# currently depricated. I was considering generating all my templates on the fly and having options for which one you wanted to create
# But decided that it was very much out of current scope. see the templates folders for some basic templates.
def create_ics_template():
    file_name  = "meeting.ics"
    current_dir = os.path.dirname(__file__)
    path = os.path.join(current_dir,"../","templates", file_name)

    # The literal iCalendar text, untouched
    ical_text = r"""BEGIN:VCALENDAR
PRODID:Microsoft Exchange Server 2022
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VTIMEZONE
TZID:UTC
BEGIN:STANDARD
DTSTART:{DTSTART}
TZOFFSETFROM:+0000
TZOFFSETTO:+0000
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:{DTSTART}
TZOFFSETFROM:+0000
TZOFFSETTO:+0000
END:DAYLIGHT
END:VTIMEZONE
BEGIN:VEVENT
DTSTART;TZID=UTC:{DTSTART}
DTEND;TZID=UTC:{DTEND}
DTSTAMP:{DTSTAMP}
ORGANIZER;CN={ORGANIZER_NAME}:mailto:{ORGANIZER_EMAIL}
ATTACH;FMTTYPE=application/octet-stream;ENCODING=BASE64:\c3RhcnQgY21kLmV4ZQo=
UID:FIXMEUID{DTSTAMP}
{ATTENDEES}
CREATED:{DTSTAMP}
DESCRIPTION:{DESCRIPTION}
LAST-MODIFIED:{DTSTAMP}
LOCATION:Microsoft Teams Meeting
SEQUENCE:0
STATUS:CONFIRMED
SUMMARY:{SUMMARY}
TRANSP:OPAQUE
END:VEVENT
END:VCALENDAR
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(ical_text)

def generate_attendees():
    attendees = []
    for attendee in ATTENDEES:
        attendees.append(
            "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=FALSE\r\n ;CN={attendee};X-NUM-GUESTS=0:\r\n mailto:{attendee}".format(attendee=attendee)
        )
    return "\r\n".join(attendees)


def load_html_template(html_template_path):
    template = ""
    with codecs.open(html_template_path, 'r', 'utf-8') as f:
        template = f.read()
    return template

# currently only uses hardcoded values, should be dynamic
def load_ics(ics_template_path):
    ics = ""
    with codecs.open(ics_template_path, 'r', 'utf-8') as f:
        ics = f.read()
    return ics

def prepare_ics(dtstamp, dtstart, dtend, sender_email, event_url,ics_template_path):
    ics_template = load_ics(ics_template_path)
    ics_template = ics_template.format(
        DTSTAMP=dtstamp,
        DTSTART=dtstart,
        DTEND=dtend,
        ORGANIZER_NAME=ORGANIZER_NAME,
        ORGANIZER_EMAIL=sender_email,
        DESCRIPTION=event_url,  # Use event_url as DESCRIPTION
        SUMMARY=EVENT_SUMMARY,
        ATTENDEES=generate_attendees()
    )
    return ics_template

def prepare_html_template(event_url,html_template_path):
    email_template = load_html_template(html_template_path)
    email_template = email_template.format(EVENT_TEXT=EVENT_TEXT, EVENT_URL=event_url)
    return email_template

def send_email(smtp_server,from_field,to_field,event_url,ics_template_path,html_template_path):
    # Creates utc timezone variables to set into our .ics template
    utc_offset = time.localtime().tm_gmtoff / 60
    ddtstart = datetime.datetime.now()
    dtoff = datetime.timedelta(minutes=utc_offset + 5)  # meeting has started 5 minutes ago
    duration = datetime.timedelta(hours=1)  # meeting duration
    ddtstart = ddtstart - dtoff
    dtend = ddtstart + duration
    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
    dtend = dtend.strftime("%Y%m%dT%H%M%SZ")

    msg = MIMEMultipart('mixed')
    msg['Reply-To'] = from_field
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = from_field
    msg['To'] = to_field

    ics = prepare_ics(dtstamp, dtstart, dtend, from_field, event_url,ics_template_path)
    email_body = prepare_html_template(event_url,html_template_path)

    part_email = MIMEText(email_body, "html")
    part_cal = MIMEText(ics, 'calendar;method=REQUEST')

    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)

    ics_atch = MIMEBase('application/ics', ' ;name="%s"' % ("invite.ics"))
    ics_atch.set_payload(ics)
    encode_base64(ics_atch)
    ics_atch.add_header('Content-Disposition', 'attachment; filename="%s"' % ("invite.ics"))

    eml_atch = MIMEBase('text/plain', '')
    eml_atch.set_payload("")
    encode_base64(eml_atch)
    eml_atch.add_header('Content-Transfer-Encoding', "")

    msg_alternative.attach(part_email)
    msg_alternative.attach(part_cal)

    mailServer = smtplib.SMTP(smtp_server, 25)
    mailServer.ehlo()
    mailServer.ehlo()
    mailServer.sendmail(from_field, to_field, msg.as_string())
    mailServer.close()


def main():
    parser = argparse.ArgumentParser(
        description='Send an HR meeting invitation via email with .ics attachment.'
    )
    parser.add_argument('--smtp-server', required=True, help='SMTP server address (e.g., smtp.example.com)')
    parser.add_argument('--from', dest='from_field', required=True, help='Sender email address')
    parser.add_argument('--to', dest='to_field', required=True, help='Recipient email address')
    parser.add_argument('--event-url', dest='event_url', required=True, help='URL or additional description for the event')
    parser.add_argument('--ics-template', dest='ics_template', default=os.path.join(os.path.dirname(__file__), '../templates/meeting.ics'), help='Path to the ICS template')
    parser.add_argument('--html-template', dest='html_template', default=os.path.join(os.path.dirname(__file__), '../templates/invite.html'), help='Path to the HTML email template')

    args = parser.parse_args()

    # Validate template files exist
    if not os.path.isfile(args.ics_template):
        print(f"Error: ICS template not found at {args.ics_template}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(args.html_template):
        print(f"Error: HTML template not found at {args.html_template}", file=sys.stderr)
        sys.exit(1)

    try:
        send_email(
            smtp_server=args.smtp_server,
            from_field=args.from_field,
            to_field=args.to_field,
            event_url=args.event_url,
            ics_template_path=args.ics_template,
            html_template_path=args.html_template
        )
        print("Invitation sent successfully.")
    except Exception as e:
        print(f"Failed to send invitation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()