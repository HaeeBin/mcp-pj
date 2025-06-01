# Slack MCP Server

FastMCP를 활용한 Slack 통합 도구 서버입니다. Slack 메시지 전송, 채널/유저 조회, 메시지 검색, 반응 추가 기능을 제공합니다.

## 📁 프로젝트 구조

```
slack-mcp/
├── .env.example # 환경 변수 템플릿
├── slack_api.py # Slack API 기능 구현
├── slack_mcp_server.py # MCP 도구 등록 및 실행
├── requirements.txt # 의존성 목록
└── test_slack_mcp.py # 테스트 코드 (선택사항)
```

## ⚙️ 기능 소개

- **메시지 전송**: 채널 또는 유저에게 메시지를 보냅니다.
- **채널 조회**: 모든 채널 리스트를 가져옵니다.
- **메시지 조회**: 채널 히스토리 또는 검색 키워드를 통해 메시지를 가져옵니다.
- **유저 조회**: 워크스페이스 유저 목록을 확인할 수 있습니다.
- **이모지 반응 추가**: 특정 메시지에 반응을 남깁니다.

## 🚀 실행 방법

### 1. 필요한 Bot Token Scopes
- 다음 권한들을 Bot Token Scopes에 추가해야 합니다.

```
channels:read        # 채널 목록 조회
channels:history     # 채널 메시지 히스토리 조회
chat:write          # 메시지 전송
im:read             # DM 채널 읽기
im:write            # DM 메시지 전송
im:history          # DM 히스토리 조회
users:read          # 사용자 정보 조회
groups:read         # 비공개 채널 정보 조회
groups:history	    # 비공개 채널 메시지 조회
mpim:history	    # 그룹 DM 메시지 조회
reactions:read	    # 이모지 반응 조회
reactions:write	    # 이모지 반응 추가/수정
search:read.enterprise	# 콘텐츠 검색 (선택 기능용)
users:read	        # 사용자 정보 조회
```

#### Bot Token Scopes 설정 방법
1. 앱 설정 페이지에서 "OAuth & Permissions" 메뉴 선택
2. "Scopes" 섹션의 "Bot Token Scopes"에서 "Add an OAuth Scope" 클릭
3. 위의 권한들을 하나씩 추가
4. "Install App to Workspace" 버튼 클릭
5. 권한 승인 후 **Bot User OAuth Token** 복사 및 저장

<br>

### 2. 환경 변수 설정
- `.env` 파일을 프로젝트 루트에 생성하고 아래와 같이 작성하세요:

```
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_USER_TOKEN=xoxp-your-user-token-here
```
<br>

### 3. 의존성 설치:

```bash
pip install -r requirements.txt
```
<br>

### 4. 서버 실행:

```bash
python slack_mcp_server.py
```
<br>

## 🧪 테스트 실행

```bash
python test_slack_mcp.py
```



