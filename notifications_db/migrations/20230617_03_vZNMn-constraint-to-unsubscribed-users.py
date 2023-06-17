"""
constraint to unsubscribed_users
"""

from yoyo import step

__depends__ = {'20230617_02_pXSEo-add-table-unsubscribed-users'}

steps = [
    step(
        """
            set lock_timeout to '5s';
            alter table unsubscribed_users add constraint unsubscribed_user_id_uniq UNIQUE (user_id);
        """,
        """
            set lock_timeout to '5s';
            alter table unsubscribed_users drop constraint if exists unsubscribed_user_id_uniq;
        """
    )
]
