# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions andx
# limitations under the License.
import base64
import os
import csv
import timeit

from flask import Flask, render_template, request
import sendgrid
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)

SENDGRID_API_KEY='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'
SENDGRID_SENDER='malika@tmail.ninjalab.com'

start = timeit.default_timer()

# to_emails = []
with open("uploads/recipient.csv") as csvfile:
    reader = csv.reader(csvfile) # change contents to floats
    for row in reader: # each row is a list
        # to_emails.append(row)
        message = Mail(
            from_email=SENDGRID_SENDER,
            to_emails='{},'.format(row[0]),
            subject='This is a test email',
            html_content='<strong>Example</strong> message.')

        file_path = 'uploads/example.pdf'
        with open(file_path, 'rb') as f:
            data = f.read()
            f.close()
        encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType('application/pdf')
        attachment.file_name = FileName('invoice.pdf')
        attachment.disposition = Disposition('attachment')
        attachment.content_id = ContentId('Example Content ID')
        message.attachment = attachment

        try:
            sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

stop = timeit.default_timer()
time = str(stop - start)
