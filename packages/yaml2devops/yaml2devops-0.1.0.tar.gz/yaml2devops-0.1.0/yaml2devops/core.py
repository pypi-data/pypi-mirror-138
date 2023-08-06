import dataclasses
from typing import Iterable

import yaml
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication


@dataclasses.dataclass
class TestCase:
    name: str
    procedure: Iterable[str]
    expected_results: Iterable[str]


@dataclasses.dataclass
class TestSuite:
    name: str
    testcases: Iterable[TestCase]


def get_suite(test_yaml) -> TestSuite:
    with open(test_yaml) as test:
        parsed_yaml = yaml.safe_load(test)
        if "testcases" not in parsed_yaml:
            print("テストケースがありません")
        if "tests_suite_name" not in parsed_yaml:
            print("テストスイート名がありません")

        testcases = [_yaml_to_testcase(test_case) for test_case in parsed_yaml["testcases"]]
        return TestSuite(name=parsed_yaml["tests_suite_name"], testcases=testcases)


def gen_tasks(test_suite, org, project_id, pat):
    organization_url = f"https://dev.azure.com/{org}"

    # Create a connection to the org
    credentials = BasicAuthentication("", pat)
    connection = Connection(base_url=organization_url, creds=credentials)
    # クライアントの取得
    work_item_tracking_client = connection.clients.get_work_item_tracking_client()

    # ユーザーストーリーの作成
    create_user_story_command = [
        {"op": "add", "path": "/fields/System.Title", "from": None, "value": test_suite.name},
        {"op": "add", "path": "/fields/System.Description", "from": None, "value": test_suite.name},
    ]
    created_user_story = work_item_tracking_client.create_work_item(
        create_user_story_command, project_id, "User Story"
    )

    for test_case in test_suite.testcases:
        # タスクの作成
        test_description = (
            test_case.name
            + "<br><br>"
            + "# 手順 <br><br>- "
            + "<br>- ".join(test_case.procedure)
            + "<br><br>"
            + "# 期待結果"
            + "<br><br>- "
            + "<br>- ".join(test_case.expected_results)
        )
        create_task_command = [
            {"op": "add", "path": "/fields/System.Title", "from": None, "value": test_case.name},
            {"op": "add", "path": "/fields/System.Description", "from": None, "value": test_description},
        ]
        created_task = work_item_tracking_client.create_work_item(create_task_command, project_id, "Task")

        # ユーザーストーリとタスクの紐付け
        task_update_command = [
            {
                "op": "add",
                "path": "/relations/-",
                "value": {
                    "rel": "System.LinkTypes.Hierarchy-Reverse",
                    "url": f"https://dev.azure.com/{project_id}/_apis/wit/workItems/{str(created_user_story.id)}",
                },
            }
        ]
        work_item_tracking_client.update_work_item(task_update_command, created_task.id, project_id)


def _yaml_to_testcase(test_case) -> TestCase:
    return TestCase(name=test_case["テスト名"], procedure=test_case["手順"], expected_results=test_case["期待結果"])
