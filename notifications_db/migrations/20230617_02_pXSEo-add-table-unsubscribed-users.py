"""
add table unsubscribed_users
"""

from yoyo import step

__depends__ = {'20230617_01_zyHE2-add-column-errors'}

steps = [
    step(
        """
        SET statement_timeout TO '2s';   
        CREATE TABLE IF NOT EXISTS unsubscribed_users (
            id bigserial PRIMARY KEY,
            user_id varchar NOT NULL,
            reason text,
            created_dt timestamp with time zone default now()
        );
        """,
        """
        SET statement_timeout TO '2s';
        DROP TABLE IF EXISTS unsubscribed_users;
        """
    )
]
