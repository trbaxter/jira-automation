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



<br/>
<br/>

<details>
  <summary>File Details</summary>
  <ul>
      <details>
        <summary>Credentials.py</summary>
          <ul>
            <blockquote>
              <p>
                This module is responsible for retrieving Jira API credentials
                (email and API token) from environment variables stored as 
                repository secrets using a pluggable accessor 
                (<code>getenv</code>) which defaults to <code>os.getenv</code>.
              </p>
              <p>
                It constructs a <code>Credentials</code> object, defined as a
                Pydantic model with strict validation via the custom 
                <code>SAFE_STR</code> type — stripping whitespace and 
                disallowing empty or <code>None</code> values.
              </p>
              <p>
                To avoid exposing internal validation details (such as
                <code>pydantic.ValidationError)</code>, these errors are 
                wrapped in a generic <code>ValueError</code> with a domain-
                specific message. This preserves encapsulation, makes failures
                diagnosable without leaking intenrals, and supports better
                abstraction for future refactors if necessary.
              </p>
            </blockquote>
          </ul>
      </details>
  </ul>
</details>


<br/>
<br/>