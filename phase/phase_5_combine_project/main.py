from dotenv import load_dotenv

from notion_utils.relate_databases_to_one.relate_databases_to_one_update import *

load_dotenv()


def main():
    # 要匯集的資料庫ID
    combination_database_C_id = os.getenv("PHASE_5_COMBINATION_DATABASE_C_ID")
    # 目標資料庫ID群
    target_databases_A_id = os.getenv("PHASE_4_TARGET_DATABASE_A_ID")
    target_databases_B_id = os.getenv("PHASE_4_TARGET_DATABASE_B_ID")
    target_database_list = []
    target_database_list.append(target_databases_A_id)
    target_database_list.append(target_databases_B_id)
    target_database_list.append("205b82c9b09480a79deaec0b8c3a6369")
    # 更新匯集資料庫欄位
    for target_database in target_database_list:
        response = add_new_relate_database_property(target_database, combination_database_C_id)
        if response: print("✅ 資料庫連結標題成功！Database ID:", response["id"])
    print("請務必目標資料庫不要重名字，不然無法新增上去")
    # -------------------------------------------------------------------------------
    # 確定匯集資料庫格式正確
    update_standard_database_property(combination_database_C_id)
    print("✅ 所有欄位確定已建立完畢。如果將欄位改名將會重新新增正確欄位名，並保留您改名的")
    # 更新匯集資料庫資訊
    update_all_target_database_to_combi(target_database_list, combination_database_C_id)


if __name__ == "__main__":  # 只有這個.py檔案被執行的時候main中的程式才會執行 ("__name__"是"__檔案名__")
    main()
