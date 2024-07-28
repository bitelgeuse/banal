import os

default_palette = {
    "primaryColor": "#d85791",
    "textColor": "#ffffff",
    "backgroundColor": "#191919",
    "secondaryBackgroundColor": "#302e38",
}
palette = default_palette
os.system(
    f'./venv/bin/streamlit run \
    --theme.primaryColor={palette["primaryColor"]}\
    --theme.textColor={palette["textColor"]}\
    --theme.backgroundColor={palette["backgroundColor"]}\
    --theme.secondaryBackgroundColor={palette["secondaryBackgroundColor"]}\
    web.py'
)
