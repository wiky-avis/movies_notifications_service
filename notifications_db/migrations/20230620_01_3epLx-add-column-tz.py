"""
add column tz
"""

from yoyo import step

__depends__ = {'20230617_03_vZNMn-constraint-to-unsubscribed-users'}

steps = [
    step(
        """
            set lock_timeout to '5s';
            ALTER TABLE deliveries
            ADD COLUMN tz varchar NULL
        """,
        """
            set lock_timeout to '5s';
            ALTER TABLE deliveries
            DROP COLUMN tz
        """,
    )
]
