import streamlit as st

import time
import pandas as pd
import requests
import json
import os
import sys


# 打包需要用到
def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.normpath(os.path.join(base_path, relative_path))


# def fetch_and_show_image(url):
#     # 发送HTTP请求下载图片
#     response = requests.get(url)
#     # 将响应内容转换为BytesIO对象，以便PIL处理
#     image_bytes = io.BytesIO(response.content)
#     # 使用PIL从BytesIO对象中打开图片
#     image = Image.open(image_bytes)
#     return image


def get_product(category, price, discount, next_id, cookie):

    category = {"手办": 2312, "模型": 2066, "3C": 2273, "周边": 2331}[category]

    price = [f"{int(price[0] * 100)}-{int(price[1] * 100)}"]
    discount = [f"{int(discount[0] * 10)}-{int(discount[1] * 10)}"]

    url = "https://mall.bilibili.com/mall-magic-c/internet/c2c/v2/list"
    payload = json.dumps(
        {
            "categoryFilter": category,
            "nextId": next_id,
            "priceFilters": price,
            "discountFilters": discount,
        }
    )
    headers = {
        "priority": "u=1, i",
        "Cookie": cookie,
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "content-type": "application/json",
    }

    return requests.request("POST", url, headers=headers, data=payload, timeout=10)


if __name__ == "__main__":

    # 状态初始化
    if "form_submit_button_visible" not in st.session_state:
        st.session_state["form_submit_button_visible"] = False

    # 主页设置
    st.set_page_config(
        page_title="B 站市集低价搜索", page_icon=get_path("./bilibili.png")
    )

    # 侧栏设置
    with st.sidebar:
        st.header("🎁 B 站市集低价搜索")
        st.info(
            "制作不易，如果对你有帮助，请到 [Github](https://github.com/lmk123568/bilibili_bazaar_tool) 给我一颗星星吧！🌟"
        )

        with st.form(key="my_form"):
            # 添加一个按钮到表单

            category = st.selectbox("种类", ["手办", "模型", "周边", "3C"])

            price = st.slider("价格", 0.0, 200.0, (25.0, 75.0))

            discount = st.slider("折扣", 0.0, 10.0, (3.0, 5.0))

            request_interval = st.slider("请求时间间隔（秒）", 0.0, 15.0, (3.0))

            cookie = st.text_input("Cookie", placeholder="去集市抓包找 Cookie")
            st.write(
                "🔗 [B站集市链接](https://mall.bilibili.com/neul-next/index.html?page=magic-market_index)"
            )

            submitted = st.form_submit_button(
                label="搜索",
                type="primary",
                use_container_width=True,
                disabled=st.session_state["form_submit_button_visible"],
            )

    if submitted:
        if cookie:
            st.session_state["form_submit_button_visible"] = True
            with st.status("🌐 爬取集市数据中 ..."):

                response_json = st.empty()

                next_id = None
                result = []

                start_time = time.time()

                while 1:
                    response = get_product(category, price, discount, next_id, cookie)
                    response_json.json(response.json())
                    # extracted_data = [{key: item[key] for key in ('c2cItemsName', 'showPrice')} for item in response.json()['data']['data']]
                    # response_json.json(extracted_data)

                    if "data" not in response.json():
                        st.toast("好像被限流了，结果不全", icon="❗")
                        break

                    for i in response.json()["data"]["data"]:
                        item_data = {}
                        item_data["name"] = i["c2cItemsName"]
                        item_data["price"] = float(i["showPrice"])
                        item_data["market_price"] = float(i["showMarketPrice"])
                        item_data["discount"] = (
                            f"{(item_data['price'] / item_data['market_price'])*10:.1f} 折"
                        )
                        # item_data['img'] = 'https:'+i['detailDtoList'][0]['img']
                        item_data["url"] = (
                            "https://mall.bilibili.com/neul-next/index.html?page=magic-market_detail&noTitleBar=1&itemsId="
                            + str(i["c2cItemsId"])
                            + "&from=market_index"
                        )

                        result.append(item_data)

                    if response.json()["data"]["nextId"] == None:
                        break

                    next_id = response.json()["data"]["nextId"]

                    time.sleep(request_interval)

            end_time = time.time()

            st.success(
                f"Crawling Count: {len(result)}, Crawling Time: {(end_time - start_time)/60:.2f} min"
            )

            result_df = pd.DataFrame(result)

            min_price_df = result_df.groupby("name")["price"].idxmin()
            min_price_df = result_df.loc[min_price_df]

            min_price_df = pd.merge(
                min_price_df, result_df["name"].value_counts(), on="name", how="outer"
            )
            new_order = ["column1", "column2", "column3"]
            min_price_df = min_price_df.reindex(
                columns=["name", "count", "price", "market_price", "discount", "url"]
            )
            st.dataframe(
                min_price_df,
                column_config={
                    "name": st.column_config.TextColumn(label="物品"),
                    "count": st.column_config.TextColumn(
                        label="个数",
                        width="small",
                    ),
                    "price": st.column_config.TextColumn(
                        label="最低价",
                        width="small",
                    ),
                    "market_price": st.column_config.TextColumn(
                        label="原价",
                        width="small",
                    ),
                    "discount": st.column_config.TextColumn(
                        label="折扣",
                        width="small",
                    ),
                    "url": st.column_config.LinkColumn(
                        label="链接", width="small", display_text="Buy 🛒"
                    ),
                },
                hide_index=True,
            )
            st.session_state["form_submit_button_visible"] = False

        else:
            st.toast("请输入 Cookie", icon="❗")
