# QTrack

This project seeks to help the Princeton University COS Lab TA program track the attendance of their employees. As a Princeton University internal tool that manages student informaton, the site is registered behind CAS authenitication and cannot be accessed by the public.

## Installation Instructions

To use, download the repository and create the following file:

**api_auth.py**

    username =  <api-username>
    API_SECRET = <api-key>

This will allow you to log in and access that database, assuming you have been granted access.

## Features

QTrack allows you to select which students you want to review by supplying a list at the top of the page. Students can be added to and removed from the page by selecting a button from a dynamically updating list of search results.

https://user-images.githubusercontent.com/61062668/184282580-a2f2aa67-09c6-46fb-8898-17423c372aa7.mp4

QTrack currently supports the following features:

### Active Search

Active Search gives information on which employees are currently helping a student in the Lab Queue. It will generate a card for each of the selected students and relay whom they have been working with and for how long.

<img width="750" alt="activeR" src="https://user-images.githubusercontent.com/61062668/184284191-354728a7-83c1-4e06-bf11-4303bbbc09c6.png">

### Period Search

Period Search gives detailed information on the session an employee has worked over a selected range of dates. For each session, it will detail the duration of the session, whether or not they surpassed the advised session limit of 25 minutes, and other information.

https://user-images.githubusercontent.com/61062668/184285219-896c9e89-9192-4d51-ae8b-033d3efd4694.mp4


