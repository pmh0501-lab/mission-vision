import os
from datetime import date, datetime, timedelta, timezone
from slack_sdk import WebClient
team_members = ["Lucy", "Bailey", "Claire", "Sayuri", "Evan", "Riley", "Silvia", "Jayla"]
kst_now = datetime.now(timezone.utc) + timedelta(hours=9)
today = kst_now.date()
anchor_date = date(2026, 8, 10)
days_diff = (today - anchor_date).days
weekdays_count = 0
for i in range(days_diff):
    d = anchor_date + timedelta(days=i)
    if d.weekday() < 5: weekdays_count += 1
current_member = team_members[weekdays_count % len(team_members)]

client = WebClient(token=os.environ["SLACK_TOKEN"])
# 여기에 아까 작성하신 5줄짜리 멋진 메시지를 넣으세요!
message = f"""{current_member}, 모든 구성원들이 업무에 온전히 행복하게 몰입할 수 있는 환경을 만들어 나감으로써, 개인, 팀, 조직(회사)의 성장을 함께 이루어내보아요💪

☝️구성원에게는 만났던 어떤 인사팀보다 나은 인사팀으로, 회사에는 성장의 원동력으로 기억되는 팀

✌️이 조직이 여기까지 온건 EX 팀 덕이 크다'는 말을 구성원들로 부터 듣는 팀

🙌구성원의 70% 이상이 성장과 보상에 만족하는 회사로 만드는 팀

🫶구직자들에게 '스푼랩스라면 한 번쯤 일해 보고 싶다'는 말을 듣는 회사로 만드는 팀""" 

client.chat_postMessage(channel="#ex", text=message)
