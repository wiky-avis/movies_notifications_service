CREATE_DELIVERY = """
    INSERT INTO deliveries(template_id, recipient, parameters, channel, type, sender)
    VALUES ($1, $2, $3, $4, $5, $6)
    RETURNING delivery_id;
"""

CREATE_TEMPLATE = """
    INSERT INTO templates(
        template_name,
        template_body,
        description,
        mandatory_parameters,
        optional_parameters,
        channel,
        type
    )
    VALUES ($1, $2, $3, $4, $5, $6, $7);
    RETURNING template_id;
"""

CHECK_TEMPLATE = """
    select template_id
    from templates
    where template_name = $1
    ;
"""
