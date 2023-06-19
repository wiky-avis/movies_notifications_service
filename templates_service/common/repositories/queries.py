CREATE_TEMPLATE = """
    insert into templates(
        template_name,
        template_body,
        description,
        mandatory_parameters,
        optional_parameters,
        channel,
        type
    )
    values ($1, $2, $3, $4, $5, $6, $7);
    returning template_id;
"""

CHECK_TEMPLATE = """
    select template_id
    from templates
    where template_name = $1;
"""

UPDATE_TEMPLATE_START = """
    update templates
    set
"""

DELETE_TEMPLATE = """
    delete from templates
    where template_id = $1;
"""

EQUALS_SEARCH = """
    select
        template_id,
        template_name,
        template_body,
        description,
        mandatory_parameters,
        optional_parameters,
        channel,
        type
    from templates
    where 1=1
        and $1 = $2;
"""

MATCH_SEARCH = """
    select
        template_id,
        template_name,
        template_body,
        description,
        mandatory_parameters,
        optional_parameters,
        channel,
        type
    from templates
    where 1=1
        and $1 = LIKE '%' || $2 || '%';
"""

ALL_SEARCH = """
    select
        template_id,
        template_name,
        template_body,
        description,
        mandatory_parameters,
        optional_parameters,
        channel,
        type
    from templates;
"""
