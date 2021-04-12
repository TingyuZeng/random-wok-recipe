from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy configuration
Base = declarative_base()

# Create 2 tables for references, based on the input of the csv files

# Table types
class Type(Base):
    '''Table types: basic types of ingredients, columns include id(pk) and type'''
    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    type = Column(String(30), nullable=False)

    ingredients = relationship("Ingredient", back_populates="type")
    methods = relationship("Method", back_populates="type")

    def __repr__(self):
        return "<Type(%r)>" % self.type

# Table styles
class Style(Base):
    '''Table styles: basic cooking styles, columns include id(pk) and style'''
    __tablename__ = "styles"

    id = Column(Integer, primary_key=True)
    style = Column(String(30), nullable=False)

    methods = relationship("Method", back_populates="style")

    def __repr__(self):
        return "<Style(%r)>" % self.style


# Create 2 more tables: ingredients and methods

# Table ingredients
class Ingredient(Base):
    '''Table ingredients. Contains id(pk), name, type_id(fk)'''
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    type_id = Column(Integer, ForeignKey("types.id"))

    type = relationship("Type", back_populates="ingredients")

    def __repr__(self):
        return "<Ingredient(%r)>" % self.name

# Table methods
class Method(Base):
    '''Table methods. Contains id(pk), type_id(fk), style_id(fk), instruction'''
    __tablename__ = "methods"

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey("types.id"))
    style_id = Column(Integer, ForeignKey("styles.id"))
    instruction = Column(String(200), nullable=False)

    type = relationship("Type", back_populates="methods")
    style = relationship("Style", back_populates="methods")

    def __repr__(self):
        return "<Method(%r.%r)>" % (self.id, self.style)

Base_admin = declarative_base()

class Admin(Base_admin):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    hashed_password = Column(String(200), nullable=False)

    def __repr__(self):
        return "<Admin (%r)>" % self.username