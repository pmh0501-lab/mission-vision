import os
import sys
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

KST = ZoneInfo("Asia/Seoul")
CHANNEL = "GG7PU8KFU"   # #ex 채널 ID (예약 목록 조회는 채널명이 아닌 ID가 필요)
SEND_AT = time(11, 0)      # 한국시간 오전 11시 정각 발송
GRACE_HOURS = 2            # 11시가 이미 지났어도 이 시간 안이면 즉시 발송
EARLY_CRON = "0 18 * * 0-4"  # 새벽 3시(KST) 실행분. 지각 발송은 이 실행분에 허용하지 않는다

team_members = ["Lucy", "Bailey", "Claire", "Sayuri", "Evan", "Riley", "Silvia", "Jayla"]

now = datetime.now(KST)
today = now.date()

# 1) 주말이면 아무것도 하지 않는다
if today.weekday() >= 5:
    print(f"[skip] 주말({today})이라 발송하지 않습니다.")
    sys.exit(0)

# 2) 오늘 담당자 계산 (기준일부터 오늘까지의 평일 수로 순번을 돌림)
anchor_date = date(2026, 8, 10)
weekdays_count = 0
for i in range((today - anchor_date).days):
    d = anchor_date + timedelta(days=i)
    if d.weekday() < 5:
        weekdays_count += 1
current_member = team_members[weekdays_count % len(team_members)]

message = f"""{current_member}, 모든 구성원들이 업무에 온전히 행복하게 몰입할 수 있는 환경을 만들어 나감으로써, 개인, 팀, 조직(회사)의 성장을 함께 이루어내보아요💪

☝️구성원에게는 만났던 어떤 인사팀보다 나은 인사팀으로, 회사에는 성장의 원동력으로 기억되는 팀

✌️'이 조직이 여기까지 온건 EX 팀 덕이 크다'는 말을 구성원들로 부터 듣는 팀

🙌구성원의 70% 이상이 성장과 보상에 만족하는 회사로 만드는 팀

🫶구직자들에게 '스푼랩스라면 한 번쯤 일해 보고 싶다'는 말을 듣는 회사로 만드는 팀"""

client = WebClient(token=os.environ["SLACK_TOKEN"])
target = datetime.combine(today, SEND_AT, tzinfo=KST)
post_at = int(target.timestamp())

# 3) 이미 오늘 11시로 예약해둔 게 있으면 중복 발송하지 않는다
#    (새벽 3시 실행분과 아침 8시 예비 실행분이 겹치는 것을 막는 장치)
try:
    scheduled = client.chat_scheduledMessages_list(
        channel=CHANNEL, oldest=post_at - 60, latest=post_at + 60
    )
    if scheduled.get("scheduled_messages"):
        print(f"[skip] 이미 {target:%Y-%m-%d %H:%M} 발송으로 예약되어 있습니다.")
        sys.exit(0)
except SlackApiError as e:
    # 예약 목록 조회에 실패해도 발송 자체는 계속 진행한다
    print(f"[warn] 예약 목록 확인 실패({e.response['error']}). 그대로 진행합니다.")

# 4) 아직 11시 전이면 슬랙에 예약을 걸어둔다 (GitHub이 늦게 돌아도 11시 정각 발송)
if now < target:
    client.chat_scheduleMessage(channel=CHANNEL, post_at=post_at, text=message)
    print(f"[scheduled] {target:%Y-%m-%d %H:%M} KST / {current_member}")
    sys.exit(0)

# 5) 11시가 지났을 때의 지각 발송
#    두 실행분이 모두 11시를 넘겨 깨어나면 같은 메시지가 두 번 나갈 수 있다.
#    (예약 목록 확인은 '아직 안 나간 예약'만 걸러내므로 이미 발송된 건 못 막는다)
#    그래서 지각 발송은 뒤쪽 실행분(아침 8시)과 수동 실행에서만 허용한다.
if os.environ.get("SCHEDULE_CRON", "") == EARLY_CRON:
    print(f"[skip] 11시가 지났습니다. 새벽 실행분은 지각 발송을 하지 않습니다. ({current_member} 차례)")
    sys.exit(0)

if now < target + timedelta(hours=GRACE_HOURS):
    client.chat_postMessage(channel=CHANNEL, text=message)
    print(f"[sent-late] {now:%H:%M} KST에 즉시 발송 / {current_member}")
    sys.exit(0)

# 6) 너무 늦었으면 보내지 않는다 (밤에 메시지가 나가는 것을 방지)
print(f"[skip] 지금은 {now:%H:%M} KST. 너무 늦어 발송하지 않습니다. ({current_member} 차례)")
