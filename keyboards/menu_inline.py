from cgitb import text
from aiogram.types import ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api.db_commands import get_faculties, get_forma, get_specialization, get_directions



menu_cd = CallbackData("show_menu", "level", "faculties", "form", "specialization", "direction_id")
direct_cd = CallbackData("direct", "direction_id")
start_menu_cd = CallbackData("start_menu","button_id")

def make_callback_data(level, faculties="0", form="0", specialization="0", direction_id="0"):
    return menu_cd.new(level=level, faculties=faculties, form=form, specialization=specialization, direction_id=direction_id)

#получаем факультеты
async def faculties_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()
    faculties = await get_faculties()
    for el in faculties:
        button_text = el.faculties_name
        callback_data = make_callback_data(level=CURRENT_LEVEL+1, faculties=el.faculties_code)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=start_menu_cd.new(button_id="button_start"))
    )
    return markup

#получаем форму обучения
async def forma_keyboard(facultie):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()
    forms = await get_forma(facultie)
    for form in forms:
        button_text = form.form_name
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, faculties=facultie, form=form.form_code)

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1, faculties=facultie))
    )
    return markup

#получаем специальность(бакалавриат и тд)
async def specialization_keyboard(facultie, form):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()
    specializations = await get_specialization(facultie, form)
    for specialization in specializations:
        button_text = specialization.specialization_name
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, faculties=facultie, form=form, specialization=specialization.specialization_code)

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1, faculties=facultie, form=form))
    )
    return markup

#получаем направление (ПИвЛ, ПМИ и т.д )
async def directions_keyboard(facultie, form, specialization):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row_width=1)
    directions = await get_directions(facultie,form,specialization)
    for direction in directions:
        button_text = direction.name
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, faculties=facultie, form=form, specialization=specialization, direction_id=direction.id)

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1, faculties=facultie, form=form, specialization=specialization))
    )
    return markup

async def direction_keyboard(facultie, form, specialization):
    CURRENT_LEVEL = 4
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1, faculties=facultie, form=form, specialization=specialization))
    )
    return markup

    
