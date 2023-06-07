"""
templates_tables
"""

from yoyo import step

__depends__ = {'20230607_01_X55jW-init-db'}

steps = [
    step(
        """
        create table if not exists templates (
            template_id bigserial primary key,
            template_name varchar(50) not null,
            template_body varchar not null,
            description varchar,
            mandatory_parameters json,
            optional_parameters json,
            channel, varchar(10) not null,
            type varchar not null,
            created_dt timestamp with time zone default now(),
            updated_dt timestamp with time zone default now(),
            unique(template_name)
            );
        
        create index idx_template_name on templates(template_name);
        """,
        """
        drop index if exists idx_template_name;
        drop table if exists templates;
        """
    )
]
