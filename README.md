# SweetChat 🤖💬

**Telegram Bot for AI-Assisted Reminders, Notifications, and Chat**

It's just a start. Not even alpha. There's nothing

---

## 📌 Project Overview

**Project Name:** SweetChat  
**Developer & Author:** emerikko  
**Development Start Date:** 15.05.2025  

SweetChat is a powerful and user-friendly Telegram bot designed to assist users with:

- 📅 Creating and managing reminders
- 🔔 Sending timely notifications
- 🧠 Engaging in natural language AI conversations

> *(Optional)* A web-based companion app may also be developed to mirror the functionality of the Telegram bot.

---

## 🎯 Project Goals

- Build an AI-integrated Telegram bot for enhanced productivity and interaction.
- Gain experience in chatbot development, AI API integration, and Python backend systems.
- Optionally, create a web interface that syncs with Telegram bot functionality.

---

## 🚀 Features

### 📝 Reminders

- **Create Reminder:**  
  Use `/createreminder`, buttons, or natural language to set reminders. Required: date, time, title. Optional: importance, description.
  - If a duplicate time is detected, reminders are merged.
  - Confirmation messages are sent after creation.

- **Edit Reminder:**  
  Change any aspect (date, time, title, description) via command or AI chat.

- **Delete Reminder:**  
  Remove reminders using commands, buttons, or natural language.

- **View Reminders:**  
  Open a menu to view "Past Reminders" or "Upcoming Reminders".

### 🤖 AI-Initiated Messaging

- AI can initiate conversations or remind users based on schedule.
- Interaction points are updated dynamically.
- Users may disable this feature if preferred.

### 🌐 (Optional) Web Companion

- Sync chat and reminders between Telegram bot and website.
- Fully responsive and compatible with Chrome, Firefox, Safari.

---

## 🧩 Tech Stack

### 💻 Backend
- **Language:** Python
- **Framework:** [aiogram](https://docs.aiogram.dev/)
- **Database:** SQLite

### 🧠 AI
- **Model:** Claude or other Model Context Protocol-compatible AI

### 🌐 Frontend *(Optional Website)*
- **Framework:** Bootstrap *(subject to change)*

### 📡 APIs
- Telegram Bot API
- AI Provider API
- *(Optional)* REST API for website integration

---

## ⚙️ System Requirements

- **Performance:**  
  - Commands processed within 250ms.  
  - AI replies display "AI is thinking..." message during delay.

- **Security:**  
  - Protection against major vulnerabilities.  
  - Secure storage of user data.

- **Testing:**  
  - Unit tests for backend logic  
  - Integration tests for API endpoints

- **Data Logging:**  
  - All actions (except casual chat) are saved and logged.  
  - All errors are logged server-side.

---

## 🧪 Testing

- 🧩 Unit Tests: For core logic
- 🔄 Integration Tests: For API and AI communication
- 🛡️ Security and Data Handling: Audited through logs and test cases

---

## 📄 Documentation & Timeline

- Work stages and development deadlines are **TBD**.
- This README will be updated accordingly as milestones are set.

---

## 📬 Contributing

Interested in contributing? Feel free to fork this repository, submit issues, or propose enhancements. Collaboration is welcome!

---

**Made with 💙 by emerikko**
