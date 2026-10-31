---
name: university-calendar
description: Create or update Google Calendar events for the user's university studies at the Open University of Israel (האוניברסיטה הפתוחה, Opal) - course meetings (מפגשים), assignments (מטלות), and exams (מבחנים) when the user asks - in one uniform format. Use whenever the user asks to add, change, fix, recolor or review university-related calendar events, sets up a new semester, or sends a screenshot of an Opal page. First collects the needed course details from the user.
---

# University calendar events

The user studies at the Open University of Israel and keeps every course meeting and assignment deadline in Google Calendar. Every semester they repeat the same setup for new courses, so this skill makes the result identical each time: same titles, same descriptions, one color per course. Reply to the user in Hebrew.

## Scope

- **Meetings (מפגשים) and assignments (מטלות):** set up at the start of a semester, updated when Opal changes something.
- **Exams (מבחנים):** the user does not know exam dates in advance. Do not ask about exams when setting up a semester. Add them only when the user brings the details, using the exam format below.
- **Any other change** to these events (moving one, recoloring, fixing a title) follows the same conventions, even when it is a single event.
- **Not part of this skill:** semester-level dates such as registration opening or semester end. Leave those events alone.

## Tools

Use the Google Calendar connector (`mcp__Google_Calendar__*`: `list_calendars`, `list_events`, `search_events`, `create_event`, `update_event`, `delete_event`). If they are deferred, load them first with ToolSearch.

Before the first write, run `list_calendars` and confirm the primary calendar is the user's personal one, not a work account. The connector can be linked to a different account (once it was a work account). If it is not the personal one, stop and tell the user instead of writing there.

## 1. Look the course up first

For every request about a course, however small (adding one assignment, fixing a date, recoloring), start by searching the calendar for the course. Do this before asking the user anything about it.

- Search by course number with `list_events` (`fullText` = the number) or `search_events`. `list_events` defaults to the next 7 days, so always pass an explicit range that covers the current semester only (the semester named in the request or screenshots; if unsure, ask the user for its start and end dates). The number appears in the description of events made by this skill (`מספר קורס: 20441`) and in the title of the user's older meeting events (`(20441)`). Also search by the course name when you know it. Names are mostly unique, so either the number or the name can find the course; if the user gives only the name, search by the name alone.
- From what you find, reuse it instead of asking:
  - **Color:** the `colorId` those events already use. If they use different colors, tell the user and ask which to keep.
  - **Links** (course page and assignments page): the URLs in the existing descriptions.
  - **Full course name** and the meetings' **location**.
- **Current semester only:** use only events inside the current semester's date range. Take nothing from earlier semesters (no color, name, links or location), even if the same course appeared before. A course with no events this semester is a new course.
- In the plan, say what you reused ("found in the calendar: color, links, course name") so the user can correct it.
- No match this semester means a new course: ask for everything in step 2 and pick a color from the Colors section.

## 2. Collect the inputs

After the lookup, ask for everything that is still missing in one Hebrew message, before building anything. Do not ask for what the lookup already gave you, and do not fill gaps from memory or from earlier semesters. The user usually answers with screenshots of Opal pages, which is fine, but read them carefully.

For each course:

1. **Full name, course number and semester** (the header of the Opal course page, e.g. "20441 - מבוא למדעי המחשב ושפת Java", semester 2027א).
2. **Links:** the course page (`https://opal.openu.ac.il/course/view.php?id=<id>`) and the course's assignments page (`https://opal.openu.ac.il/mod/ouilassign/index.php?id=<id>&quicklinks=1`). In the two courses so far both links used the same id, so if the user gives only one you may build the other, but say you did and ask them to confirm.
3. **Assignments:** a screenshot of the assignments page ("מטלות הקורס") showing, for each assignment, its number, type (מטלה מקוונת / מטלת קובץ / מטלה מקדמת השתתפות ...), start date, due date (תאריך אחרון להגשה) and status (הוגשה / טרם הוגש). If the list is long, ask for all of it.
4. **Meetings:** the schedule is not always weekly. The user will often send a screenshot of the university's calendar that shows the date and time of each meeting. Read every meeting from it. Also accept a typed list or a simple pattern ("every Wednesday 18:00-20:00 until 27/01"). For each meeting you need the date, the start and end time, and the location (the Java course used "מקוון"). If a screenshot is unclear or cut off, ask instead of guessing. If the calendar numbers the meetings or gives them a topic, tell the user and ask whether to put that in the title or description (default: no). If there is a meeting link, ask whether it should go in the location field or the description.

Ask, never decide silently, about these (every semester, naming the specific assignments concerned; past answers varied):

- Assignments already submitted (הוגשה): include or skip?
- Participation-promoting assignments (מטלה מקדמת השתתפות): include or skip?

## 3. Check before writing

