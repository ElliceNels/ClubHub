import sqlite3
from Verification import Verification

class ClubCreationVerification:

    def valid_club(club_name,club_description):
        if len(club_name) > 40:
            print()

    def create_new_club(club_name, club_description, user_id):
        coordinator_id = Verification.UserIdToCoordId(user_id)
        conn = sqlite3.connect('ClubHub-Mini4\database\Clubhub.db')
        cur = conn.cursor()
        cur.execute(''' INSERT INTO CLUBS Club_name, Coordinator_id, Description
                    VALUES ( ?, ?, ? ) ''', (club_name, coordinator_id, club_description))
