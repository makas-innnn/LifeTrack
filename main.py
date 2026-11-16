import flet as ft
import json
import datetime
import platform

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
        "copy_logs": "Скопировать логи для разработчика", "logs_copied": "Логи скопированы! Отправьте их разработчику."
    },
    "en": {
        "app_title": "LifeTrack", "habits": "Habits", "notes": "Notes", "finance": "Finance", "info": "Info",
        "habit_name": "Habit name...", "note_title": "Title", "note_text": "Note text...",
        "expense_name": "What for?", "expense_amount": "Amount",
        "income_name": "Source of income?", "income_amount": "Amount",
        "type_income": "Income", "type_expense": "Expense",
        "cat_food": "Food", "cat_transport": "Transport", "cat_fun": "Fun", 
        "cat_bad": "Bad habits", "cat_other": "Other", "cat_salary": "Salary", "cat_gift": "Gift",
        "save": "Add", "delete": "Delete", "balance": "Balance:",
        "top_cat": "Most spent on:",
        "about_me": "Beginner coder, doing what I love",
        "tg_channel": "Telegram channel:", "tg_dm": "Contact (DM):", "gh": "GitHub:",
        "copy_logs": "Copy logs for developer", "logs_copied": "Logs copied! Send them to the developer."
    }
}

THEMES = {
    "dark": {"bg": ft.Colors.SURFACE, "card": ft.Colors.SURFACE_CONTAINER_HIGHEST},
    "light": {"bg": ft.Colors.WHITE, "card": ft.Colors.GREY_200},
    "purple": {"bg": ft.Colors.DEEP_PURPLE_900, "card": ft.Colors.DEEP_PURPLE_800},
    "forest": {"bg": ft.Colors.GREEN_900, "card": ft.Colors.GREEN_800}
}

