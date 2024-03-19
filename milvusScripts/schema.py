from pymilvus import CollectionSchema, FieldSchema, DataType

chunk_id = FieldSchema(
  name="chunk_id",
  dtype=DataType.INT64,
  is_primary=True,
  auto_id=True,
)

paper_id = FieldSchema(
  name="paper_id",
  dtype=DataType.INT64,
)

paper_title = FieldSchema(
  name="paper_title",
  dtype=DataType.VARCHAR,
  max_length=200,
  # The default value will be used if this field is left empty during data inserts or upserts.
  # The data type of `default_value` must be the same as that specified in `dtype`.
  default_value="Unknown"
)
tokenCount = FieldSchema(
  name="tokenCount",
  dtype=DataType.INT64,
  # The default value will be used if this field is left empty during data inserts or upserts.
  # The data type of `default_value` must be the same as that specified in `dtype`.
  default_value=9999
)
paperVector = FieldSchema(
  name="paperVector",
  dtype=DataType.FLOAT_VECTOR,
  dim=2
)
paper_text = FieldSchema(
    name="paper_text",
    dtype=DataType.VARCHAR,
    max_length=2048
)

schema = CollectionSchema(
  fields=[chunk_id, paper_id, paper_title, tokenCount, paperVector],
  description="AI research search",
  enable_dynamic_field=True
)
collection_name = "papers"
