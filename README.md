
# Clubhub

## Description
Clubhub is a club management system for a university website developed using Python and a flask web framework. In this website, users can sign up as coordinators or students depending on their ID. Once their sign up request is approved by the admin, coordinators can create and manage clubs and events which students can then join.

## Website Screenshots
<img width="940" alt="clubhub-clubs" src="https://github.com/user-attachments/assets/717e4eb1-b17b-437e-96e2-48bf8dc888d9" />

*Clubs* <br>

<img width="941" alt="clubhub-events" src="https://github.com/user-attachments/assets/04d2fc88-b2d5-430a-bb22-bb1b666349b5" />

*Events* <br>

<img width="950" alt="clubhub-requests" src="https://github.com/user-attachments/assets/cebd53fe-2fc7-422f-b3fc-914df1352152" />

*Sign-up requests* <br>

## Getting Started

### Running the website locally (for development)
1. Clone the git repository
``` git clone https://github.com/ElliceNels/ClubHub.git```
2. Create venv
``` python -m venv .venv ```
3. Activate venv
``` . .venv/Scripts/activate ```
4. Install requirements
``` pip install -r requirements.txt ```
5. Run flask app
``` flask --app ClubHub-Mini4\main.py run ```

To deactivate the venv run:
``` deactivate```

***The first to login as the Administrator should do so using the following details:*** <br>
Username: AdminCoordinator <br>
Password: DefaultPassword123!

***Make sure to update the password immediately.***

### Run the website from the deployed docker container
1. Open docker desktop
2. Run this command in terminal
``` docker run -p 5000:5000 xmisty/clubhub:one ```
3. Access website here
http://localhost:5000

