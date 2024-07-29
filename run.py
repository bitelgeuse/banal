import os

default_palette = {
    "primaryColor": "#d85791",
    "textColor": "#ffffff",
    "backgroundColor": "#191919",
    "secondaryBackgroundColor": "#302e38",
}
palette = default_palette
if os.name == "nt":
    os.system(
        f'{os.path.join("venv", "Scripts", "streamlit.exe")} run \
        --theme.primaryColor={palette["primaryColor"]}\
        --theme.textColor={palette["textColor"]}\
        --theme.backgroundColor={palette["backgroundColor"]}\
        --theme.secondaryBackgroundColor={palette["secondaryBackgroundColor"]}\
        web.py'
    )
else:
    os.system(
        f'{os.path.join("venv", "bin", "streamlit")} run \
        --theme.primaryColor={palette["primaryColor"]}\
        --theme.textColor={palette["textColor"]}\
        --theme.backgroundColor={palette["backgroundColor"]}\
        --theme.secondaryBackgroundColor={palette["secondaryBackgroundColor"]}\
        web.py'
    )
