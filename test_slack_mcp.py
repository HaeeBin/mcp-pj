import pytest
import asyncio
from slack_api import (
    send_message, get_channels, 
    get_channel_history, send_direct_message,
    get_users, search_messages, upload_file,
    add_reaction
)

test_channel_id = "C1234567890"  # 예시 채널 ID
test_user_id = "U1234567890"     # 예시 사용자 ID
test_file_path = "./test_file.txt"  # 테스트용 파일 경로 


def test_send_slack_message():
    """Slack 채널에 메시지를 보내는 기능 테스트"""
    res = asyncio.run(send_message(test_channel_id, "✅ 테스트 메시지입니다."))
    assert res.get("ok") is True


def test_get_slack_channels():
    """채널 목록을 조회하는 기능 테스트"""
    res = get_channels()
    assert res.get("ok") is True
    assert "channels" in res

def test_get_slack_channel_history():
    """채널 메시지 히스토리를 조회하는 기능 테스트"""
    res = get_channel_history(test_channel_id, limit=5)
    assert res.get("ok") is True
    assert isinstance(res.get("messages"), list)

def test_send_slack_direct_message():
    """특정 사용자에게 DM을 보내는 기능 테스트"""
    res = asyncio.run(send_direct_message(test_user_id, "✅ DM 테스트입니다."))
    assert res.get("ok") is True

def test_list_workspace_users():
    """워크스페이스 사용자 목록 조회 테스트"""
    users = get_users()
    assert isinstance(users, list)
    assert len(users) > 0

def test_search_messages():
    """키워드 기반 메시지 검색 기능 테스트"""
    res = search_messages("테스트", count=3)
    assert res.get("ok") is True

def test_upload_file():
    """Slack 채널에 파일 업로드 기능 테스트"""
    with open(test_file_path, "w") as f:
        f.write("테스트 파일입니다.")

    result = upload_file(test_file_path, test_channel_id, title="테스트 파일")
    assert result.startswith("✅")

def test_add_reaction():
    """메시지에 이모지 반응 추가 기능 테스트 (가장 최근 메시지 기준)"""
    history = get_channel_history(test_channel_id, limit=1)
    assert history.get("ok") is True

    if not history["messages"]:
        pytest.skip("채널에 메시지가 존재하지 않음")

    ts = history["messages"][0]["ts"]
    res = add_reaction(test_channel_id, ts, "thumbsup")
    assert res.get("ok") is True