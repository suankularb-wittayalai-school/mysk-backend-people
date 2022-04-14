from ..database import contact_table, contact_type_table, engine

from mysk_utils.schema import Contact, QueryContact

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


def create_contact(contact: QueryContact) -> Contact:
    """
    Create contact
    :param contact:
    :return:
    """
    conn = engine.connect()
    contact_type_id = conn.execute(
        select([contact_type_table.c.id]).where(
            contact_type_table.c.name == contact.type.value
        )
    ).fetchone()[0]

    if contact_type_id is None:
        raise Exception(f"Contact type {contact.type} not found")

    contact = conn.execute(
        contact_table.insert().values(
            type=contact_type_id,
            value=contact.value,
            name=contact.name,
        )
    ).inserted_primary_key[0]
    conn.close()

    return get_contact_by_id(contact)


def update_contact(contact_id: int, contact: QueryContact) -> Contact:
    """
    Update contact
    :param contact:
    :return:
    """
    conn = engine.connect()
    contact_type_id = conn.execute(
        select([contact_type_table.c.id]).where(
            contact_type_table.c.name == contact.type.value
        )
    ).fetchone()[0]

    if contact_type_id is None:
        raise Exception(f"Contact type {contact.type} not found")

    conn.execute(
        contact_table.update()
        .where(contact_table.c.id == contact_id)
        .values(
            type=contact_type_id,
            value=contact.value,
            name=contact.name,
        )
    )
    conn.close()

    return get_contact_by_id(contact_id)
