GET_DELIVERY = """
    SELECT delivery_id, template_id, channel, "type", recipient, parameters, sender, created_dt, updated_dt
    FROM deliveries
    WHERE delivery_id=$1;
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
