"""
init_db
"""

from yoyo import step


__depends__ = {}

steps = [
    step(
        """
        SET statement_timeout TO '2s';
        CREATE TABLE IF NOT EXISTS notifications (
            notification_id serial4 NOT NULL PRIMARY KEY,
            template_id text NOT NULL,
            recipient_id text NULL,
            excluded boolean DEFAULT FALSE,
            exclude_reason varchar NULL,
            created_dt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_dt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    
        CREATE TABLE IF NOT EXISTS notifications_distributions (
            id serial4 NOT NULL PRIMARY KEY,
            notification_id int4 NOT NULL,
            recipient_id text NULL,
            status varchar NOT NULL,
            created_dt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_dt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        SET statement_timeout TO '2s';
        DROP TABLE IF EXISTS notifications;
        DROP TABLE IF EXISTS notifications_distributions;
        """
    )
]
