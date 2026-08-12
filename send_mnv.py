import os
from datetime import date, datetime, timedelta, timezone
from slack_sdk import WebClient

# 1. 팀원 목록을 순서대로 적어줍니다.
team_members = ["Lucy", "Bailey", "Riley", "Claire", "Evan", "Silvia", "Sayuri", "Jayla"]

# 2. 한국 시간(KST) 기준으로 오늘 날짜를 가져옵니다. (GitHub 서버는 UTC를 쓰기 때문에 +9시간 필요)
kst_now = datetime.now(timezone.utc) + timedelta(hours=9)
today = kst_now.date()

# 3. 로테이션 기준일 (2026년 8월 10일 월요일을 A의 차례로 기준 잡음)
anchor_date = date(2026, 8, 10)

# 4. 기준일부터 오늘까지 '주말을 제외하고' 며칠이 지났는지 계산
days_diff = (today - anchor_date).days
weekdays_count = 0

for i in range(days_diff):
    d = anchor_date + timedelta(days=i)
    if d.weekday() < 5: # 0:월, 1:화, 2:수, 3:목, 4:금 (토/일 제외)
        weekdays_count += 1

# 5. 전체 인원수(8명)로 나눈 나머지 값을 이용해 오늘의 담당자를 구합니다.
current_member = team_members[weekdays_count % len(team_members)]

# 6. 메시지 내용 작성 및 전송
client = WebClient(token=os.environ["SLACK_TOKEN"])
message = f"""{current_member}, 모든 구성원들이 업무에 온전히 행복하게 몰입할 수 있는 환경을 만들어 나감으로써, 개인, 팀, 조직(회사)의 성장을 함께 이루어내보아요💪

구성원에게는 만났던 어떤 인사팀보다 나은 인사팀으로, 회사에는 성장의 원동력으로 기억되는 팀

이 조직이 여기까지 온건 EX 팀 덕이 크다'는 말을 구성원들로 부터 듣는 팀

구성원의 70% 이상이 성장과 보상에 만족하는 회사로 만드는 팀

구직자들에게 '스푼랩스라면 한 번쯤 일해 보고 싶다'는 말을 듣는 회사로 만드는 팀""""

client.chat_postMessage(
    channel="#ex",
    text=message
)
