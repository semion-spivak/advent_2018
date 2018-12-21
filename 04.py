from collections import defaultdict as dd, Counter
from re import compile
from datetime import datetime

pattern = compile(r"^\[(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (?:Guard #(?P<guard_id>\d+) begins shift|(?P<action>falls asleep|wakes up))$")

def parse_ts(ts):
    return datetime.strptime(ts, '%Y-%m-%d %H:%M')

with open('04.in', 'r') as f:
    log = f.readlines()
    log.sort()
    # print(log[:10])
    current_guard = None
    fall_asleep_time = None
    asleep = False

    guard_time_table = dd(Counter)

    for line in log:
        match = pattern.match(line).groupdict()
        gid = match.get('guard_id')
        if gid:
            current_guard = int(gid)
            asleep = False
            fall_asleep_time = None
            continue
        action = match.get('action')
        if action == 'falls asleep':
            asleep = True
            fall_asleep_time = parse_ts(match['ts'])
        elif action == 'wakes up' and asleep:
            wake_up_time = parse_ts(match['ts'])
            guard_time_table[current_guard].update(range(fall_asleep_time.minute, wake_up_time.minute))

    
    results = {}
    most_sleepy_gid = None
    max_sleeped_minutes = 0
    for gid, cntr in guard_time_table.items():
        sleeped_minutes = len(list(cntr.elements()))
        if sleeped_minutes > max_sleeped_minutes:
            max_sleeped_minutes = sleeped_minutes
            most_sleepy_gid = gid
    m, c = guard_time_table[most_sleepy_gid].most_common(1)[0]
    print(f"part 1: {most_sleepy_gid*m}")

    result = {}
    for gid, cntr in guard_time_table.items():
        m, c = cntr.most_common(1)[0]
        result[c] = (gid, m)
    print(f"part 2: {int.__mul__(*result[max(result.keys())])}")
