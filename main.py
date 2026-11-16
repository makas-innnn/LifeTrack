import flet as ft
import json
import datetime
import platform
import os
import asyncio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "lifetrack_data.json")

TEXTS = {
    "ru": {
        "app_title": "LifeTrack", "habits": "Привычки", "notes": "Заметки", "finance": "Финансы", "info": "Инфо",
        "habit_name": "Название привычки...", "note_title": "Заголовок", "note_text": "Текст заметки...",
        "expense_name": "На что потратил?", "expense_amount": "Сумма",
        "income_name": "Откуда доход?", "income_amount": "Сумма",
        "type_income": "Доход", "type_expense": "Расход",
        "cat_food": "Еда", "cat_transport": "Транспорт", "cat_fun": "Развлечения", 
        "cat_bad": "Вредное", "cat_other": "Другое", "cat_salary": "Зарплата", "cat_gift": "Подарок",
        "save": "Добавить", "delete": "Удалить", "balance": "Баланс:",
        "top_cat": "Больше всего потрачено на:",
        "about_me": "Начинающий кодер, делаю что в кайф",
        "tg_channel": "Телеграм-канал:", "tg_dm": "Связь (ЛС):", "gh": "GitHub:",
        "copy_logs": "Скопировать логи", "logs_copied": "Логи скопированы!",
        "clear_data": "Очистить все данные", "confirm_del": "Удалить запись?", "yes": "Да", "no": "Нет",
        "filter_all": "Все", "filter_today": "Сегодня", "filter_week": "Неделя", "filter_month": "Месяц",
        "confirm_clear": "Вы уверены, что хотите удалить ВСЕ данные? Это действие нельзя отменить.",
        "support_btn": "Написать в поддержку", "support_copied": "✅ Скопировано!"
    },
    "en": {
        "app_title": "LifeTrack", "habits": "Habits", "notes": "Notes", "finance": "Finance", "info": "Info",
        "habit_name": "Habit name...", "note_title": "Title", "note_text": "Note text...",
        "expense_name": "What for?", "expense_amount": "Amount",
        "income_name": "Source of income?", "income_amount": "Amount",
        "type_income": "Income", "type_expense": "Expense",
        "cat_food": "Food", "cat_transport": "Transport", "cat_fun": "Fun", 
        "cat_bad": "Bad", "cat_other": "Other", "cat_salary": "Salary", "cat_gift": "Gift",
        "save": "Add", "delete": "Delete", "balance": "Balance:",
        "top_cat": "Most spent on:",
        "about_me": "Beginner coder, doing what I love",
        "tg_channel": "Telegram channel:", "tg_dm": "Contact (DM):", "gh": "GitHub:",
        "copy_logs": "Copy logs", "logs_copied": "Logs copied!",
        "clear_data": "Clear all data", "confirm_del": "Delete record?", "yes": "Yes", "no": "No",
        "filter_all": "All", "filter_today": "Today", "filter_week": "Week", "filter_month": "Month",
        "confirm_clear": "Are you sure you want to delete ALL data? This cannot be undone.",
        "support_btn": "Contact Support", "support_copied": "✅ Copied!"
    }
}

THEMES = {
    "dark": {"bg": ft.Colors.SURFACE, "card": ft.Colors.SURFACE_CONTAINER_HIGHEST},
    "light": {"bg": ft.Colors.WHITE, "card": ft.Colors.GREY_200},
    "purple": {"bg": ft.Colors.DEEP_PURPLE_900, "card": ft.Colors.DEEP_PURPLE_800},
    "forest": {"bg": ft.Colors.GREEN_900, "card": ft.Colors.GREEN_800}
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"habits": [], "notes": [], "expenses": []}

