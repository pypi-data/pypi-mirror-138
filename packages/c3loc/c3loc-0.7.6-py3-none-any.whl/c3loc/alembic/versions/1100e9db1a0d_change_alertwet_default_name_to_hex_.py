"""Change AlertWet default name to hex representation

Revision ID: 1100e9db1a0d
Revises: b06fbcb5e5d3
Create Date: 2022-02-14 12:27:07.342579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1100e9db1a0d'
down_revision = 'b06fbcb5e5d3'
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
            NEW.name := 'AlertWet ' || to_hex(NEW.bid);
    END IF;
    return NEW;
END
$$;""")  # noqa: E501


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
    ELSIF New.type = 'AlertWet' THEN
            NEW.name := 'AlertWet ' || NEW.bid;
    END IF;
    return NEW;
END
$$;""")  # noqa: E501
