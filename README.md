# Dr. Teeth's Dental Clinic (Management Software)

## About The Project

The primary purpose of the created software is to help the clinic efficiently manage it's day-to-day operations. It allows the clinic to automate numerous time-consuming tasks, thereby saving precious time.

## Built With

* Tkinter (Python Framework)
* SQLite

## Installation

### Step 1 :
Fork all files from the GitHub Repository (https://github.com/Ansfred/DentalClinic-Management-System). Install Tkinter (pip install tkinter)
***
### Step 2 :
Make a 'database' folder. Add a 'clinicDatabase.db' file to it. Under the same directory, make a new .sql file and paste the following commands as stated below.
***
### Step 3 :
> CREATE TABLE employee(
   employee_id          CHAR(15)   PRIMARY KEY    NOT NULL,
   name                 CHAR(30)                  NOT NULL,
   contact_number       INT                       NOT NULL,
   address              TEXT                      NOT NULL,
   aadhar_number        INT                       NOT NULL,
   password             CHAR(30)                  NOT NULL,
   designation          CHAR(50)                  NOT NULL
);

> INSERT INTO employee VALUES('DTC0000', 'Ansfred Dsouza', 8788944520, 'Pune', 634255368879, 'admin', 'Admin');

> CREATE TABLE receipt(
   bill_number              CHAR(15)   PRIMARY KEY    NOT NULL,
   date                     CHAR(30)                  NOT NULL,
   doctor_name              TEXT                      NOT NULL,
   patient_name             TEXT                      NOT NULL,
   patient_mobile           INT                       NOT NULL,
   amount                   INT                       NOT NULL
);
***
### Step 4 :
Save the file (Now DTC0000 is the master admin)
***
### Step 5 :
Run this file. In your VS Code, download the SQLite extension(~ alexcvzz). Press 'Ctrl + Shift + P' / 'Cmd + Shift + P', type 'SQLite'. Click on 'Open Database', select the project database('clinicDatabase.db'). Then again repeat the above step, but this time select 'Run Query'. Respective tables would be created.

## Future Scope
This software can be hosted online and a more scalable database like MongoDB can be used instead of SQLite, which is been used currently.

## PS
All images are manually designed on Canva(https://www.canva.com/). Few images have been sourced from https://www.pexels.com/
