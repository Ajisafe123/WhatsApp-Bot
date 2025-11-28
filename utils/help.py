def get_help() -> str:
    header = "📘 *Help Menu — What I Can Do*"

    intro = (
        "I'm your Reminder & Productivity Assistant.\n"
        "Here are the things you can ask me to help you with:"
    )

    examples = (
        "\n\n🕒 *Set Reminders*\n"
        "• “Remind me to read by 10 PM”\n"
        "• “In 20 minutes remind me to check the food”\n"
        "• “Remind me to pray every day at 6 AM”\n"
        "• “Every 2 hours remind me to drink water”"
    )

    management = (
        "\n\n📋 *Manage Reminders*\n"
        "• “Show my reminders”\n"
        "• “Delete reminder 1”"
    )

    advanced = (
        "\n\n⚙️ *Advanced Commands*\n"
        "• “Remind me every day for 5 days at 8 AM”\n"
        "• “Remind me every 15 minutes for 2 hours”"
    )

    closing = (
        "\n\n✨ You can type naturally — I’ll understand.\n"
        "Type *help* anytime to see this menu again."
    )

    return f"{header}\n\n{intro}{examples}{management}{advanced}{closing}"
