from sqlalchemy import create_engine
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    ForeignKey,
    Date,
    # Boolean,
    # Constraint,
    ForeignKeyConstraint,
)
from dotenv import load_dotenv
import os

# from utils.types.student_teacher.contacts import ContactType

# from types.student_teacher.person import Person

load_dotenv()

metadata = MetaData()
engine = create_engine(
    os.environ.get("DATABASE_URL"), connect_args={"check_same_thread": False}
)

contact_type_table = Table(
    "contact_type",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
)

contact_table = Table(
    "contact",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("type", Integer, ForeignKey("contact_type.id"), nullable=False),
    Column("value", String(50), nullable=False),
    ForeignKeyConstraint(
        ["type"], ["contact_type.id"], name="contact_type_fk", ondelete="CASCADE"
    ),
)

person_contact_table = Table(
    "people_contact",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("person_id", Integer, ForeignKey("people.id", ondelete="CASCADE")),
    Column("contact_id", Integer, ForeignKey("contact.id", ondelete="CASCADE")),
)

people_table = Table(
    "people",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("prefix_th", String),
    Column("first_name_th", String),
    Column("middle_name_th", String, nullable=True),
    Column("last_name_th", String),
    Column("prefix_en", String),
    Column("first_name_en", String),
    Column("middle_name_en", String, nullable=True),
    Column("last_name_en", String),
    Column("birthdate", Date),
    Column("citizen_id", String, unique=True),
)

student_table = Table(
    "student",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("person_id", Integer, ForeignKey("people.id")),
    Column("student_id", String),
)

teacher_table = Table(
    "teacher",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("person_id", Integer, ForeignKey("people.id")),
    Column("teacher_id", String),
)

metadata.create_all(engine)

# add contact type to database if none exits

# query current contact types
contact_types = engine.execute("SELECT * FROM contact_type").fetchall()

if contact_types == []:
    # add contact types
    engine.execute(
        contact_type_table.insert(),
        [
            {"name": "Phone"},
            {"name": "Email"},
            {"name": "Facebook"},
            {"name": "Line"},
            {"name": "Instagram"},
            {"name": "Twitter"},
            {"name": "Website"},
            {"name": "Discord"},
            {"name": "Other"},
        ],
    )
