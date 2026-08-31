import os
  import sys
  from datetime import date, datetime, time, timedelta
  from zoneinfo import ZoneInfo

  from slack_sdk import WebClient
  from slack_sdk.errors import SlackApiError

  KST = ZoneInfo("Asia/Seoul")
  CHANNEL = "GG7PU8KFU"   # #ex 채널 ID (예약 목록 조회는 채널명이 아닌 ID가
  필요)
  SEND_AT = time(11, 0)      # 한국시간 오전 11시 정각 발송
  GRACE_HOURS = 2            # 11시가 이미 지났어도 이 시간 안이면 즉시 발송

  team_members = ["Lucy", "Bailey", "Claire", "Sayuri", "Evan", "Riley",
  "Silvia", "Jayla"]

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

  message = f"""{current_member}, 모든 구성원들이 업무에 온전히 행복하게 몰입할
  수 있는 환경을 만들어 나감으로써, 개인, 팀, 조직(회사)의 성장을 함께
  이루어내보아요💪

  ☝️구성원에게는 만났던 어떤 인사팀보다 나은 인사팀으로, 회사에는 성장의
  원동력으로 기억되는 팀

  ✌️'이 조직이 여기까지 온건 EX 팀 덕이 크다'는 말을 구성원들로 부터 듣는 팀

  🙌구성원의 70% 이상이 성장과 보상에 만족하는 회사로 만드는 팀

  🫶구직자들에게 '스푼랩스라면 한 번쯤 일해 보고 싶다'는 말을 듣는 회사로 만드는
  팀"""

  client = WebClient(token=os.environ["SLACK_TOKEN"])
  target = datetime.combine(today, SEND_AT, tzinfo=KST)
  post_at = int(target.timestamp())
