GET_DELIVERY = """
    SELECT delivery_id, template_id, channel, "type", recipient, parameters, sender, created_dt, updated_dt
    FROM deliveries
    WHERE delivery_id=$1 and not excluded;
"""

SET_EXCLUDED_DELIVERY = """
    UPDATE deliveries SET excluded = true, exclude_reason = $1, updated_dt = now()
    WHERE delivery_id = $2;
"""

GET_USER_UNSUBSCRIPTION = """
    SELECT id, user_id, reason, channel_type, created_dt
    FROM unsubscribed_users
    WHERE user_id=$1;
"""

GET_READY_TO_SEND_DELIVERIES = """
    SELECT delivery_id, recipient
    FROM deliveries
    WHERE NOT excluded AND type = 'not_night' AND CAST(tz AS INTEGER) BETWEEN $1 AND $2
    ORDER BY created_dt;
"""

CREATE_DELIVERY_DISTRIBUTION = """
    INSERT INTO delivery_distributions (delivery_id, recipient, status)
    VALUES ($1, $2, $3) RETURNING id;
"""

UPDATE_DELIVERY = """
    UPDATE deliveries SET recipient=$1, tz=$2, updated_dt = now()
    WHERE delivery_id=$3;
"""

CREATE_DELIVERY_DISTRIBUTION = """
    INSERT INTO delivery_distributions (delivery_id, recipient, status)
    VALUES ($1, $2, $3) RETURNING id;
"""

SET_DISTRIBUTIONS_STATUS = """
    UPDATE delivery_distributions SET status = $1, errors = $2, updated_dt = now()
    WHERE delivery_id = $3;
"""
