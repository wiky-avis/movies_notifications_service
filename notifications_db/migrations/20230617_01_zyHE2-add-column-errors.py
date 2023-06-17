"""
add column errors
"""

from yoyo import step

__depends__ = {'20230615_01_YGhFF-templates-tables'}

steps = [
    step(
        """
            set lock_timeout to '5s';
            ALTER TABLE delivery_distributions
            ADD COLUMN errors jsonb NULL
        """,
        """
            set lock_timeout to '5s';
            ALTER TABLE delivery_distributions
            DROP COLUMN errors
        """,
    )
]