def main(page: ft.Page):
    page.title = "LifeTrack"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK

    state = {"lang": "ru", "theme": "dark", "habits": [], "notes": [], "expenses": []}

    try:
        saved = page.client_storage.get("lifetrack_data")
        if saved:
            data = json.loads(saved)
            state["habits"] = data.get("habits", [])
            state["notes"] = data.get("notes", [])
            state["expenses"] = data.get("expenses", [])
    except: pass

    def save_data():
        try:
            page.client_storage.set("lifetrack_data", json.dumps({
                "habits": state["habits"], "notes": state["notes"], "expenses": state["expenses"]
            }))
        except: pass

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

    def delete_habit(index):
        state["habits"].pop(index)
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
                    ft.IconButton(ft.Icons.DELETE, icon_size=16, icon_color=ft.Colors.RED_400, on_click=lambda e, i=i: delete_habit(i))
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

    def delete_note(index):
        state["notes"].pop(index)
        update_notes_ui()
        save_data()
        page.update()

    def update_notes_ui():
        notes_col.controls.clear()
        for i, n in enumerate(reversed(state["notes"])):
            real_index = len(state["notes"]) - 1 - i
            notes_col.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(n["title"], size=16, weight=ft.FontWeight.BOLD, expand=True),
                            ft.Text(n["date"], size=12, color=ft.Colors.GREY_500),
                            ft.IconButton(ft.Icons.DELETE, icon_size=16, icon_color=ft.Colors.RED_400, on_click=lambda e, i=real_index: delete_note(i))
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

    def add_expense(e):
        try:
            amount = float(exp_amount_input.value)
        except:
            return
        if amount > 0:
            is_income = (type_radio.value == "income")
            state["expenses"].append({
                "name": exp_name_input.value, 
                "amount": amount if not is_income else -amount,
                "cat": exp_category.value,
                "date": datetime.datetime.now().strftime("%d.%m"),
                "is_income": is_income
            })
            exp_name_input.value = ""
            exp_amount_input.value = ""
            update_finance_ui()
            save_data()
            page.update()

    def delete_expense(index):
        state["expenses"].pop(index)
        update_finance_ui()
        save_data()
        page.update()

    def update_finance_ui():
        finance_col.controls.clear()
        balance = sum(item["amount"] for item in state["expenses"])
        balance_text.value = f"{TEXTS[state['lang']]['balance']} {balance:.2f} ₽"
        
        if balance < 0:
            balance_text.color = ft.Colors.GREEN_400
        else:
            balance_text.color = ft.Colors.WHITE if balance == 0 else ft.Colors.RED_400

        expenses_only = [item for item in state["expenses"] if not item.get("is_income", False)]
        if expenses_only:
            cats = {}
            for item in expenses_only:
                cats[item["cat"]] = cats.get(item["cat"], 0) + item["amount"]
            top_cat = max(cats, key=cats.get)
            top_cat_text.value = f"{TEXTS[state['lang']]['top_cat']} {top_cat}"
        else:
            top_cat_text.value = ""

        for i, item in enumerate(reversed(state["expenses"])):
            real_index = len(state["expenses"]) - 1 - i
            is_inc = item.get("is_income", False)
            color = ft.Colors.GREEN_400 if is_inc else ft.Colors.RED_400
            prefix = "+" if is_inc else "-"
            
            finance_col.controls.append(
                ft.Row([
                    ft.Column([
                        ft.Text(item["name"], size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(f'{item["cat"]} • {item["date"]}', size=12, color=ft.Colors.GREY_400)
                    ], expand=True),
                    ft.Text(f"{prefix}{abs(item['amount'])} ₽", size=14, color=color),
                    ft.IconButton(ft.Icons.DELETE, icon_size=16, icon_color=ft.Colors.RED_400, on_click=lambda e, i=real_index: delete_expense(i))
                ])
            )

    tab_finance = ft.Column([
        ft.Text("💰 Финансы", size=24, weight=ft.FontWeight.BOLD),
        balance_text,
        top_cat_text,
        ft.Divider(),
        exp_name_input,
        ft.Row([exp_amount_input, exp_category]),
        type_radio,
        ft.Button(TEXTS[state["lang"]]["save"], on_click=add_expense, bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE),
        ft.Divider(),
        finance_col
    ], scroll=ft.ScrollMode.AUTO, expand=True)

    # --- ВКЛАДКА 4: ИНФО + ЛОГИ ---
    async def copy_logs(e):
        sys_info = (
            f"--- LifeTrack Logs ---\n"
            f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"OS: {platform.system()} {platform.release()}\n"
            f"Python: {platform.python_version()}\n"
            f"Processor: {platform.processor()}\n"
            f"Lang: {state['lang']}, Theme: {state['theme']}\n"
            f"Habits: {len(state['habits'])}, Notes: {len(state['notes'])}, Expenses: {len(state['expenses'])}\n"
            f"----------------------\n"
            "Скопируйте этот текст и отправьте разработчику."
        )
        await ft.Clipboard().set(sys_info)
        page.snack_bar = ft.SnackBar(content=ft.Text(TEXTS[state["lang"]]["logs_copied"], color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN_800)
        page.snack_bar.open = True
        page.update()

    tab_info = ft.Column([
        ft.Icon(ft.Icons.PERSON, size=80),
        ft.Text("Евгений (makas)", size=22, weight=ft.FontWeight.BOLD),
        ft.Text(TEXTS[state["lang"]]["about_me"], size=16, color=ft.Colors.GREY_400),
        ft.Divider(height=15, color="transparent"),
        ft.Text(TEXTS[state["lang"]]["tg_channel"], size=14, color=ft.Colors.GREY_500),
        ft.Text("https://t.me/makas_1337", size=16, color=ft.Colors.BLUE_400, weight=ft.FontWeight.BOLD),
        ft.Divider(height=10, color="transparent"),
        ft.Text(TEXTS[state["lang"]]["tg_dm"], size=14, color=ft.Colors.GREY_500),
        ft.Text("https://t.me/makas_ik", size=16, color=ft.Colors.BLUE_400, weight=ft.FontWeight.BOLD),
        ft.Divider(height=10, color="transparent"),
        ft.Text(TEXTS[state["lang"]]["gh"], size=14, color=ft.Colors.GREY_500),
        ft.Text("https://github.com/makas-innnn", size=16, color=ft.Colors.BLUE_400, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20, color="transparent"),
        ft.Button(
            TEXTS[state["lang"]]["copy_logs"], 
            icon=ft.Icons.BUG_REPORT, 
            on_click=lambda e: page.run_task(copy_logs, e), 
            bgcolor=ft.Colors.GREY_700, 
            color=ft.Colors.WHITE
        ),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True)

    # --- НАВИГАЦИЯ ---
    content_container = ft.Container(expand=True, content=tab_habits)

    def switch_tab(index):
        if index == 0: content_container.content = tab_habits
        elif index == 1: content_container.content = tab_notes
        elif index == 2: content_container.content = tab_finance
        else: content_container.content = tab_info
        page.update()

    nav_bar = ft.NavigationBar(
        selected_index=0,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label=TEXTS[state["lang"]]["habits"]),
            ft.NavigationBarDestination(icon=ft.Icons.NOTE, label=TEXTS[state["lang"]]["notes"]),
            ft.NavigationBarDestination(icon=ft.Icons.MONEY, label=TEXTS[state["lang"]]["finance"]),
            ft.NavigationBarDestination(icon=ft.Icons.INFO, label=TEXTS[state["lang"]]["info"]),
        ],
        on_change=lambda e: switch_tab(e.control.selected_index)
    )

    def toggle_theme(e):
        themes = list(THEMES.keys())
        idx = themes.index(state["theme"])
        state["theme"] = themes[(idx + 1) % len(themes)]
        t = THEMES[state["theme"]]
        page.bgcolor = t["bg"]
        page.appbar.bgcolor = t["card"]
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text(TEXTS[state["lang"]]["app_title"]),
        center_title=True,
        actions=[ft.IconButton(ft.Icons.PALETTE, on_click=toggle_theme)]
    )

    page.navigation_bar = nav_bar
    page.add(content_container)
    
    update_habits_ui()
    update_notes_ui()
    update_finance_ui()

ft.run(main)
