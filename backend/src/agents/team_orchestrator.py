from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import BaseGroupChat, SelectorGroupChat

from .company_policy_agent import get_company_policy_agent
from .hotel_search_agent import get_hotel_search_agent
from .planner_agent import get_planner_agent
from .summary_agent import get_summary_agent
from .transport_cost_agent import get_transport_cost_agent


def get_team(model_client) -> BaseGroupChat:
    condition = TextMentionTermination("TERMINATE") | MaxMessageTermination(15)

    hotel_search_agent = get_hotel_search_agent(model_client)
    planner_agent = get_planner_agent(model_client)
    summary_agent = get_summary_agent(model_client)
    transport_cost_agent = get_transport_cost_agent(model_client)
    company_policy_agent = get_company_policy_agent(model_client)

    return SelectorGroupChat(
        participants=[
            company_policy_agent,
            hotel_search_agent,
            planner_agent,
            summary_agent,
            transport_cost_agent,
        ],
        model_client=model_client,
        termination_condition=condition,
        allow_repeated_speaker=False,
        selector_prompt="""あなたのタスクは、会話の状況に応じて次のタスクを実行する role を選択することです。
## 次の role の選択ルール

各 role の概要以下です。

{roles}

次のタスクに選択可能な participants は以下です。

{participants}

以下のルールに従って、次の role を選択してください。

- 会話履歴を確認し、次の会話に最適な role を選択します。role name のみを返してください。
- role は1つだけ選択してください。
- 他の role が作業を開始する前に、"PlannerAgent" にタスクを割り当て、サブタスクを計画してもらうことが必要です。
- PlannerAgent はサブタスクの計画のみを行います。サブタスクの作業を依頼してはいけません。
- PlannerAgent が計画したサブタスクに応じて、role を選択します。
- タスクを完了するための必要な情報が揃ったと判断したら "SummaryAgent" に最終回答の作成を依頼します。

## 会話履歴

{history}
""",
    )
