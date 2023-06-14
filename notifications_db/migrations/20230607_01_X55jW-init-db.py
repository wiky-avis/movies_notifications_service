"""
init_db
"""

from yoyo import step


__depends__ = {}

steps = [
    step(
        """
        SET statement_timeout TO '2s';
        CREATE TABLE IF NOT EXISTS deliveries (
            delivery_id bigserial PRIMARY KEY,
            template_id bigint NOT NULL,
            recipient jsonb NOT NULL,
            parameters jsonb NOT NULL,
            channel varchar NOT NULL,
            type varchar NOT NULL,
            excluded boolean DEFAULT FALSE,
            exclude_reason varchar NULL,
            sender text NOT NULL,
            created_dt timestamp with time zone default now(),
            updated_dt timestamp with time zone default now()
        );
    
        CREATE TABLE IF NOT EXISTS delivery_distributions (
            id bigserial PRIMARY KEY,
            delivery_id bigint NOT NULL,
            recipient jsonb  NOT NULL,
            status varchar NOT NULL,
            created_dt timestamp with time zone default now(),
            updated_dt timestamp with time zone default now()
        );
        """,
        """
        SET statement_timeout TO '2s';
        DROP TABLE IF EXISTS deliveries;
        DROP TABLE IF EXISTS delivery_distributions;
        """
    )
]
