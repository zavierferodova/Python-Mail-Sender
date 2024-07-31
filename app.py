import pandas as pd
from mailer import Mailer
from config import *
from util import var_parser, check_attachment, np_lower
from copy import copy
import argparse

parser = argparse.ArgumentParser(description="Python send emails using a template and a spreadsheet")
parser.add_argument("-d", "--data", metavar="path", type=str,  help="path to the excel spreadsheet file")
args = parser.parse_args()

if args.data:
    subject_path = "template/subject.txt"
    body_path = "template/body.txt"
    data_path = args.data

    # Check data file exist
    if not check_attachment(data_path):
        print("Sorry, data file does not exist!")
        exit(1)

    # Read subject
    with open(subject_path, "r") as file:
        subject = file.read()

    # Read body
    with open(body_path, "r") as file:
        body = file.read()

    # Read spreadsheet data
    df = pd.read_excel(data_path, dtype=str)

    # Lowercase all keys
    old_keys = df.keys()
    lower_keys = np_lower(df.keys())
    df.rename(columns=dict(zip(old_keys, lower_keys)), inplace=True)

    # Check recipient column exists
    if "recipient" not in lower_keys:
        print("Sorry, 'recipient' column does not exist!")
        exit(1)

    not_found_paths = []

    # Finding not existing attachments
    for index, row in df.iterrows():
        row_keys = row.keys()
        attachment_keys = row_keys[row_keys.str.find("attachment") == 0]
        attachments = row[attachment_keys]
        parsed_attachments = []

        for key, row in attachments.items():
            parsed_attachments.append(row.strip())

        # Check if attachments exist
        for path in parsed_attachments:
            result = check_attachment(path)
            if not result:
                not_found_paths.append(path)

    if len(not_found_paths) > 0:
        print("Sorry, the following attachments do not exist: \n")
        for path in not_found_paths:
            print(path)
        exit(1)

    # Initialize mailer
    mailer = Mailer(sender_email, sender_password)

    # Iterate over rows
    for index, row in df.iterrows():
        row_keys = row.keys()
        value_keys = row_keys[row_keys.str.find("attachment") == -1]
        attachment_keys = row_keys[row_keys.str.find("attachment") == 0]
        
        values = row[value_keys]
        attachments = row[attachment_keys]

        parsed_subject = copy(subject)
        parsed_body = copy(body)
        parsed_attachments = []

        # Parse variables
        for item in values.items():
            parsed_subject = var_parser(item, parsed_subject)
            parsed_body = var_parser(item, parsed_body)
        
        # Parse attachments
        for key, row in attachments.items():
            parsed_attachments.append(row.strip())

        recipient = values["recipient"].strip()

        mailer.build_plain_message(recipient, parsed_subject, parsed_body, parsed_attachments)
        mailer.send()

    mailer.close()
else:
    parser.print_help()
