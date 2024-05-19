# CITS5505-Group_Project
## Description
QuestHub is a web-based forum designed for users to engage in discussions by posting and answering questions. Users can register, log in, create new tasks, and respond to questions created by others. The application features a leaderboard showcasing top contributors and a user profile section for managing personal information, check their post questions and answered questions and reviewing their contributions. The design prioritizes user-friendliness and responsiveness, utilizing Bootstrap for styling and jQuery for interactive elements. The backend is built using Python Flask, ensuring a robust and scalable server infrastructure. 

## Student Details
| UWA Student ID | Student Name  | Github Username |
|----------------|---------------|-----------------|
|    24014534    |   Jiahe Fan   |     ocele       | 
|    23861003    |  Jianing Liu  |     LJanieL     |  
|    23764722    |   Yapei Chen  | Transparencency |  
|    23778972    |  Xudong Chen  | pilipalaboom27  |  

## Setup Instructions
1. **Ensure Python is installed**: Make sure you have a recent version of Python installed on your system. You can download the latest version from the [official Python website](https://www.python.org/).

2. **Install dependencies**: Open your terminal or command prompt and navigate to the directory where the project is located. Run the following command to install all necessary dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the application**: Once all dependencies are installed, you can start the application by executing the following command:
   ```bash
   python3 run.py
   ```

By following these steps, you should be able to set up and run the application without any issues. If you encounter any problems, please refer to the documentation or seek assistance from the project maintainer.

## Run test application

1. **Before running the test, make sure your Flask application is running locally.**
 You can use the following command to execute the test file:
    ```bash
   python3 test/test_app.py
   ```
Below is a detailed description of the test file:

	- test_1_register: Test the user registration function.
	- test_2_login: Test the user login function.
	- test_3_navigate_links: Test navigation links.
 
## Run cleanup.py if you wish to clean all the testusedata 

 You can use the following command to execute You can use the following command to execute the test file:
    ```bash
   python3 test/cleanup.py
   ```
