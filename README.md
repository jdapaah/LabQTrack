# QTrack

This project seeks to help the Princeton University COS Lab TA program track the attendance of their employees.

## Installation Instructions

To use, download the repository and create the following file:

**api_auth.py**

    username =  <api-username>
    API_SECRET = <api-key>

This will allow you to log in and access that database, assuming you have been granted access.

## Features

QTrack allows you to select which students you want to review by supplying a list at the top of the page. Students can be added to and removed from the page by selecting a button from a dynamically updating list of search results.

*video*

QTrack currently supports the following features:

### Active Search

Active Search gives information on which employees are currently helping a student in the Lab Queue. It will generate a card for each of the selected students and relay whom they have been working with and for how long.
*video*

### Period Search

Period Search gives detailed information on the session an employee has worked over a selected range of dates. For each session, it will detail the duration of the session, whether or not they surpassed the advised session limit of 25 minutes, and other information.

*video*
