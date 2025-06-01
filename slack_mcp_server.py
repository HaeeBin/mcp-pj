from fastmcp import FastMCP
from slack_api import (
    send_message, get_channels, 
    get_channel_history, send_direct_message,
    get_users,
    search_messages, add_reaction
)
import asyncio

# MCP 인스턴스 및 Slack API 클라이언트 생성
mcp = FastMCP("slack-mcp-server")

# 도구 등록
@mcp.tool()
async def send_slack_message(channel: str, text: str) -> str:
    """
    지정된 Slack 채널에 메시지를 전송합니다.

    Args:
        channel : 채널 ID 또는 이름
        text (str): 전송할 메시지 내용

    Returns:
        str: 성공 또는 오류 메시지
    """
    res = await send_message(channel, text)
    return "메시지 전송 성공" if res.get("ok") else f"오류: {res.get('error')}"

    
    
@mcp.tool()
def get_slack_channels() -> list:
    """
    접근 가능한 모든 Slack 채널 목록을 조회합니다.

    Returns:
        list: 채널 ID, 이름, 공개/비공개 여부, 멤버십 상태 포함
    """
    res = get_channels()
    return res.get("channels", []) if res.get("ok") else f"오류: {res.get('error')}"


@mcp.tool()
def get_slack_channel_history(channel_id: str, limit: int = 10) -> list:
    """
    지정한 채널의 최근 메시지 히스토리를 조회합니다.

    Args:
        channel_id (str): 채널 ID
        limit (int): 조회할 메시지 수 (기본: 10)

    Returns:
        list: 메시지 내용, 작성자, 타임스탬프 리스트 또는 오류 메시지
    """
    res = get_channel_history(channel_id, limit)
    return res.get("messages", []) if res.get("ok") else f"오류: {res.get('error')}"

@mcp.tool()
async def send_slack_direct_message(user_id: str, text: str) -> str:
    """
    특정 사용자에게 1:1 다이렉트 메시지를 전송합니다.

    Args:
        user_id (str): 사용자 ID
        text (str): 전송할 메시지 내용

    Returns:
        str: 성공 또는 오류 메시지
    """
    res = await send_direct_message(user_id, text)
    return "메시지 전송 성공" if res.get("ok") else f"오류: {res.get('error')}"

@mcp.tool()
async def list_workspace_users() -> str:
    """
    워크스페이스의 사용자 목록을 조회합니다.

    Returns:
        str: 사용자 리스트 문자열 또는 오류 메시지
    """
    users = get_users()

    if not users or "error" in users[0]:
        return f"❌ 사용자 조회 실패: {users[0].get('error')}"

    formatted = []
    for user in users:
        if user.get("deleted"):  # 비활성화된 사용자 제외
            continue
        name = user.get("profile", {}).get("real_name", user.get("name", "이름 없음"))
        user_id = user.get("id", "ID 없음")
        formatted.append(f"👤 {name} (ID: {user_id})")

    return "\n".join(formatted)

@mcp.tool()
async def search_slack_messages(query: str, count: int = 10) -> list:
    """
    Slack에서 키워드를 포함한 메시지를 검색합니다.

    Args:
        query (str): 검색 키워드
        count (int): 검색 결과 수 (기본값: 10)

    Returns:
        list: 간략화된 메시지 검색 결과 리스트
    """
    res = search_messages(query, count)
    if not res.get("ok"):
        return [f"❌ 검색 실패: {res.get('error')}"]

    matches = res.get("messages", {}).get("matches", [])
    return [
        {
            "user": match.get("username"),
            "text": match.get("text"),
            "channel": match.get("channel", {}).get("name"),
            "timestamp": match.get("ts"),
            "permalink": match.get("permalink")
        }
        for match in matches
    ]

@mcp.tool()
async def add_slack_reaction(channel: str, timestamp: str, emoji_name: str) -> str:
    """
    지정한 Slack 메시지에 이모지 반응을 추가합니다.

    Args:
        channel (str): 채널 ID
        timestamp (str): 메시지의 ts 값
        emoji_name (str): 이모지 이름

    Returns:
        str: 성공 또는 실패 메시지
    """
    res = add_reaction(channel, timestamp, emoji_name)
    return f"✅ '{emoji_name}' 반응 추가 성공" if res.get("ok") else f"❌ 반응 추가 실패: {res.get('error')}"

# 실행
if __name__ == "__main__":
    mcp.run("stdio")