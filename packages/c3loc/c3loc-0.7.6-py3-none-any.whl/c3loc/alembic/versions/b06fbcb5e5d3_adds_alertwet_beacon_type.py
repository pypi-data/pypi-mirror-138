"""Adds AlertWet beacon type

Revision ID: b06fbcb5e5d3
Revises: 515df7865792
Create Date: 2022-02-12 15:04:23.452511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b06fbcb5e5d3'
down_revision = '515df7865792'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
CREATE OR REPLACE FUNCTION def_tag_name() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.name IS NOT NULL OR NEW.name != ''
       THEN RETURN NEW;
    ELSIF NEW.type = 'iBeacon' THEN
        NEW.name := 'iBeacon ' || NEW.uuid || ':' || NEW.major || ':' || NEW.minor;
    ELSIF NEW.type = 'LocationAnchor' THEN
            NEW.name := 'Location Anchor ' || NEW.major || ':' || NEW.minor;
    ELSIF NEW.type = 'SmartRelay' THEN
            NEW.name := 'SmartRelay ' || NEW.mac;
    ELSIF New.type = 'SecureSmartRelay' THEN
            NEW.name := 'SecureSmartRelay ' || NEW.bid;
    ELSIF New.type = 'SecureLocationAnchor' THEN
            NEW.name := 'SecureLocationAnchor ' || NEW.bid;
    ELSIF New.type = 'AlertWet' THEN
            NEW.name := 'AlertWet ' || NEW.bid;
    END IF;
    return NEW;
END
$$;""")  # noqa: E501
    op.execute("""
DO $$ BEGIN
    ALTER TYPE tag_type ADD VALUE 'AlertWet';
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;""")  # noqa: E501


def downgrade():
    op.execute("""
CREATE OR REPLACE FUNCTION def_tag_name() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
        IF NEW.name IS NOT NULL OR NEW.name != ''
       THEN RETURN NEW;
    ELSIF NEW.type = 'iBeacon' THEN
        NEW.name := 'iBeacon ' || NEW.uuid || ':' || NEW.major || ':' || NEW.minor;
    ELSIF NEW.type = 'LocationAnchor' THEN
            NEW.name := 'Location Anchor ' || NEW.major || ':' || NEW.minor;
    ELSIF NEW.type = 'SmartRelay' THEN
            NEW.name := 'SmartRelay ' || NEW.mac;
    ELSIF New.type = 'SecureSmartRelay' THEN
            NEW.name := 'SecureSmartRelay ' || NEW.bid;
    ELSIF New.type = 'SecureLocationAnchor' THEN
            NEW.name := 'SecureLocationAnchor ' || NEW.bid;
    END IF;
    return NEW;
END
$$;""")  # noqa: E501
