from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, Table, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association table for many-to-many relationship between User and Role
user_has_role = Table(
    'user_has_role', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('role.id'), primary_key=True)
)


# User model
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    # Relationships
    roles = relationship("Role", secondary=user_has_role, back_populates="users")

    def __repr__(self):
        return f"<User {self.email}>"


# Role model
class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(Text)

    # Relationships
    users = relationship("User", secondary=user_has_role, back_populates="roles")