def save_data_to_file(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except: pass

def main(page: ft.Page):
    page.title = "LifeTrack"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK

    loaded_data = load_data()
    state = {
        "lang": "ru", "theme": "dark", 
        "habits": loaded_data.get("habits", []), 
        "notes": loaded_data.get("notes", []), 
        "expenses": loaded_data.get("expenses", []),
        "filter": "all"
    }

    def save_data():
        save_data_to_file({
            "habits": state["habits"], 
            "notes": state["notes"], 
            "expenses": state["expenses"]
        })

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def confirm_delete(callback, item):
        def on_yes(e):
            callback(item)
            close_dialog(dialog)
        
        dialog = ft.AlertDialog(
            title=ft.Text(TEXTS[state["lang"]]["confirm_del"]),
            actions=[
                ft.TextButton(TEXTS[state["lang"]]["yes"], on_click=on_yes),
                ft.TextButton(TEXTS[state["lang"]]["no"], on_click=lambda e: close_dialog(dialog))
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # --- ВКЛАДКА 1: ПРИВЫЧКИ ---
    habits_col = ft.Column(spacing=10)
    habit_input = ft.TextField(hint_text=TEXTS[state["lang"]]["habit_name"], expand=True)
    
    def add_habit(e):
        if habit_input.value:
            state["habits"].append({"name": habit_input.value, "last_done": "", "streak": 0, "date": datetime.datetime.now().strftime("%d.%m")})
            habit_input.value = ""
            update_habits_ui()
            save_data()
            page.update()

    def toggle_habit(index):
        h = state["habits"][index]
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if h["last_done"] == today:
            h["last_done"] = ""
            h["streak"] = max(0, h["streak"] - 1)
        else:
            h["last_done"] = today
            h["streak"] += 1
        update_habits_ui()
        save_data()
        page.update()

    def delete_habit(item):
        state["habits"].remove(item)
        update_habits_ui()
        save_data()
        page.update()

    def update_habits_ui():
        habits_col.controls.clear()
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        for i, h in enumerate(state["habits"]):
            is_done = (h["last_done"] == today)
            habits_col.controls.append(
                ft.Row([
                    ft.Checkbox(value=is_done, on_change=lambda e, i=i: toggle_habit(i)),
                    ft.Column([
                        ft.Text(h["name"], size=16, color=ft.Colors.GREY_300 if is_done else ft.Colors.WHITE),
                        ft.Text(f'Создано: {h["date"]}', size=10, color=ft.Colors.GREY_500)
                    ], expand=True),
                    ft.Text(f'🔥 {h["streak"]}', size=14, color=ft.Colors.ORANGE_400),
                    ft.IconButton(ft.Icons.DELETE, icon_size=16, icon_color=ft.Colors.RED_400, on_click=lambda e, h=h: confirm_delete(delete_habit, h))
                ])
            )

    tab_habits = ft.Column([
        ft.Text("🏠 Привычки", size=24, weight=ft.FontWeight.BOLD),
        ft.Row([habit_input, ft.IconButton(ft.Icons.ADD, on_click=add_habit, bgcolor=ft.Colors.BLUE_400, icon_color=ft.Colors.WHITE)]),
        habits_col
    ], scroll=ft.ScrollMode.AUTO, expand=True)

    # --- ВКЛАДКА 2: ЗАМЕТКИ ---
    notes_col = ft.Column(spacing=10)
    note_title_input = ft.TextField(hint_text=TEXTS[state["lang"]]["note_title"])
    note_text_input = ft.TextField(hint_text=TEXTS[state["lang"]]["note_text"], multiline=True, min_lines=2)

    def add_note(e):
        if note_title_input.value or note_text_input.value:
            state["notes"].append({
                "title": note_title_input.value, "text": note_text_input.value,
                "date": datetime.datetime.now().strftime("%d.%m %H:%M")
            })
            note_title_input.value = ""
            note_text_input.value = ""
            update_notes_ui()
            save_data()
            page.update()

    def delete_note(item):
        state["notes"].remove(item)
        update_notes_ui()
        save_data()
        page.update()

    def update_notes_ui():
        notes_col.controls.clear()
        for n in reversed(state["notes"]):
            notes_col.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(n["title"], size=16, weight=ft.FontWeight.BOLD, expand=True),
                            ft.Text(n["date"], size=12, color=ft.Colors.GREY_500),
                            ft.IconButton(ft.Icons.DELETE, icon_size=16, icon_color=ft.Colors.RED_400, on_click=lambda e, n=n: confirm_delete(delete_note, n))
                        ]),
                        ft.Text(n["text"], size=14, color=ft.Colors.GREY_400)
                    ]),
                    padding=10, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=10
                )
            )

    tab_notes = ft.Column([
        ft.Text("📝 Заметки", size=24, weight=ft.FontWeight.BOLD),
        note_title_input,
        note_text_input,
        ft.Button(TEXTS[state["lang"]]["save"], on_click=add_note, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE),
        ft.Divider(),
        notes_col
    ], scroll=ft.ScrollMode.AUTO, expand=True)

    # --- ВКЛАДКА 3: ФИНАНСЫ ---
    finance_col = ft.Column(spacing=10)
    balance_text = ft.Text(f"{TEXTS[state['lang']]['balance']} 0 ₽", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400)
    top_cat_text = ft.Text("", size=12, color=ft.Colors.GREY_400)
    
    exp_name_input = ft.TextField(hint_text=TEXTS[state["lang"]]["expense_name"])
    exp_amount_input = ft.TextField(hint_text=TEXTS[state["lang"]]["expense_amount"], keyboard_type=ft.KeyboardType.NUMBER)
    
    type_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="expense", label=TEXTS[state["lang"]]["type_expense"]),
            ft.Radio(value="income", label=TEXTS[state["lang"]]["type_income"]),
        ]),
        value="expense"
    )
    
    exp_category = ft.Dropdown(
        options=[
            ft.dropdown.Option(TEXTS[state["lang"]]["cat_food"]),
            ft.dropdown.Option(TEXTS[state["lang"]]["cat_transport"]),
            ft.dropdown.Option(TEXTS[state["lang"]]["cat_fun"]),
            ft.dropdown.Option(TEXTS[state["lang"]]["cat_bad"]),
            ft.dropdown.Option(TEXTS[state["lang"]]["cat_other"]),
            ft.dropdown.Option(TEXTS[state["lang"]]["cat_salary"]),
            ft.dropdown.Option(TEXTS[state["lang"]]["cat_gift"]),
        ],
        value=TEXTS[state["lang"]]["cat_food"]
    )

    def set_filter(f):
        state["filter"] = f
        update_finance_ui()
        page.update()

    filter_buttons = ft.Row([
        ft.Button(TEXTS[state["lang"]]["filter_all"], on_click=lambda e: set_filter("all")),
        ft.Button(TEXTS[state["lang"]]["filter_today"], on_click=lambda e: set_filter("today")),
        ft.Button(TEXTS[state["lang"]]["filter_week"], on_click=lambda e: set_filter("week")),
        ft.Button(TEXTS[state["lang"]]["filter_month"], on_click=lambda e: set_filter("month")),
    ], scroll=ft.ScrollMode.AUTO)

    def add_expense(e):
        try:
            amount = float(exp_amount_input.value)
        except:
            return
        if amount > 0:
            is_income = (type_radio.value == "income")
            final_amount = amount if not is_income else -amount
            state["expenses"].append({
                "id": str(datetime.datetime.now().timestamp()),
                "name": exp_name_input.value, 
                "amount": final_amount,
                "cat": exp_category.value,
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "is_income": is_income
            })
            exp_name_input.value = ""
