# start
HELLO_USER = "Привет, {}! Я помогу тебе с выбором."
FACULTY_SELECTION = 'Выберите факультет'
FORM_SELECTION = 'Выберите форму обучения'
SPECIALIZATION_SELECTION = 'Выберите специальность'
DIRECTION_SELECTION = 'Выберите направление'

# filter
START_MESSAGE = 'Выберите нужное количество предметов и нажмите кнопку "Найти".'
ANSWER_1_ERROR = 'Вы не выбрали ни одного предмета. Повторите еще раз.'
ITEM_SELECTION = 'Вы выбрали {}'
DEF_FIND_ERROR_MESSAGE = 'По вашему запросу ({}) я не смог найти ни одного направления.'
DEF_FIND_MESSAGE = 'Ваш запрос: {}'
DEF_LIST_DIRECTIONS_LEVEL = 'Направления по вашему запросу ({}).\nКоличество направлений: {}'

# support
ASK_USER = 'Вы можете задать свой вопрос. Оператор ответит вам позже.'
GET_QUESTIONS = 'Получить список новых вопросов'
ASK_CONTROLLER_ACCEPT = 'Напишите ваш вопрос\nДля отмены пропишите команду /start'
ASK_CONTROLLER_GET = 'Есть новые вопросы!\n'
ASK_CONTROLLER_QUESTION = 'Вопрос пришел {}\nВопрос от {}:\n{}'
ASK_CONTROLLER_QUESTION_ADMIN = 'ID: {}\nИмя пользователя: {}\nIDпользователя: {}\nВремя: {}\nВопрос:\n{}'
ASK_MESSAGE = 'Ваш вопрос был отправлен оператору.'
NO_NEW_QUESTIONS = 'Новый вопросов нет'
QUESTION_ANSWER = 'Оператор: {}\nАбитуриент: {}\nВопрос пришел {}\nПолучен ответ {}\nВопрос: {}\nОтвет: {}'

# support_controller
REJECT_QUESTION_OPERATOR = 'Вопрос отклонен'
REJECT_QUESTION_USER = 'Ваш вопрос был отклонен'
REPLY_QUESTION_OPERATOR = 'Жду ответ на вопрос'
# support_state
REPLY_SENT = 'Ответ на вопрос отправлен'
REPLY_RESEIVED = '<b>Ответ на ваш вопрос:</b>\n{}'


def message_text(direction):
    text: str

    def list_exams(exams: []):
        str_exams = ''
        for exam in exams:
            str_exams += f'\n{exam["name"]} - {exam["estimation"]} {get_points(exam["estimation"])} {"<b>(по выбору)</b>" if bool(exam["choice"]) else ""}'
        return str_exams

    def list_spos(spos: []):
        str_spo = ''
        for spo in spos:
            str_spo += f'\n{spo["name"]} - {spo["estimation"]} {get_points(spo["estimation"])} {"<b>(по выбору)</b>" if bool(spo["choice"]) else ""}'
        return str_spo

    def get_points(estimation: int):
        estimation %= 10
        if estimation == 1:
            return "балл"
        elif estimation in [2, 3, 4]:
            return "балла"
        elif estimation in [5, 6, 7, 8, 9, 0]:
            return "баллов"
        else:
            return "баллов"

    def bachelor_text():
        return f"""<b>{direction["name"]}</b>
    
<i><b>{direction["qualifications"]["forms_of_study"]["faculties"]["name"]}</b></i>
<i><b>{direction["qualifications"]["forms_of_study"]["name"]}</b> форма обучения</i>
<i>Уровень образования - <b>{direction["qualifications"]["name"].lower()}</b></i>

{f"<b>Экзамены (на базе ЕГЭ)</b>{list_exams(direction['exams'])}" if len(direction["exams"]) > 0 else ""}

{f"<b>Экзамены (на базе СПО)</b>{list_spos(direction['spos'])}" if len(direction['spos']) != 0 else ""}

<b>Бюджетные места {direction["budget_places"]}</b>
<b>Платные места {direction["paid_places"]}</b>

<b>Стоимость обучения в год</b> {direction["coast"]} ₽

<b>Срок обучения</b> {int(direction["duration"]) if float(direction["duration"]).is_integer() else direction["duration"]}

{direction["description"]}"""

    def magistracy_text():
        return f"""<b>{direction["name"]}</b>

<i><b>{direction["qualifications"]["forms_of_study"]["faculties"]["name"]}</b></i>
<i><b>{direction["qualifications"]["forms_of_study"]["name"]}</b> форма обучения</i>
<i>Уровень образования - <b>{direction["qualifications"]["name"].lower()}</b></i>

{f"<b>Вступительные испытания</b>{list_exams(direction['exams'])}" if len(direction["exams"]) > 0 else ""}

<b>Бюджетные места {direction["budget_places"]}</b>
<b>Платные места {direction["paid_places"]}</b>

<b>Стоимость обучения в год</b> {direction["coast"]} ₽

<b>Срок обучения</b> {int(direction["duration"]) if float(direction["duration"]).is_integer() else direction["duration"]}

{direction["description"]}"""

    match direction["qualifications"]["name"]:
        case "Бакалавриат":
            return bachelor_text()
        case "Магистратура":
            return magistracy_text()
        case _:
            return bachelor_text()

