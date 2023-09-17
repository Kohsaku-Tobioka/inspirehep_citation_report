# inspirehep_api_practice

This code to setup regular emails about your HEP-inpire citation record. The code is intended to be used with Google Appscript. 

1. Open https://script.google.com/home

2. Click "New Project"

3. Paste this code in "Code.gs"

4. Change the input parameters of the code: authorId, authorName, pastDays(default is 7 days), emailAddress
   ![Screen Shot 2023-09-17 at 9 42 31 AM](https://github.com/Kohsaku-Tobioka/inspirehep_api_practice/assets/100147234/49e1aefc-04cd-440c-ae95-d2ba609bdd74)   
   authorId: Go to your iNSPIRE-HEP auther page, and get "Author Identifier". In my case, it's K.Tobioka.1. Put it in "authorId"  
   authorName: Filter the output of iNSPIRE citation results. While "Lastname, First-name-initial." tends to work, choose it as you want.  
   pastDays: put the days you want to cover from today.  
   emailAddress:  your email address (can be the same gmail)   

6. Click "Triggers" on the left. Click "+Add Trigger" on the bottom right.

7. Adjust Trigger parameters and Save. 
![Screen Shot 2023-09-17 at 9 43 30 AM](https://github.com/Kohsaku-Tobioka/inspirehep_api_practice/assets/100147234/440b9444-faa4-4e21-a862-01b25a174bb5)   
  Choose which function to run->main  
  Choose which deployment should run ->Head  
  Select event source ->Time-driven  
  Select type of time based trigger->Week timer (adjust as you want. Perhaps coordinate with "pastDays")   
  Select day of week->Every Monday (adjust as you want)  
  Select time of day->Midnight to 1am.   

