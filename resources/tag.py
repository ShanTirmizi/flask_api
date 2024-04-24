import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema, TagAndItemSchema
from models import StoreModel, TagModel, ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Tags", "tags", description="Operations on tags")

@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
  @blp.response(200, TagSchema(many=True))
  def get(self, store_id):
    store = StoreModel.query.get_or_404(store_id)

    return store.tags.all()
  
  # Read more on how these arguments works
  @blp.arguments(TagSchema)
  @blp.response(201, TagSchema)
  def post(self, tag_data, store_id):
    if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
      abort(400, message="A tag with that name already exists in that store")
    tag = TagModel(**tag_data, store_id=store_id)

    try:
      db.session.add(tag)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(
        500,
        message=str(e)
      )
    return tag


@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagToItem(MethodView):
  @blp.response(201, TagSchema)
  def post(self, item_id, tag_id):
    item = ItemModel.query.get_or_404(item_id)
    tag = TagModel.query.get_or_404(tag_id)
    # Why are we doing this this way and not the other way around
    item.tags.append(tag)

    try:
      db.session.add(item)
      db.session.commit()
    except SQLAlchemyError:
      abort(500, message="An error occurred while inserting the tag.")
    # Why do we return a tag and not the item 
    return tag
  @blp.response(200, TagAndItemSchema)
  def delete(self, item_id, tag_id):
    item = ItemModel.query.get_or_404(item_id)
    tag = TagModel.query.get_or_404(tag_id)

    item.tags.remove(tag)

    try:
      db.session.add(item)
      db.session.commit()
    except SQLAlchemyError:
      abort(
        500,
        message="An error occurred while inserting the tag."
      )
    return {
      "message": "Item removed from tag",
      "item": item,
      "tag": tag
    }
@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
  @blp.response(200, TagSchema)
  def get(self, tag_id):
    tag = TagModel.query.get_or_404(tag_id)
    return tag
  # Read docs about what you can add to the decorators 
  @blp.response(
    202,
    description="Deletes a tag if no item is tagged with it.",
    example={
      "message": "Tag deleted."
    }
  )
  @blp.alt_response(404, description="Tag not found")
  @blp.alt_response(
    400,
    description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted"
  )
  def delete(self, tag_id):
    tag = TagModel.query.get_or_404(tag_id)

    if not tag.items:
      db.session.delete(tag)
      db.commit()
      return {
        "message": "Tag deleted."
      }
    abort(
      400,
      message="Could not delete tag. Please make sure is not associated with any items, then try again."
    )

