import math
import msvcrt
import time
import winsound

# ---------- MATPLOTLIB ----------
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt


def get_total_study_time():
    while True:
        try:
            total_minutes = float(input("Enter TOTAL study time (in minutes): "))
            if total_minutes > 0:
                return total_minutes

            print("Please enter a study time greater than 0.")

        except ValueError:
            print("Please enter a valid number.")


def is_back_reply(reply):
    cleaned_reply = reply.strip().upper()
    return cleaned_reply == "I'M BACK" or cleaned_reply == "I'M BACKKK"


def wait_until_user_returns():
    print("\nBreak time is over!")
    print("Type I'M BACK and press Enter to continue studying.")
    print("Reminder beep will continue until you return.\n")

    typed_text = ""
    break_end_time = time.time()
    last_beep_time = 0

    while True:
        current_time = time.time()

        if current_time - last_beep_time >= 1.2:
            winsound.Beep(2000, 700)
            last_beep_time = time.time()

        if msvcrt.kbhit():
            char = msvcrt.getwch()

            if char in ("\r", "\n"):
                print()

                if is_back_reply(typed_text):
                    delay = round((time.time() - break_end_time) / 60, 2)
                    print("\nWelcome back! Continuing study session...")
                    return delay

                print("\nRETURN BACK TO STUDY!")
                print("Type I'M BACK and press Enter to continue studying.\n")
                typed_text = ""

            elif char == "\b":
                if typed_text:
                    typed_text = typed_text[:-1]
                    print("\b \b", end="", flush=True)

            else:
                typed_text += char
                print(char, end="", flush=True)

        time.sleep(0.05)


def create_study_plan(total_minutes):
    # Dynamic formula:
    # 1. Session size grows gradually as total time increases.
    # 2. Breaks are calculated as a percentage of study time.
    # 3. Every fourth break becomes a longer recovery break.
    base_cycle_minutes = 25
    cycle_growth = math.sqrt(total_minutes)
    target_cycle_minutes = base_cycle_minutes + cycle_growth

    total_sessions = max(1, round(total_minutes / target_cycle_minutes))
    long_break_after_sessions = 4

    short_break_units = 0
    long_break_units = 0

    for session in range(1, total_sessions + 1):
        has_more_sessions = session < total_sessions

        if has_more_sessions and session % long_break_after_sessions == 0:
            long_break_units += 1
        else:
            short_break_units += 1

    short_break_ratio = 0.18
    long_break_ratio = 0.45

    study_session = total_minutes / (
        total_sessions
        + (short_break_units * short_break_ratio)
        + (long_break_units * long_break_ratio)
    )

    short_break_time = study_session * short_break_ratio
    long_break_time = study_session * long_break_ratio

    rounded_study = round(study_session)
    rounded_short_break = round(short_break_time)
    rounded_long_break = round(long_break_time)
    rounded_plan_total = (
        (total_sessions * rounded_study)
        + (short_break_units * rounded_short_break)
        + (long_break_units * rounded_long_break)
    )

    if rounded_plan_total == round(total_minutes):
        study_session = rounded_study
        short_break_time = rounded_short_break
        long_break_time = rounded_long_break

    break_sessions = []

    for session in range(1, total_sessions + 1):
        has_more_sessions = session < total_sessions

        if has_more_sessions and session % long_break_after_sessions == 0:
            break_sessions.append(("Long Break", long_break_time))
        else:
            break_sessions.append(("Short Break", short_break_time))

    return total_sessions, study_session, break_sessions

# ---------- INTRO ----------
print("=" * 65)
print("           SMART POMODORO STUDY TRACKER")
print("=" * 65)

# ---------- USER INPUT ----------
total_study_time = get_total_study_time()

# ---------- SMART SESSION GENERATION ----------
total_sessions, study_session, planned_breaks = create_study_plan(total_study_time)
short_breaks = [minutes for break_type, minutes in planned_breaks if break_type == "Short Break"]
long_breaks = [minutes for break_type, minutes in planned_breaks if break_type == "Long Break"]

print("\nSmart Study Plan Generated")
print(f"Total Sessions     : {total_sessions}")
print(f"Study Session Time : {study_session:.2f} mins")
if short_breaks:
    print(f"Short Break Time   : {short_breaks[0]:.2f} mins")
if long_breaks:
    print(f"Long Break Time    : {long_breaks[0]:.2f} mins")
print(f"\n{total_sessions} study session(s) will be conducted.")

for index, (break_type, break_minutes) in enumerate(planned_breaks, start=1):
    print(f"Session {index}: {study_session:.2f} mins study + {break_minutes:.2f} mins {break_type.lower()}")

