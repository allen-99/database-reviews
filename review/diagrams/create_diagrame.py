from review.diagrams.base import theme_color
from review.models.getters import get_themes_name
from review.models.models import Text, BlockOfText, Theme
from flask_login import login_required, current_user
import pandas as pd
import matplotlib.pyplot as plt
from review import db
from sqlalchemy import select


@login_required
def create_diagram(themes_ids, datebegin, dateend, company, platforms):
    data_for_themes = []
    for theme_id in themes_ids:
        if datebegin and dateend:
            reviews = select(BlockOfText.block_id.label('id'),
                             BlockOfText.sa_value.label('sa'),
                             Text.date.label('date')).join(BlockOfText).where(Text.date >= datebegin,
                                                                              Text.date <= dateend,
                                                                              Text.company_id == company,
                                                                              Text.platform_id.in_(platforms),
                                                                              BlockOfText.theme_id == theme_id)
        elif datebegin and not dateend:
            reviews = select(BlockOfText.block_id.label('id'),
                             BlockOfText.sa_value.label('sa'),
                             Text.date.label('date')).join(BlockOfText).where(Text.date >= datebegin,
                                                                              Text.company_id == company,
                                                                              Text.platform_id.in_(platforms),
                                                                              BlockOfText.theme_id == theme_id)
        elif not datebegin and dateend:
            reviews = select(BlockOfText.block_id.label('id'),
                             BlockOfText.sa_value.label('sa'),
                             Text.date.label('date')).join(BlockOfText).where(Text.date <= dateend,
                                                                              Text.company_id == company,
                                                                              Text.platform_id.in_(platforms),
                                                                              BlockOfText.theme_id == theme_id)
        else:
            reviews = select(BlockOfText.block_id.label('id'),
                             BlockOfText.sa_value.label('sa'),
                             Text.date.label('date')).join(BlockOfText).where(Text.company_id == company,
                                                                              Text.platform_id.in_(platforms),
                                                                              BlockOfText.theme_id == theme_id)
        one_line_data = db.session.execute(reviews).all()
        data_for_themes.append(one_line_data)

        themes = get_themes_name(themes_ids)
        themes = [a[0] for a in themes]

        create_pict(data_for_themes, themes)


@login_required
def create_pict(data_for_themes, themes):
    plt.rcParams["figure.figsize"] = (20, 5)
    fig, (axs1, axs2) = plt.subplots(2)
    df_data_for_themes = [pd.DataFrame(a) for a in data_for_themes]
    i = 0
    for df in df_data_for_themes:
        df = df.sort_values(by=['date'])
        axs1.plot(df['date'], df['sa'], c=theme_color[i])
        i += 1

    for df in df_data_for_themes:
        df = df.sort_values(by=['date'])
        axs2.bar(df['sa'], df['date'], color=theme_color)
        i += 1

    axs1.legend([theme for theme in themes])

    plt.savefig(f'review/static/${current_user.id}.png')
