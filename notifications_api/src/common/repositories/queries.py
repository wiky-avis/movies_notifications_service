CREATE_DELIVERY = """
    INSERT INTO deliveries(template_id, recipient, parameters, channel, type, sender)
    VALUES ($1, $2, $3, $4, $5, $6)
    RETURNING delivery_id;
"""

GET_DELIVERY_DISTRIBUTIONS = """
    SELECT delivery_id, status, created_dt, updated_dt
    FROM delivery_distributions
    WHERE delivery_id=$1;
"""
