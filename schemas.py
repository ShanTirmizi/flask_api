from marshmallow import Schema, fields

# class ItemSchema(Schema):
#   id = fields.Str(dump_only=True)  # The 'id' will be included when sending data out, but ignored when receiving data.
#   name = fields.Str(required=True)              # The 'name' can be both sent out and included when receiving data.
#   price = fields.Float(required=True)
#   store_id = fields.Str(required=True)

# class ItemUpdateScheme(Schema):
#   name = fields.Str()
#   price = fields.Float()

# class StoreSchema(Schema):
#   id = fields.Str(dump_only=True)
#   name = fields.Str(required=True)

class PlainItemSchema(Schema):
  id = fields.Int(dump_only=True)  # The 'id' will be included when sending data out, but ignored when receiving data.
  name = fields.Str(required=True)              # The 'name' can be both sent out and included when receiving data.
  price = fields.Float(required=True)

class PlainStoreSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)

class PlainTagSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str()


class ItemUpdateScheme(Schema):
  name = fields.Str()
  price = fields.Float()
  store_id = fields.Int()

class ItemSchema(PlainItemSchema):
  store_id = fields.Int(required=True, load_only=True)
  # Find out what dumping only is
  store = fields.Nested(PlainStoreSchema(), dump_only=True)
  tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class StoreSchema(PlainStoreSchema):
  items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
  tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
  store_id = fields.Int(load_only=True)
  store = fields.Nested(PlainStoreSchema(), dump_only=True)
  items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class TagAndItemSchema(Schema):
  message = fields.Str()
  item = fields.Nested(ItemSchema)
  tag = fields.Nested(TagSchema)