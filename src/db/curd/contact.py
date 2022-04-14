from ..database import contact_table, contact_type_table, engine

from mysk_utils.schema import Contact

from sqlalchemy import select


def get_contact_by_id(contact_id: int) -> Contact:
    """
    Get contact by id
    :param contact_id:
    :return:
    """
    conn = engine.connect()
    contact = conn.execute(
        select([contact_table, contact_type_table])
        .where(contact_table.c.id == contact_id)
        .join(contact_type_table, contact_table.c.type == contact_type_table.c.id)
    ).fetchone()
    conn.close()

    return Contact(
        id=contact.id, type=contact["name_1"], value=contact.value, name=contact.name
    )
