import flet as ft
import json
import datetime

TEXTS = {
    "ru": {
        "app_title": "LifeTrack", "habits": "Привычки", "notes": "Заметки", "finance": "Финансы", "info": "Инфо",
        "add_habit": "Добавить привычку", "habit_name": "Название привычки...",
        "add_note": "Добавить заметку", "note_title": "Заголовок", "note_text": "Текст заметки...",
        "add_expense": "Добавить расход", "expense_name": "На что потратил?", "expense_amount": "Сумма (₽)",
        "categories": "Категория", "cat_food": "Еда", "cat_transport": "Транспорт", "cat_fun": "Развлечения", 
        "cat_bad": "Вредное (алкоголь/сигареты)", "cat_other": "Другое",
        "save": "Сохранить", "delete": "Удалить", "total": "Всего потрачено:",
        "about_me": "Начинающий кодер, делаю что в кайф",
        "tg_channel": "Телеграм-канал:", "tg_dm": "Связь (ЛС):", "gh": "GitHub:"
    },
    "en": {
        "app_title": "LifeTrack", "habits": "Habits", "notes": "Notes", "finance": "Finance", "info": "Info",
        "add_habit": "Add habit", "habit_name": "Habit name...",
        "add_note": "Add note", "note_title": "Title", "note_text": "Note text...",
        "add_expense": "Add expense", "expense_name": "What for?", "expense_amount": "Amount",
        "categories": "Category", "cat_food": "Food", "cat_transport": "Transport", "cat_fun": "Fun", 
        "cat_bad": "Bad (alcohol/smokes)", "cat_other": "Other",
        "save": "Save", "delete": "Delete", "total": "Total spent:",
        "about_me": "Beginner coder, doing what I love",
        "tg_channel": "Telegram channel:", "tg_dm": "Contact (DM):", "gh": "GitHub:"
    }
}

THEMES = {
    "dark": {"bg": ft.Colors.SURFACE, "accent": ft.Colors.PURPLE_400, "card": ft.Colors.SURFACE_CONTAINER_HIGHEST},
    "light": {"bg": ft.Colors.WHITE, "accent": ft.Colors.PURPLE_700, "card": ft.Colors.GREY_200},
    "purple": {"bg": ft.Colors.DEEP_PURPLE_900, "accent": ft.Colors.PURPLE_200, "card": ft.Colors.DEEP_PURPLE_800},
    "forest": {"bg": ft.Colors.GREEN_900, "accent": ft.Colors.LIGHT_GREEN_400, "card": ft.Colors.GREEN_800}
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
            state["habits"].append({"name": habit_input.value, "done": False})
            habit_input.value = ""
            update_habits_ui()
            save_data()
            page.update()

    def toggle_habit(index):
        state["habits"][index]["done"] = not state["habits"][index]["done"]
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
        for i, h in enumerate(state["habits"]):
            habits_col.controls.append(
                ft.Row([
                    ft.Checkbox(value=h["done"], on_change=lambda e, i=i: toggle_habit(i)),
                    ft.Text(h["name"], size=16, expand=True, color=ft.Colors.GREY_300 if h["done"] else ft.Colors.WHITE),
                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=lambda e, i=i: delete_habit(i))
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
            state["notes"].append({"title": note_title_input.value, "text": note_text_input.value})
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
        for i, n in enumerate(state["notes"]):
            notes_col.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(n["title"], size=16, weight=ft.FontWeight.BOLD, expand=True),
                            ft.IconButton(ft.Icons.DELETE, icon_size=16, icon_color=ft.Colors.RED_400, on_click=lambda e, i=i: delete_note(i))
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
    total_text = ft.Text(f"{TEXTS[state['lang']]['total']} 0 ₽", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400)
    
    exp_name_input = ft.TextField(hint_text=TEXTS[state["lang"]]["expense_name"])
    exp_amount_input = ft.TextField(hint_text=TEXTS[state["lang"]]["expense_amount"], keyboard_type=ft.KeyboardType.NUMBER)
    exp_category = ft.Dropdown(
        options=[
            ft.dropdown.Option(TEXTS[state["lang"]]["cat_food"]),
            ft.dropdown.Option(TEXTS[state["lang"]]["cat_transport"]),
            ft.dropdown.Option(TEXTS[state["lang"]]["cat_fun"]),
            ft.dropdown.Option(TEXTS[state["lang"]]["cat_bad"]),
            ft.dropdown.Option(TEXTS[state["lang"]]["cat_other"]),
        ],
        value=TEXTS[state["lang"]]["cat_food"]
    )

    def add_expense(e):
        try:
            amount = float(exp_amount_input.value)
        except:
            return
        if amount > 0:
            state["expenses"].append({
                "name": exp_name_input.value, "amount": amount, "cat": exp_category.value,
                "date": datetime.datetime.now().strftime("%d.%m")
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
        total = sum(item["amount"] for item in state["expenses"])
        total_text.value = f"{TEXTS[state['lang']]['total']} {total:.2f} ₽"
        
        for i, item in enumerate(reversed(state["expenses"])):
            real_index = len(state["expenses"]) - 1 - i
            finance_col.controls.append(
                ft.Row([
                    ft.Column([
                        ft.Text(item["name"], size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(f'{item["cat"]} • {item["date"]}', size=12, color=ft.Colors.GREY_400)
                    ], expand=True),
                    ft.Text(f"-{item['amount']} ₽", size=14, color=ft.Colors.RED_400),
                    ft.IconButton(ft.Icons.DELETE, icon_size=16, icon_color=ft.Colors.RED_400, on_click=lambda e, i=real_index: delete_expense(i))
                ])
            )

    tab_finance = ft.Column([
        ft.Text("💰 Финансы", size=24, weight=ft.FontWeight.BOLD),
        total_text,
        exp_name_input,
        ft.Row([exp_amount_input, exp_category]),
        ft.Button(TEXTS[state["lang"]]["save"], on_click=add_expense, bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE),
        ft.Divider(),
        finance_col
    ], scroll=ft.ScrollMode.AUTO, expand=True)

    # --- ВКЛАДКА 4: ИНФО ---
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