# ---------- CONVERSION ----------
total_seconds = round(total_study_time * 60)
study_seconds = round(study_session * 60)

# ---------- DATA ----------
study_sessions = []
break_sessions = []
short_break_sessions = []
long_break_sessions = []
late_returns = []

completed_study = 0
session_number = 1

# ---------- MAIN LOOP ----------
while session_number <= total_sessions:

    print("\n" + "=" * 65)
    print(f"              SESSION {session_number} OF {total_sessions}")
    print("=" * 65)

    current_session = study_seconds

    print("\nStudy session started!")
    print("Stay focused...\n")

    start_time = time.time()

    # ---------- STUDY TIMER ----------
    for remaining in range(current_session, 0, -1):

        mins = remaining // 60
        secs = remaining % 60

        timer = f"{mins:02d}:{secs:02d}"

        print(f"Study Time Left: {timer}", end="\r")

        time.sleep(1)

    end_time = time.time()

    actual_study = round((end_time - start_time) / 60, 2)

    study_sessions.append(actual_study)

    completed_study += current_session

    winsound.Beep(1000, 1000)

    print("\n\nStudy session completed!")

    # ---------- BREAK TIMER ----------
    break_type, current_break_time = planned_breaks[session_number - 1]
    break_seconds = round(current_break_time * 60)

    print(f"\n{break_type} Started!")
    print("Relax for a while...\n")

    for remaining in range(break_seconds, 0, -1):

        mins = remaining // 60
        secs = remaining % 60

        timer = f"{mins:02d}:{secs:02d}"

        print(f"Break Time Left: {timer}", end="\r")

        time.sleep(1)

    break_sessions.append(current_break_time)

    if break_type == "Short Break":
        short_break_sessions.append(current_break_time)
    else:
        long_break_sessions.append(current_break_time)

    # ---------- RETURN CHECK ----------
    delay = wait_until_user_returns()
    late_returns.append(delay)

    if delay > 0.1:
        print(f"\nYou returned late by {delay:.2f} mins")

    # ---------- IF ALL SESSIONS FINISHED ----------
    if session_number >= total_sessions:
        break

    session_number += 1

# ---------- ANALYTICS ----------
total_study = sum(study_sessions)
total_break = sum(break_sessions)
total_short_break = sum(short_break_sessions)
total_long_break = sum(long_break_sessions)

late_time = sum(late_returns)

total_time = total_study + total_break + late_time

productivity = (total_study / total_time) * 100

# ---------- PERFORMANCE ----------
if productivity >= 85:
    performance = "Excellent"

elif productivity >= 70:
    performance = "Good"

else:
    performance = "Needs Improvement"

# ---------- FINAL REPORT ----------
print("\n" + "=" * 65)
print("                     FINAL REPORT")
print("=" * 65)

print(f"Total Study Time     : {total_study:.2f} mins")
print(f"Total Break Time     : {total_break:.2f} mins")
print(f"Short Break Time     : {total_short_break:.2f} mins")
print(f"Long Break Time      : {total_long_break:.2f} mins")
print(f"Late Return Time     : {late_time:.2f} mins")
print(f"Productivity Score   : {productivity:.2f}%")
print(f"Performance          : {performance}")

# ---------- PIE CHART ----------
labels = ["Study", "Short Break", "Long Break", "Late Return"]
values = [total_study, total_short_break, total_long_break, late_time]

plt.figure(figsize=(7, 7))

plt.pie(
    values,
    labels=labels,
    autopct='%1.1f%%'
)

plt.title("Time Utilization Analysis")

plt.show()

# ---------- BAR GRAPH ----------
categories = ["Productivity"]
scores = [productivity]

plt.figure(figsize=(6, 5))

plt.bar(categories, scores)

plt.ylim(0, 100)

plt.ylabel("Percentage")
plt.title("Productivity Score")

plt.show()

# ---------- PRODUCTIVITY TREND ----------
session_labels = []

for i in range(1, len(study_sessions) + 1):
    session_labels.append(f"S{i}")

plt.figure(figsize=(8, 5))

plt.plot(session_labels, study_sessions, marker='o')

plt.ylabel("Study Time")
plt.xlabel("Sessions")
plt.title("Study Session Growth")

plt.show()

# ---------- FINAL MESSAGE ----------
print("\n" + "=" * 65)

if productivity >= 85:
    print("Outstanding focus and time management!")

elif productivity >= 70:
    print("Good productivity! Keep improving consistency.")

else:
    print("Try reducing delays after breaks.")

print("=" * 65)
