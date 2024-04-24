from db import db

class ItemModel(db.Model):
  # Look for the table name items in the db
  __tablename__ = "items"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  price = db.Column(db.Float(precision=2), unique=False, nullable=False)
  # Find out what unique = false does
  store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
  # Find out what is back populate as well 
  store = db.relationship("StoreModel", back_populates="items")
  tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")

