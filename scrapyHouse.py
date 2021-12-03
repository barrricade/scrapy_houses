import requests
import json

def loop_url_for_data(url, page_count = 1, project_id=None,token=""):
    header = {
        "gzfauthentication": token
    }
    for page_index in range(page_count):
        body = {
            "pageIndex": page_index,
            "pageSize": 10,
            "where": {"keywords": "", "projectId": project_id}
        }
        res = requests.post(url=url,json=body,headers=header)
        if res.status_code == 200:
            yield res.json()
        else:
            raise Exception("请重试")
        
if __init__ == "__main__":
    # 获取小区的信息的页数信息
    housing_estates = []
    houses = []
    estates_page = page_count = next(loop_url_for_data("https://select.pdgzf.com/api/v1.0/app/gzf/project/list"))['data']['pageCount']
    for estate in loop_url_for_data("https://select.pdgzf.com/api/v1.0/app/gzf/project/list",estates_page):
        housing_estates += estate['data']['data']
    for estate in housing_estates:
        page_count = 1
        page_count = next(loop_url_for_data("https://select.pdgzf.com/api/v1.0/app/gzf/house/list", page_count=page_count, project_id=estate['id']))['data']['pageCount']
        for house in loop_url_for_data("https://select.pdgzf.com/api/v1.0/app/gzf/house/list",page_count,project_id=estate['id']):
            houses += house['data']['data']