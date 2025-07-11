import os

import requests
from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool

API_URL = os.environ.get("ADD_INVENTORY_ENDPOINT")


def get_company_policy_info(question: str) -> str:
    body = {"question": question}
    response = requests.post(url=API_URL, json=body)
    return response.text


def get_company_policy_agent(model_client) -> AssistantAgent:
    company_policy_tool = FunctionTool(
        get_company_policy_info,
        name="company_policy_tool",
        description="会社の規程 (正社員や正社員以外の就業規則, 出張旅費, 賃金, 退職金, 福利厚生, 特定個人情報取扱など) に関連する情報を取得できるツール",
    )

    return AssistantAgent(
        name="CompanyPolicyAgent",
        description="会社の規程 (正社員や正社員以外の就業規則, 出張旅費, 賃金, 退職金, 福利厚生, 特定個人情報取扱など) に関連する質問に回答するエージェント",
        model_client=model_client,
        tools=[company_policy_tool],
        system_message="""tool: company_policy_tool を使用して会社の規程を調べ、質問に回答することができます。
主に以下に関する質問に回答ができます。

- "出張旅費規程": 出張旅費(目的, 適用範囲, 留意事項,  出張の区分, 出張旅費の構成, 出張の区分による出張旅費の支給基準, 出張申請・仮払い, 出張報告・旅費の清算, 旅費の分担, 出張中の傷病・災害, 出発・帰着の場所, 交通手段, 日当, 交通費, 宿泊費, 研修費, その他費用, 外貨建て旅費の円換算, 旅費の減額・不支給)
- "就業規則": 総則(目的, 従業員の定義, 適用範囲, 規則遵守の義務), 服務(服務規律, 営業秘密・個人情報の管理, 通勤方法, 兼業の届出), 人事(採用, 採用選考, 内定取消事由, 採用時の提出書類, 試用期間, 正社員への転換, 派遣社員からの採用, 労働条件の明示, 人事異動, 休職, 休職期間, 復職), 定年、退職及び解雇(定年, 退職, 解雇, 解雇の予告, 解雇の制限), 労働時間、休憩及び休日(所定労働時間, 始業・終業の時刻及び休憩時間, フレックスタイム制, 専門業務型裁量労働制, 出張時の勤務時間及び旅費, 欠勤・遅刻・早退・私用外出, 休日, 休日の振替, 時間外・休日労働, 時間外・休日労働の事前承認, 代休, 適用除外), 休暇及び休業(年次有給休暇, 採用時特別休暇, 慶弔休暇, 産前産後の休業, 母性健康管理のための休暇等, 育児・介護休業、子の看護休暇等, 育児時間, 生理休暇, 公民権行使等休暇), 賃金及び退職金(賃金・賞与, 退職金, 出張旅費), 福利厚生(福利厚生), 懲戒(懲戒の種類, けん責、減給、出勤停止又は降職, 諭旨解雇又は懲戒解雇, 損害賠償), 教育(教育訓練), 安全衛生及び労災補償(遵守義務, 健康診断, 安全衛生教育, 災害補償), 知的財産(職務発明)
- "特定個人情報取扱規程": 総則(目的, 適用範囲, 定義, 利用目的, 会社が行う個人番号関係事務の範囲, 特定個人情報責任者, 事務取扱担当者), 特定個人情報の取扱い(安全管理の原則, 遵守事項, 教育研修, 個人番号の提供および収集, 本人確認), 保管及び廃棄等(情報の開示と訂正, 特定個人情報の廃棄, 特定個人情報の外部提供), 危機管理(危機管理対応, 危機管理対応, 懲戒及び損害賠償, 苦情・相談窓口, 法令との関係, 改廃)
- "特定個人情報取扱規程補足資料 保存期間": 本書について(（参考）特定個人情報の廃棄), 国税関係(法定の保管義務, 対応), 雇用保険関係(法定の保管義務, 対応), 労災保険関係(法定の保管義務, 対応), 社会保険関係(法定の保管義務, 対応)
- "短時間正社員 就業規則": 総則(目的, 適用範囲), 人事(利用事由, 雇用契約期間, 常勤正社員への復帰), 労働時間、始業就業の時刻、休憩時間および休日(労働時間, 時間外労働, 始業・終業の時刻, 休憩時間, 休日), 賃金・賞与・退職金(賃金, 賞与, 退職金), その他(年次有給休暇, 社会保険・労働保険の加入)
- "賃金規程": 総則(目的, 適用範囲, 賃金の構成, 賃金の支払と控除, 賃金計算期間及び支払日, 端数処理, 昇給・降給, 賃金請求権の時効, 手当の届け出及び不正受給), 正社員の賃金(本章の適用範囲, 賃金の支払形態, 基本給, 職能給, 業務手当, 役職手当, 通勤手当, 住宅手当, 所定外労働手当, 賃金の日割り計算, 休職・休暇・欠勤等による賃金の減額), 臨時社員及び嘱託社員の賃金(本章の適用範囲, 賃金の支払形態, 基本給, 職能給, 業務手当, 役職手当, 通勤手当, 住宅手当, 所定外労働手当, 休職・休暇・欠勤等による賃金の減額), 賞与(賞与の支給, 計算対象期間, 賞与の決定)
- "退職金規程": 総則(目的, 退職金の支給範囲), 退職金共済(退職金共済契約, 退職金共済契約の時期, 掛金, 掛金の納付停止, 退職金の額, 退職金の減額, 退職金の支給方法)
- "福利厚生規程": 福利厚生(目的, 適用範囲, 不正受給, 慶弔見舞金, 社内懇親会補助, 書籍購入補助, セミナー補助, 予防接種補助)
    """,
    )
