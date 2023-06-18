CREATE_DELIVERY = """
    INSERT INTO deliveries(template_id, recipient, parameters, channel, type, sender)
    VALUES ($1, $2, $3, $4, $5, $6)
    RETURNING *;
"""

GET_DELIVERY = """
    SELECT d.delivery_id, dd.status, d.template_id, d.channel, d."type", d.recipient, d.parameters, d.sender, d.created_dt, d.updated_dt
    FROM deliveries d
    LEFT JOIN delivery_distributions dd ON dd.delivery_id = d.delivery_id
    WHERE d.delivery_id=$1;
"""
CREATE_UNSUBSCRIBED_USER = """
    INSERT INTO unsubscribed_users(user_id, reason, mailing_type)
    VALUES ($1, $2, $3)
    RETURNING id;
"""
