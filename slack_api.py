import os
import httpx
from dotenv import load_dotenv
import json
import requests

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_USER_TOKEN = os.getenv("SLACK_USER_TOKEN")

user_headers = {
        "Authorization": f"Bearer {SLACK_USER_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }
headers = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    "Content-Type": "application/json; charset=utf-8"
}
file_headers = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    "Content-Type": "application/json"  # ✅ charset=utf-8 없이
}


async def send_message(channel: str, text: str) -> dict:
    """
    Slack 채널에 메시지를 전송합니다. (UTF-8 인코딩 지원)

    Args:
        channel : 메시지를 보낼 채널 ID 또는 이름
        text : 전송할 메시지 내용

    Returns:
        dict: Slack API 응답 결과
    """
    url = "https://slack.com/api/chat.postMessage"
    payload = {"channel": channel, "text": text}
    
    # httpx를 사용하여 UTF-8 인코딩 보장
    async with httpx.AsyncClient() as client:
        res = await client.post(
            url, 
            headers=headers, 
            content=json.dumps(payload, ensure_ascii=False).encode('utf-8')
        )
    
    return res.json()

def get_channels() -> dict:
    """
    Slack 워크스페이스 내 접근 가능한 모든 채널 목록을 조회합니다.

    Returns:
        dict: 채널 정보 리스트를 포함한 응답
    """
    url = "https://slack.com/api/conversations.list"
    res = requests.get(url, headers=headers)
    return res.json()


def get_channel_history(channel_id: str, limit: int = 10) -> dict:
    """
    지정된 채널의 최근 메시지 히스토리를 조회합니다.

    Args:
        channel_id : 조회할 채널의 ID
        limit : 조회할 메시지 수 (기본값: 10)

    Returns:
        dict: 메시지 리스트를 포함한 응답
    """
    url = "https://slack.com/api/conversations.history"
    params = {"channel": channel_id, "limit": limit}
    res = requests.get(url, headers=headers, params=params)
    return res.json()


async def send_direct_message(user_id: str, text: str) -> dict:
    """
    특정 사용자에게 다이렉트 메시지를 전송합니다.

    Args:
        user_id : 대상 사용자 ID
        text : 전송할 메시지 내용

    Returns:
        dict: DM 채널 생성 및 메시지 전송 결과
    """
    # 1. DM 채널 열기
    url_open = "https://slack.com/api/conversations.open"
    payload = {"users": user_id}

    async with httpx.AsyncClient() as client:
        res_open = await client.post(
            url_open,
            headers=headers,
            json=payload  # ✅ json으로 전송
        )
        res_open_data = res_open.json()
        if not res_open_data.get("ok"):
            return {"error": f"❌ DM 채널 열기 실패: {res_open_data.get('error')}"}

        channel_id = res_open_data["channel"]["id"]

        # 2. 메시지 전송
        url_message = "https://slack.com/api/chat.postMessage"
        msg_payload = {"channel": channel_id, "text": text}
        res_msg = await client.post(
            url_message,
            headers=headers,
            json=msg_payload
        )

        return res_msg.json()

def get_users() -> list:
    """
    워크스페이스의 사용자 목록을 조회합니다.

    Returns:
        list: 사용자 정보 객체 목록 또는 오류 정보
    """
    url = "https://slack.com/api/users.list"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return [{"error": f"요청 실패 - {response.status_code}"}]

    data = response.json()
    if not data.get("ok"):
        return [{"error": f"Slack API 오류 - {data.get('error')}"}]

    return data.get("members", [])

def search_messages(query: str, count: int = 10) -> dict:
    """
    지정된 키워드로 Slack 메시지를 검색합니다.

    Args:
        query : 검색 키워드
        count : 최대 검색 결과 수

    Returns:
        dict: 검색 결과 응답
    """
    url = "https://slack.com/api/search.messages"
    params = {"query": query, "count": count}
    res = requests.get(url, headers=user_headers, params=params)
    return res.json()

def get_channel_id_by_name(channel_name: str) -> str:
    """
    채널 이름으로부터 해당 채널 ID를 조회합니다.

    Args:
        channel_name (str): 채널 이름 또는 ID (예: "#general")

    Returns:
        str: 채널 ID 또는 None
    """
    url = "https://slack.com/api/conversations.list"
    res = requests.get(url, headers=headers)
    if not res.ok:
        return None

    clean_name = channel_name.lstrip("#")

    for channel in res.json().get("channels", []):
        if channel.get("name") == clean_name:
            return channel.get("id")

    # 만약 channel_name이 이미 ID일 경우
    if channel_name.startswith("C") and len(channel_name) > 8:
        return channel_name

    return None

    
def add_reaction(channel: str, timestamp: str, emoji_name: str) -> dict:
    """
    특정 메시지에 이모지 반응을 추가합니다.

    Args:
        channel : 채널 ID
        timestamp : 메시지의 timestamp (ts)
        emoji_name : 추가할 이모지 이름 (예: "thumbsup")

    Returns:
        dict: Slack API 응답
    """
    url = "https://slack.com/api/reactions.add"
    payload = {
        "channel": channel,
        "timestamp": timestamp,
        "name": emoji_name
    }
    res = requests.post(url, headers=headers, json=payload)
    return res.json()