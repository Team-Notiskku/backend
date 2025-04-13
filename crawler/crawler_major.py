from configs.config_major import MAJOR_URLS, MAJOR_XPATHS, pin_major, other_major
from modules import get_general, get_pinned, get_exceptions

SHEET_NAMES = list(MAJOR_URLS.keys())

for name in SHEET_NAMES:
    if name == "건축학과(건축학계열)":
        data = get_pinned(MAJOR_URLS[name], MAJOR_XPATHS[name], -1, 1)
    elif name in pin_major:
        data = get_pinned(MAJOR_URLS[name], MAJOR_XPATHS[name], -1, 0)
    elif name in other_major:
        data = get_exceptions(name, MAJOR_URLS[name], MAJOR_XPATHS[name], -1)
    else:
        data = get_general(MAJOR_URLS[name], MAJOR_XPATHS[name], -1)
    
    # if data:
    #     update_google_sheets(SPREADSHEET_ID, name, data, 2)
    
    # update_last_modified_time(SPREADSHEET_ID, name)