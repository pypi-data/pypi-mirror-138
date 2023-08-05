"""Tag Foreign Key and cascades

Revision ID: 4903aef6a91d
Revises: 9d16de5f03a7
Create Date: 2021-11-24 17:38:11.753522

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "4903aef6a91d"
down_revision = "9d16de5f03a7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "_feature_sets_tags_obj_name_fk", "feature_sets_tags", type_="foreignkey"
    )
    op.drop_constraint(
        "_feature_vectors_tags_obj_name_fk", "feature_vectors_tags", type_="foreignkey"
    )
    op.drop_constraint(
        "_functions_tags_obj_name_fk", "functions_tags", type_="foreignkey"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(
        "_functions_tags_obj_name_fk",
        "functions_tags",
        "functions",
        ["obj_name"],
        ["name"],
    )
    op.create_foreign_key(
        "_feature_vectors_tags_obj_name_fk",
        "feature_vectors_tags",
        "feature_vectors",
        ["obj_name"],
        ["name"],
    )
    op.create_foreign_key(
        "_feature_sets_tags_obj_name_fk",
        "feature_sets_tags",
        "feature_sets",
        ["obj_name"],
        ["name"],
    )
    # ### end Alembic commands ###
