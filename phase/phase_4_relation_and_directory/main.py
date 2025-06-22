from dotenv import load_dotenv

from phase.phase_4_relation_and_directory.relate_database import update_all_target_database_to_combi
from search_database import *

# 選擇目標資料庫群(本次資料已經新建好)
load_dotenv()

target_databases_A_id = os.getenv("PHASE_4_TARGET_DATABASE_A_ID")
target_databases_B_id = os.getenv("PHASE_4_TARGET_DATABASE_B_ID")
combination_database_C_id = os.getenv("PHASE_4_COMBINATION_DATABASE_C_ID")

target_database_list = [target_databases_A_id, target_databases_B_id]

# response = connect_new_relate_database(target_databases_A_id, combination_database_C_id)
# if response: print_response(response)
# if response: print("✅ 新增資料庫連結標題成功！Database ID:", response["id"])
#
# response = connect_new_relate_database(target_databases_B_id, combination_database_C_id)
# if response: print("✅ 新增資料庫連結標題成功！Database ID:", response["id"])

# 更新資料庫們合併到C
update_all_target_database_to_combi(target_database_list, combination_database_C_id)
