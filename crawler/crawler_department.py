from configs.config_department import DEPT_URLS, DEPT_XPATHS, pin_dept, other_dept, has_views_dept
from modules import get_general, get_pinned, get_exceptions

SHEET_NAMES = list(DEPT_URLS.keys())

for name in SHEET_NAMES:
    if name in pin_dept:
        data = get_pinned(DEPT_URLS[name], DEPT_XPATHS[name], -1, 0)
    elif name in other_dept:
        data = get_exceptions(name, DEPT_URLS[name], DEPT_XPATHS[name], -1)
    else:
        data = get_general(DEPT_URLS[name], DEPT_XPATHS[name], -1)
    
    # if data:
    #     update_google_sheets(SPREADSHEET_ID, name, data, 2)
    
    # update_last_modified_time(SPREADSHEET_ID, name)