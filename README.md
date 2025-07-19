# jira-automation
Modular Python tool for automating sprint lifecycle tasks in JIRA.

<br/>

Necessary libraries:
- Requests
- Responses

<br/>

1.) Need an API token from JIRA. 

Can be obtained by visiting the Account Settings section from the Jira board page: 

![img.png](img/img.png)

Then select the Security tab at the top of the account settings: 

![img_1.png](img/img_1.png)

Then select the Create and manage API tokens hyperlink in the Security section: 

![img_3.png](img/img_3.png)

Click the Create API token button: 

![img_4.png](img/img_4.png)

Enter whatever name and set the expiration date for a year from the current date. 

![img_5.png](img/img_5.png)

Click the copy button and save the API token in a safe place.

![img_6.png](img/img_6.png)




<br/> <br/>
Useful future hint: 

If creating a run configuration for Pytest, be sure to use the dropdown menu 
and select "script" and set the target to the test folder. The working 
directory should still be the root directory.

If this is omitted (or forgotten), the conftest.py file in the test package 
can be used as a fix.