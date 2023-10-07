# inspirehep_citation_report

This code is to set up regular emails about your HEP-inspire citation record. The code is intended to be used with Google Appscript. 

1. Open https://script.google.com/home

2. Click "New Project"

3. Paste the code(inspirehep_appscrpt.js) in "Code.gs"

4. Change the input parameters of the code: authorId, authorName, pastDays(default is 7 days), emailAddress
   ![Screen Shot 2023-10-07 at 9 17 41 AM](https://github.com/Kohsaku-Tobioka/inspirehep_citation_report/assets/100147234/767d80b6-5881-4c18-974e-274039f603c7)  
   authorId: Go to your iNSPIRE-HEP author page, and get "Author Identifier". In my case, it's K.Tobioka.1. Put it in "authorId"  
   authorName: Filter the output of iNSPIRE citation results. While "Lastname, First-name-initial." tends to work, choose it as you want.  
   pastDays: put the days you want to cover from today.  
   emailAddress:  your email address (it can be the same Gmail)   

6. Click "Triggers" on the left. Click "+Add Trigger" on the bottom right.
   ![Screen Shot 2023-10-07 at 9 29 27 AM](https://github.com/Kohsaku-Tobioka/inspirehep_citation_report/assets/100147234/59770fa2-ba29-4fee-bf45-80e386c6dd3a)


8. Adjust Trigger parameters and Save. 
![Screen Shot 2023-10-07 at 9 29 57 AM](https://github.com/Kohsaku-Tobioka/inspirehep_citation_report/assets/100147234/7fa4049f-70a9-4b63-a047-562d46bd89bf)  
  Choose which function to run->main  
  Choose which deployment should run ->Head  
  Select event source ->Time-driven  
  Select type of time based trigger->Week timer (adjust as you want. Perhaps coordinate with "pastDays")   
  Select day of week->Every Monday (adjust as you want)  
  Select time of day->Midnight to 1am.   

9. Save the trigger. 
