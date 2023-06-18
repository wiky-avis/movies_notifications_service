create table if not exists templates (
    template_id varchar(30) primary key,
    template_body varchar not null,
    description varchar,
    mandatory_parameters json,
    optional_parameters json,
    channel, varchar(10) not null,
    type varchar not null,
    created_dt timestamp with time zone default now(),
    updated_dt timestamp with time zone default now()
);

drop table if exists templates;

