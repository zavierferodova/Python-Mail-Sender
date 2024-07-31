# Python Mail Sender
A script to help you send bulk of email message using Excel Spreadsheet data.

### Setup
1. Install required depedencies,
   ```sh
   pip -r requirements.txt
   ```
2. Copy `.env.example` to `.env` file,
   ```sh
   cp .env.example .env
   ```
3. Configure env file,
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=465
   
   SENDER_EMAIL=<your_email>
   SENDER_PASSWORD=<your_email_password>

   ```

### Usage
First of all you need to prepare spreadsheet data like example below,
|     Name    |      Recipient      |    Attachment1    |     Attachment2   |
|:-----------:|:-------------------:|:-----------------:|:-----------------:|
| John Doe    | johndoe@mail.com    | path/to/file.pdf  | path/to/file.jpg  |
| John Carlos | johncarlos@mail.com | path/to/file2.pdf | path/to/file2.jpg |

- **Important !** \
  Make sure your data has `recipient` column to specify message destination.
- **Attachments** \
  Create columns with prefix `attachment` using format like `attachment1`, `attachment_2`, `attachment_3`, etc. Then fill that column with file attachment destination path.
  
- **Running Script** \
  Here is the command example that you can use to run the script,
  ```sh
  python app.py --data Data.xlsx
  ```

### Templating
You can modify subject and body of message on `template/subject.txt` and `template/body.txt` with custom content. And you can using columns as variable to replace message content like below.
- **Input:**
  ```
  Hello {{name}} this is email subject
  ```
- **Output:**
  ```
  Hello John Doe this is email subject
  ```

### Logging
This script log the process on `app.log` file, you can observe it using command below when you're run this script.
```
tail -f app.log
```

### Credits
Made by Zavier Ferodova Al Fitroh 😎 \
Enjoyyy...
