GET_DELIVERY = """
    SELECT delivery_id, template_id, channel, "type", recipient, parameters, sender, created_dt, updated_dt
    FROM deliveries
    WHERE delivery_id=$1;
"""
