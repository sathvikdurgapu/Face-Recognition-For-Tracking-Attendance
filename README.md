# Face-Recognition-For-Tracking-Attendance

## Overview
The project is done in two modules, one for admin and other one for teacher. 

The admin has to register the student details such as name, email address and also create training data of each student by entering id and taking photos of his/her face and then web app will create model for tht id and save it on server. Admin also can register teachers using the site.

The teacher has to login first and then they can click on attendance tab the student will then have to just click a snap enter class and roll id and press enter to mark their attandance. After marking attendance, If teacher wants to see attendace, just select date and time to see the attendance. And the teacher can also see total attendance for his or her lecture.

### Admin Module

#### Authentication

This function will authenticate the admin by verifying the username and password. Once the admin successfully logged in, register_teacher function is called where the faculty details are collected and stored it in the database. 

#### Training Phase
This function is responsible for training student data through face recognition and storing it in a database. The whole training process involves preprocessing the image and the model generation.

#### Model Generation

This function will result in the model generation through the input image and storing the result in the folder which is named after the register number of the student.

### Teacher Module

#### Image Capturing

This function will be responsible for capturing the image of the student to mark the attendance.

#### Image Detection

This function will classify the student based upon the model which is already trained and stored in database.Once the prediction is completed, the status of the student is stored in the excel sheet.

#### Attendance View

This function will be responsible for viewing the attendance i.e,report for the particular class.

#### Consolidated Report Generation

The function to calculate the overall percentage of the particular course or student.

#### Email

The Teacher can send email for the attendance marked to all the parents as well as students by selecting class and clicking on send mail button.