- Use the lookup from step 1: update events that already exist instead of creating duplicates.
- Opal dates are DD/MM/YYYY. If two screenshots disagree, use the newer one and tell the user.
- Due dates often fall on Saturday. That is normal for this university, not an error.
- Course color: reuse the one found in step 1. For a new course, first list the semester's events to see which colors the other courses use, then pick per the Colors section.
- For bulk work (more than about 3 events), first write out the full plan in Hebrew: every event with its title, date(s) and color name, plus the open questions above. Wait for approval. For a single event, just do it and report.

## 4. Event format

Common to every event:

- **Title:** `<type> <number> · <full course name>`. The type and number come first because the phone calendar cuts off the end of long titles. The course name is complete and does not include the course number. Separator is " · ". No emoji. Examples: `מטלת קובץ 05 · מבוא למדעי המחשב ושפת Java`, `מטלה מקוונת 07 · מתמטיקה קדם אקדמית`, `מפגש · מתמטיקה קדם אקדמית`. Use Opal's own wording for the type, and keep the two-digit numbers as Opal shows them.
- **Color:** the course's color on all of its events (meetings, assignments, exams).
- **Description:** plain text only. The user's phone shows HTML tags literally, so no `<br>`, no `<a>`, no Markdown; use real line breaks. The link sits alone on its own line, with no other text on that line. Labels do not mention "Opal".
- Leave timeZone unset, leave reminders at the defaults, no attendees.

### Assignments

All-day events, availability free (`AVAILABILITY_FREE`).

- **File assignments (מטלת קובץ)**, and any assignment whose window is longer than 7 days or opens at the start of the semester: a single all-day event on the due date.
- **Online assignments (מטלה מקוונת)** whose start-to-due window is 7 days or less: one multi-day all-day event from the start date through the due date. The end date in the tool is exclusive, so end = due date + 1 day. Example: window 10/11-14/11 means `startTime` 2026-11-10T00:00:00 and `endTime` 2026-11-15T00:00:00.

Description:

```
מספר קורס: <number>
דף המטלות של הקורס:
<assignments page URL>
```

### Meetings

First list every meeting you read (date, weekday, start-end time, location) and have the user confirm the list as part of the plan. When the source is a screenshot, this is where misreads get caught.

Then choose the shape from the actual schedule:

- **Regular schedule** (same weekday and time on a fixed interval, possibly with a few skipped weeks): one recurring series per course. Use `create_event` with `recurrenceData`, e.g. `RRULE:FREQ=WEEKLY;BYDAY=WE;UNTIL=20270127T235959Z` (UNTIL = last meeting date; add `INTERVAL=2` for every other week). For skipped weeks add `EXDATE` entries (e.g. `EXDATE;TZID=Asia/Jerusalem:20261118T180000`), then check with `list_events` that exactly those dates are absent.
- **Irregular schedule** (varying weekdays, times or gaps, or locations that differ between meetings): one separate event per meeting, all with the same title, description and color.
- If most meetings follow a pattern and one or two differ, you may use a series for the regular ones and single events for the exceptions. When in doubt between the two shapes, say which one you chose and why in the plan.

All meeting events are busy (the default). The location field holds the room, or "מקוון" for online, set per meeting when it differs. `update_event` cannot change a recurrence rule. If a series' rule has to change, tell the user and recreate the series.

Description:

```
מספר קורס: <number>
דף הקורס:
<course page URL>
```

### Exams

Only when the user brings exam details. Ask for whatever is missing: course, date, start time, duration, location, and the sitting (מועד א / ב ...).

- Title: `מבחן · <course>`, with the sitting before the course if known: `מבחן מועד א · <course>`.
- Timed event with start and end, busy, location in the location field. If the time is not known yet: all-day, free, and "שעה: טרם נקבעה" in the description.
- Description: course number, sitting, time, location, then `דף הקורס:` and the link on its own line.

## Colors

One color per course, identical on all of its events. A course that already has events this semester keeps its color (step 1). For a new course, choose the one that feels intuitive for the subject, make sure two courses in the same semester never share a color, and tell the user which color you picked (by name, in the plan).

For two courses of the same subject, use a neighboring color.

Google Calendar `colorId`s (pass the number in `colorId`):

| colorId | Name | Looks like |
|---|---|---|
| 1 | Lavender | light purple |
| 2 | Sage | light green |
| 3 | Grape | purple |
| 4 | Flamingo | pink |
| 5 | Banana | yellow |
| 6 | Tangerine | orange |
| 7 | Peacock | teal-blue |
| 8 | Graphite | gray |
| 9 | Blueberry | deep blue |
| 10 | Basil | dark green |
| 11 | Tomato | red |

## 5. After writing

- **Verify** with `list_events` over the semester's range (filter by the course number): count, dates, titles, colors, and that the description has the link alone on its own line. Fix mismatches before reporting.
- **Report** in Hebrew, briefly: what was created or updated per course, what was skipped and why, any choice you made that the user did not specify, and conflicts you noticed (a meeting overlapping another calendar event, due dates of two courses on the same day). Do not recap the steps.

## Updating existing events

When Opal changes a date, find the event (type and number in the title, course number in the description) and update that event instead of creating a new one. Send only the changed fields. The description holds no dates, so a date change touches only the event itself. Remember that the end of an all-day event is exclusive.
