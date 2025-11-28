def get_greeting(name: str = None) -> str:
    user_name = name.split()[0] if name else "there"

    greet = f"👋 Hello {user_name}, welcome."

    intro = (
        "I'm your intelligent Reminder & Productivity Assistant. "
        "My role is to help you stay organized, manage tasks, and set reminders with ease."
    )

    menu = (
        "\n\nYou can get started by sending messages like:\n"
        "• “Remind me to review my notes at 3 PM”\n"
        "• “In 15 minutes, remind me to stretch”\n"
        "• “Set a daily reminder to practice coding at 9 PM”\n"
        "• “Show my reminders” or “Delete reminder 2”"
    )

    closing = (
        "\n\nFeel free to type naturally! You can also type `help` for more advanced examples. Ready to organize your day? 🗓️"
    )

    return f"{greet}\n{intro}{menu}{closing}"