CREATE_DELIVERY = """
    INSERT INTO deliveries(template_id, recipient, parameters, channel, type, sender)
    VALUES ($1, $2, $3, $4, $5, $6)
    RETURNING delivery_id;
"""
