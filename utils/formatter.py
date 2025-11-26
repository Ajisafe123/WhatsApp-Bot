def format_reminders(reminders):
    if not reminders:
        return "No reminders set."
    
    lines = ["📝 Your Reminders:\n"]
    for i, r in enumerate(reminders, 1):
        time_str = r.remind_time.strftime("%I:%M %p")
        lines.append(f"{i}. {r.task} - ⏰ {time_str}")
    
    return "\n".join(lines)