I'm looking for someone who can write a single program (e.g. java script web browser simulator) to collect ALL the information from a specific online database. This should be possible by issuing a succession of website queries, and then parsing and compiling each resulting website response Record into a CSV file for viewing/manipulation as a Table in Excel.

The website is
www2.dre.ca.gov/PublicADP/pplinfo.asp

The query will run over an inputted range of individual "License ID" numbers. (Valid License ID numbers are in the form of an 8 digit number from roughly 00100000 to 02100000.)

Each License ID query will result in an output Record.
Each output Record will be parsed into specific Fields in the CSV file.

The deliverable will be a program which will run on an Apple computer. It will automatically query over a specified sequence of License ID numbers and output each resulting record into a corresponding field of a CSV file. The CSV file will be suitable for importing into Excel for sorting and manipulating of the data.

Examples of Fields are as follows: (There should be one comprehensive field key)

License_Type
Name (Name further parsed into additional fields)
    First_Name
    Last_Name
Mailing_Address (Address further parsed into additional fields as below)
   Mailing_Address_Street_Number
   Mailing_Address_Street_Name
   Mailing_Address_City
   Mailing_Address_State
   Mailing_Address_Zipcode
License_ID
Expiration_Date
License_Status
MLO_License_Endorsement
Corporation_License_Issued
Salesperson_License_Issued
Former_Names
     Former_First_Name1
     Former_Last_Name1
     Former_First_Name2
     Former_Last_Name2
Main_Office
Licensed_Officers (Name up to 3)
     Licensed_Officer1_License_ID
     Licensed_Officer1_First_Name
     Licensed_Officer1_Last_Name
DBA (name up to 6)
     DBA1
     DBA2
     DBA3
     DBA4
     DBA5
     DBA6
Branches
     Branch1
     Branch1_Street_Number
     Branch1_Street_Name
     Branch1_City
     Branch1_State
     Branch1_Zipcode
     Branch2
     Branch2_Street_Number
     Branch2_Street_Name
     Branch2_City
     Branch2_State
     Branch2_Zipcode
Salespersons (provide url link if any)
Employing_Broker (provide License ID and url link if any)
Comment (Capture text if any)
Disiplinary_or_Formal_Action_Documents (provide designation and url link if any)


Examples of various Output Files are provided.