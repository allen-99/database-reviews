from review.models.models import Text, Theme, BlockOfText
import random
from review import db


def generate_blocks():
    texts = Text.query.all()
    themes = Theme.query.all()

    for text in texts:
        for theme in themes:
            block = BlockOfText(text_id=text.id,
                                theme_id=theme.theme_id,
                                sa_value=(random.randint(-10, 10)) / 10,
                                block_text='da')

            db.session.add(block)

    db.session.commit()
