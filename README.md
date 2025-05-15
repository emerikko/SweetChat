# SweetChat 🤖🍬

**SweetChat** is a Telegram bot project designed to leverage AI for managing reminders, sending notifications, and engaging in user conversations. This project is an endeavor by **emerikko** to enhance skills in chatbot development, AI API integration, and Python backend development.

**Development Start Date:** 15.05.2025 (or actual start date)

## Table of Contents

1.  [Project Goal](#project-goal)
2.  [Priorities & MVP](#priorities--mvp)
3.  [Key Features](#key-features)
    * [MVP Features](#mvp-features)
    * [Post-MVP Features](#post-mvp-features)
4.  [Technology Stack](#technology-stack)
5.  [Functional Overview](#functional-overview)
    * [Reminder Management (Commands/Buttons)](#reminder-management-commandsbuttons)
    * [Reminder Management (AI)](#reminder-management-ai)
    * [Notifications](#notifications)
    * [Proactive AI Interaction](#proactive-ai-interaction)
6.  [Getting Started (Conceptual)](#getting-started-conceptual)
7.  [Project Roadmap](#project-roadmap)
8.  [Future Scope (Out of Current TS)](#future-scope-out-of-current-ts)
9.  [Author](#author)

## Project Goal

* To create a Telegram bot allowing users to interact with AI for setting reminders, receiving notifications, and general chat.
* To develop and refine skills in chatbot development, AI API utilization, and Python backend programming.
* (Optional) To create an accompanying website with similar functionality if time and interest permit.

## Priorities & MVP

The immediate focus is on delivering a **Minimum Viable Product (MVP)** with core reminder functionalities.

### MVP:
* Basic Telegram bot:
    * Create, view (upcoming), modify, and delete reminders using commands and UI buttons.
* Telegram notifications for due reminders.
* SQLite database for storing reminders.

### Post-MVP (in order of potential implementation):
1.  **AI Integration:** Natural language processing for reminder management.
2.  **View Past Reminders:** Functionality to see completed or missed reminders.
3.  **Basic Proactive AI:** Simple triggered messages (e.g., morning greeting with daily tasks).
4.  **(Optional)** Web interface development.
5.  **(Optional)** More complex proactive AI scenarios.
6.  **(Optional)** Synchronization of chat history between Telegram and the website.

## Key Features

### MVP Features:
* **Reminder CRUD:** Create, Read (upcoming), Update, Delete reminders via Telegram commands (e.g., `/createreminder`, `/myreminders`) and inline buttons.
* **Notifications:** Timely alerts in Telegram for set reminders.
* **Data Persistence:** Reminders saved locally using SQLite.

### Post-MVP Features:
* **Natural Language Reminder Management:** Create, modify, delete, and view reminders by chatting with the AI (e.g., "Remind me to call mom tomorrow at 10 AM").
* **Past Reminders:** Ability to view reminders that have already passed.
* **Proactive AI Messages:**
    * Optional morning/evening summaries of tasks.
    * User-configurable proactive messaging via `/settings`.
* **(Optional) Web Interface:** A simple, clean web UI with core bot functionalities.
* **(Optional) Chat Synchronization:** View chat history across Telegram and the (optional) website.

## Technology Stack

* **Backend:** Python (Libraries: `python-telegram-bot` or `aiogram`)
* **Database:** SQLite
* **AI:** Claude API (or a similar conversational AI API with context support)
* **(Optional Frontend for Website):** HTML, CSS (Bootstrap or similar), JavaScript

## Functional Overview

### Reminder Management (Commands/Buttons - MVP)
* `/createreminder`: Initiates a sequence to get Title, Date, and Time for a new reminder.
* `/myreminders`: Displays a list of upcoming reminders.
* Inline buttons for selecting reminders to modify or delete.
* Confirmation messages for all actions.

### Reminder Management (AI - Post-MVP)
* Users can type requests like:
    * "Remind me to buy milk tomorrow."
    * "What are my reminders for today?"
    * "Cancel my meeting on Friday."
* AI will parse, confirm, and act on these natural language requests.
* AI may ask clarifying questions if input is ambiguous.

### Notifications
* Sent directly to the user in Telegram at the reminder's specified time.
* Format: `[Reminder Title]. (If description exists: [Description])`.

### Proactive AI Interaction (Post-MVP)
* Optional, user-configurable messages (e.g., daily agenda).
* Advanced contextual interactions are a long-term consideration.

## Getting Started (Conceptual)

This project is currently in the planning/early development phase.
For future setup:
1.  Clone the repository.
2.  Create and activate a Python virtual environment.
3.  Install dependencies: `pip install -r requirements.txt` (file to be created).
4.  Set up environment variables for API keys:
    * `TELEGRAM_BOT_TOKEN`
    * `AI_API_KEY` (e.g., Claude API Key)
5.  Initialize the database.
6.  Run the main bot script: `python bot.py` (or similar).

## Project Roadmap

Development will be iterative:

* **Iteration 1 (MVP Telegram Bot):**
    * Environment setup & Telegram API connection.
    * CRUD for reminders (commands/buttons).
    * Notification system.
    * Basic logging.
* **Iteration 2 (AI Integration):**
    * Connect to AI API.
    * Implement natural language intent recognition for reminders.
    * Test and debug AI interactions.
* **Iteration 3 (Improvements & Optional Features):**
    * View "past" reminders.
    * Proactive messaging (if pursued).
    * (If decided) Begin web interface development.

*Timelines are flexible as this is a personal project developed in free time.*

## Future Scope (Out of Current TS)

Features not currently planned but could be considered later:
* Complex usage analytics.
* Multi-language support.
* Voice input/output.
* Integration with external calendars (e.g., Google Calendar).

## Author

* **emerikko**

---

*This README is based on the Technical Specification dated 15.05.2025. Also this README made by Gemini. I didn't write a thing to this*
