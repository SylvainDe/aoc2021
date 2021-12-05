import re
import datetime

header = """      --------Part 1--------   --------Part 2--------
Day       Time   Rank  Score       Time   Rank  Score"""
new_header = """      --------Part 1--------   --------Part 2--------  --------Delta--------
Day       Time   Rank  Score       Time   Rank  Score       Delta rank  Delta time"""


# From https://adventofcode.com/2021/leaderboard/self

stats = """
  3   08:16:54  54746      0   08:32:17  35746      0
  2   07:50:32  56717      0   07:52:32  53147      0
  1   07:35:16  44355      0   07:40:40  38014      0
"""


print(new_header)
time_re = r"([0-9:]+|>24h)"
stat_line_re = re.compile(
    r"^\s+(?P<day>\d+)\s+(?P<time1>%s)\s+(?P<rank1>\d+)\s+(?P<score1>\d+)\s+(?P<time2>%s)\s+(?P<rank2>\d+)\s+(?P<score2>\d+)$"
    % (time_re, time_re)
)
time_format = "%H:%M:%S"
for line in stats.split("\n"):
    if line:
        m = stat_line_re.match(line)
        d = m.groupdict()
        rank1 = int(d["rank1"])
        rank2 = int(d["rank2"])
        dtime1 = d["time1"]
        dtime2 = d["time2"]
        if dtime2 == ">24h":
            dtime2 = "23:59:59"
        time1 = datetime.datetime.strptime(dtime1, time_format)
        time2 = datetime.datetime.strptime(dtime2, time_format)
        delta_rank = rank1 - rank2
        delta_time = time2 - time1
        print("{}       {:5d}        {}".format(line, delta_rank, delta_time))