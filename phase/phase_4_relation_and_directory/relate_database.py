from search_database import *
import os

#連接增加新的連接欄位
def connect_new_relate_database(new_target_databases_id, combination_database_id):#只選擇一個資料庫，所以要先生成才能用比較不複雜

#將選擇集合資料庫建立連動欄(已建立簡單格式，需要建立那是其他的方法，但是新家資料庫要加上)。
#簡單格式:資料名稱|連動資料庫A|連動資料庫B...
    new_property_title = get_database_title(new_target_databases_id)
    print("new_property_title:", new_property_title)
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    if property_exists(combination_database_id, new_property_title):
        print("資料庫標題'%s'已存在於欄位中無法加入總表，請更改資料庫標題" % new_property_title)
        return get_database_response(combination_database_id)
    response = notion.databases.update(
        database_id = combination_database_id,
        properties = {
            new_property_title: {
                "type": "relation",
                "relation": {
                    "database_id": new_target_databases_id,
                    "type": "single_property",
                    "single_property": {
                    }
                }
            }
        }
    )
    print("新欄位新增成功, 新欄位名稱:", new_property_title)
    return response
#-----------------------------------------------------------------------------------
#控制-掃描所有子database更新總database
def update_all_target_database_to_combi(target_databases_id_list, combination_database_id):
    target_databases_title_list = []
    for target_database_id in target_databases_id_list:
        update_single_target_database_to_combi(target_database_id, combination_database_id)
        # 整理出target_database_title_list
        target_databases_title_list.append(get_database_title(target_database_id))
    print("全部目標資料庫合併完畢")

    delete_no_relation_pages(combination_database_id, target_databases_title_list)
    print("全部目標資料庫清理完畢")
    print("全部任務完成")
#控制-掃描所有pages更新總database
def update_single_target_database_to_combi(target_databases_id, combination_database_id):
    pages_id = get_page_id_list(target_databases_id)
    target_database_title = get_database_title(target_databases_id)
    for page_id in pages_id:
        update_page_to_combi(page_id, combination_database_id, target_database_title, target_databases_id)
    print("資料庫%s合併完畢" % target_database_title)

#選擇-掃描單個pages更新總database
def update_page_to_combi(page_id, combination_database_id, target_database_title, target_database_id):
    title_property = get_title_property_name(target_database_id)
    if not is_page_id_in_combi_relation_id(page_id, combination_database_id, target_database_title):
        add_new_page_helper(page_id, combination_database_id, target_database_title, title_property)
        print("頁面:%s，已同步新增完畢" % get_page_title(page_id, title_property))
    else: #原本找對應了但都刪掉了怎麼找對應->每次自動刪除沒有連結任何page的
        # if is_page_archived(page_id):
        #     target_delete_page_id = page_id
        #     combi_delete_page_id = get_combi_page_id(target_delete_page_id, combination_database_id)
        #     delete_page(combi_delete_page_id)
        #     print("頁面:%s，已同步清除完畢" % get_page_title(page_id, title_property))
        # else:
        print("更新部分是下一階段，所以頁面:%s，並無更新" % get_page_title(page_id, title_property))

#回傳-回傳一個database中所有page_id的list
def get_page_id_list(database_id):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))

    all_page_ids = []

    response = notion.databases.query(database_id=database_id)
    #API最多一次查找100筆資料，如果有需求要使用START_CURSOR
    for page in response["results"]:
        all_page_ids.append(page["id"])
    print("以回傳%d筆pages" % len(all_page_ids))
    return all_page_ids

#判斷-有無這個relation?
def is_page_id_in_combi_relation_id(page_id, combination_database_id, target_database_title):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))

    response = notion.databases.query(database_id=combination_database_id)

    for page in response["results"]:  # 資料庫為空的話會結束回圈，設定上只會有一個對應的id所以不太可能隊到同一個
        if not page["properties"][target_database_title]["relation"] == []:
            if page_id == page["properties"][target_database_title]["relation"][0]["id"]:
                print("目標ID: %s對應ID: %s，此ID已存在，將不會新增頁面" % (page_id, page["id"]))  # 有對應到
                return True
    print("目標ID: %s沒有對應頁面，將會新增頁面" % page_id)
    return False

#判斷-有無被封存?
# def is_page_archived(page_id):
#     notion = Client(auth=os.getenv("NOTION_TOKEN"))
#     response = notion.pages.retrieve(page_id=page_id)
#     if response["archived"]:
#         return True
#     else:
#         return False

#判斷-有無其他更新?
# def is_page_change(page_id):
#     pass

#功能-新增一個page
def add_new_page(page_id, database_id, database_title_property_name, database_relation_property_name, title_property):
    page_title = get_page_title(page_id, title_property)
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    notion.pages.create(
        parent={"database_id": database_id},
        properties = {
            database_title_property_name: {
                "type": "title",
                "title": [
                    {
                        "text": {"content": page_title}
                    }
                ]
            },
            database_relation_property_name: {
                "type": "relation",
                "relation": [
                    {
                        "id" : page_id
                    }
                ]
            }
        }
    )
#補件-用於找出property_title和property_relation的名稱
def add_new_page_helper(page_id, database_id, target_database_title, title_property):
    database_title_property_name = get_title_property_name(database_id)
    database_relation_property_name = target_database_title
    add_new_page(page_id, database_id, database_title_property_name, database_relation_property_name, title_property)

#功能-刪除一個page
def delete_page(page_id):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    notion.pages.update(
        page_id=page_id,
        archived = True
    )

def delete_no_relation_pages(combination_database_id, relation_property_name_list):
    pages_id_list = get_page_id_list(combination_database_id)
    notion = Client(auth=os.getenv("NOTION_TOKEN"))

    for page_id in pages_id_list:
        delete = True
        for relation_property_name in relation_property_name_list:
            response = notion.pages.retrieve(page_id=page_id)
            if response["properties"][relation_property_name]["relation"]:
                delete = False
        if delete:
            delete_page(page_id)




# #回傳-回傳target_page_id對應的combi_page_id
# def get_combi_page_id(target_page_id, combination_database_id):
#     notion = Client(auth=os.getenv("NOTION_TOKEN"))
#
#     response = notion.databases.query(database_id=combination_database_id)
#
#     for page in response["results"]:# 只會有一個依樣的
#         if target_page_id == page["properties"]["relation"][0]["id"]:
#             print("目標ID: %d找到對應ID: %d" % (target_page_id, page["id"]))
#             return page["id"]
#     print("目標ID: %d沒有對應頁面")
#     return -1


#其他更新(下一階段)





