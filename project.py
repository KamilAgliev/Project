import json

from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup
from duty import Duty

TOKEN = "1116820230:AAHm6C00UvlPDOk-NAnT1kPgftMPuzI-CG4"

duties = {}

with open("sessionStorage.json", "r") as ses_file:
    cur_ses = json.load(ses_file)


def save_session():
    with open("sessionStorage.json", "w") as save_file:
        json.dump(cur_ses, save_file)


def get_commands1(update, context):
    update.message.reply_text("/get_duties - просмотеть все ваши дежурства\n"
                              "/start_add - добавить дежурство\n"
                              "/delete_duty - удалить дежурство\n"
                              "/logout - удалить историю своего аккаунта\n"
                              "/help - вывести информацию о командах")
    return 1


def get_commands2(update, context):
    update.message.reply_text("/duty_now - получить набор людей, которые будут сейчас дежурить,\n"
                              "вызывайте команду столько раз, сколько происходит дежурств в день\n"
                              "/absent - указать людей, которые отсутствуют на данный момент\n"
                              "/returned - удалить людей, которые вернулись после отсутствия\n"
                              "/get_back - возвратится в предыдущее меню\n"
                              "/help - вывести информацию о командах")
    return 2


def start(update, context):
    user = update.effective_user
    if str(user.id) not in cur_ses:
        cur_ses[str(user.id)] = {}
    update.message.reply_text("Здравствуйте, это бот - помощник по дежурству.\n"
                              "Вы можете вызвать команду /help для ознакомления.")
    save_session()
    return 1


def get_back(update, context):
    update.message.reply_text("Теперь вы в основном меню.")
    return 1


def logout(update, context):
    user = update.effective_user
    update.message.reply_text("Вы удалены из базы данных, для начала нажмите /start")
    del cur_ses[str(user.id)]
    save_session()


def get_duties(update, context):
    user = update.effective_user
    if "c" not in cur_ses[str(user.id)].keys():
        cur_ses[str(user.id)]["c"] = 0
    cur_ses[str(user.id)]["c"] = 1
    if "ask" not in cur_ses[str(user.id)]:
        cur_ses[str(user.id)]["ask"] = 0
    return get_info(update, context)


def start_duties(update, context):
    user = update.effective_user
    if "w" not in cur_ses[str(user.id)]:
        cur_ses[str(user.id)]["w"] = 0
    cur_ses[str(user.id)]["w"] = 1
    return get_info(update, context)


def duty_now(update, context):
    user = update.effective_user
    for i in range(len(duties[str(user.id)])):
        if duties[str(user.id)][i].name == cur_ses[str(user.id)]["cur_duty_name"]:
            res = duties[str(user.id)][i].duty_now()
            update.message.reply_text("\n".join(res))
    return 2


def delete_duty(update, context):
    user = update.effective_user
    if "del" not in cur_ses[str(user.id)].keys():
        cur_ses[str(user.id)]["del"] = 0
    cur_ses[str(user.id)]["del"] = 1
    if "del_ask" not in cur_ses[str(user.id)]:
        cur_ses[str(user.id)]["del_ask"] = 0
    return get_info(update, context)


def get_info(update, context):
    user = update.effective_user
    text = update.message.text
    if "del" not in cur_ses[str(user.id)].keys():
        cur_ses[str(user.id)]["del"] = 0
        cur_ses[str(user.id)]["del_ask"] = 0

    if cur_ses[str(user.id)]["del"] == 1:
        if cur_ses[str(user.id)]["del_ask"] == 0:
            reply_keyboard = []
            for d in cur_ses[str(user.id)]["duties"]:
                reply_keyboard.append([d.name])
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            update.message.reply_text("Выберите нужное дежурство.", reply_markup=markup)
            cur_ses[str(user.id)]["del_ask"] = 1
            return 1
        else:
            ind = -1
            for i in range(len(duties[str(user.id)])):
                if duties[str(user.id)][i].name == update.message.text:
                    ind = i
                    break
            if ind == -1:
                update.message.reply_text("Выберите существующее дежурство!")
                return 1
            del duties[str(user.id)][ind]
            cur_ses[str(user.id)]["del_ask"] = 0
            cur_ses[str(user.id)]["del"] = 0
            update.message.reply_text("Дежурство успешно удалено.")
            return 1

    if "c" not in cur_ses[str(user.id)].keys():
        cur_ses[str(user.id)]["c"] = 0

    if cur_ses[str(user.id)]["c"] == 1:
        if "ask" not in cur_ses[str(user.id)]:
            cur_ses[str(user.id)]["ask"] = 0
        if cur_ses[str(user.id)]["ask"] == 0:
            reply_keyboard = []
            if str(user.id) not in duties.keys():
                duties[str(user.id)] = []
            if len(duties[str(user.id)]) == 0:
                update.message.reply_text("У вас пока нет дежурств. Вы можете их добавить.")
                return 1
            for d in duties[str(user.id)]:
                reply_keyboard.append([d.name])
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            update.message.reply_text("Выберите нужное дежурство", reply_markup=markup)
            cur_ses[str(user.id)]["ask"] = 1
            return 1
        else:
            f = 0
            for d in duties[str(user.id)]:
                if d.name == update.message.text:
                    f = 1
                    break
            if f == 0:
                update.message.reply_text("Выберите существующее дежурство")
                return 1
            cur_ses[str(user.id)]["cur_duty_name"] = update.message.text
            cur_ses[str(user.id)]["ask"] = 0
            cur_ses[str(user.id)]["c"] = 0
            get_commands2(update, context)
            return 2

    if "w" not in cur_ses[str(user.id)]:
        cur_ses[str(user.id)]["w"] = 0

    if cur_ses[str(user.id)]["w"] == 1:
        if "step" not in cur_ses[str(user.id)]:
            cur_ses[str(user.id)]["step"] = -1
        if cur_ses[str(user.id)]["step"] == -1:
            update.message.reply_text("Введите название дежурства.")
            cur_ses[str(user.id)]["step"] += 1
            return 1
        if cur_ses[str(user.id)]["step"] == 0:
            if "lst" not in cur_ses[str(user.id)]:
                cur_ses[str(user.id)]["lst"] = []
            cur_ses[str(user.id)]["lst"].append(update.message.text)
            cur_ses[str(user.id)]["step"] += 1
            update.message.reply_text("Вводите последовательность людей следующим образом:\n"
                                      "Иван Иванов, Галкин Матвей, Тимаков Ильнар и т.д. через запятую")
            return 1
        if cur_ses[str(user.id)]["step"] == 1:
            text = update.message.text
            people = [p for p in text.split(',')]
            cur_ses[str(user.id)]["lst"].append(people)
            cur_ses[str(user.id)]["step"] += 1
            update.message.reply_text("Введите количество людей в группе.")
            return 1
        if cur_ses[str(user.id)]["step"] == 2:
            cur_ses[str(user.id)]["lst"].append(update.message.text)
            if "duties" not in cur_ses[str(user.id)]:
                cur_ses[str(user.id)]["duties"] = []
            lst = cur_ses[str(user.id)]["lst"]
            cur_ses[str(user.id)]["lst"] = []
            D = Duty(lst[0], lst[1], lst[2])
            if str(user.id) not in duties:
                duties[str(user.id)] = []
            duties[str(user.id)].append(D)
            update.message.reply_text("Дежурство добавлено")
            cur_ses[str(user.id)]["w"] = 0
            cur_ses[str(user.id)]["step"] = -1
            return 1

    if "left" not in cur_ses[str(user.id)]:
        cur_ses[str(user.id)]["left"] = 0
        cur_ses[str(user.id)]["left_ask"] = 0

    if cur_ses[str(user.id)]["left"] == 1:
        if cur_ses[str(user.id)]["left_ask"] == 0:
            update.message.reply_text("Вводите последовательность людей следующим образом:\n"
                                      "Иван Иванов, Галкин Матвей, Тимаков Ильнар и т.д. через запятую")
            cur_ses[str(user.id)]["left_ask"] = 1
        else:
            text = update.message.text
            people = [p for p in text.split(',')]
            for i in range(len(duties[str(user.id)])):
                if duties[i].name == cur_ses[str(user.id)]["cur_duty_name"]:
                    duties[i].left(people)
            update.message.reply_text("Изменения сохранены.")
            cur_ses[str(user.id)]["left"] = 0
            cur_ses[str(user.id)]["left_ask"] = 0

    if "returned" not in cur_ses[str(user.id)]:
        cur_ses[str(user.id)]["returned"] = 0
        cur_ses[str(user.id)]["returned_ask"] = 0

    if cur_ses[str(user.id)]["returned"] == 1:
        if cur_ses[str(user.id)]["returned_ask"] == 0:
            update.message.reply_text("Вводите последовательность людей следующим образом:\n"
                                      "Иван Иванов, Галкин Матвей, Тимаков Ильнар и т.д. через запятую")
            cur_ses[str(user.id)]["returned_ask"] = 1
        else:
            people = [p for p in text.split(',')]
            for i in range(len(duties[str(user.id)])):
                if duties[i].name == cur_ses[str(user.id)]["cur_duty_name"]:
                    duties[i].returned(people)
            update.message.reply_text("Изменения сохранены.")
            cur_ses[str(user.id)]["left"] = 0
            cur_ses[str(user.id)]["left_ask"] = 0


def left(update, context):
    user = update.effective_user
    if "left" not in cur_ses[str(user.id)]:
        cur_ses[str(user.id)]["left"] = 0
        cur_ses[str(user.id)]["left_ask"] = 0
    cur_ses[str(user.id)]["left"] = 1
    get_info(update, context)


def returned(update, context):
    user = update.effective_user
    if "left" not in cur_ses[str(user.id)]:
        cur_ses[str(user.id)]["returned"] = 0
        cur_ses[str(user.id)]["returned_ask"] = 0
    cur_ses[str(user.id)]["returned"] = 1
    get_info(update, context)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        fallbacks=[CommandHandler("logout", logout)],
        states={
            1: [CommandHandler("get_duties", get_duties),
                CommandHandler("start_add", start_duties),
                CommandHandler("delete_duty", delete_duty),
                CommandHandler("help", get_commands1),
                MessageHandler(Filters.text, get_info)
                ],
            2: [
                CommandHandler("duty_now", duty_now),
                CommandHandler("absent", left),
                CommandHandler("returned", returned),
                CommandHandler("get_back", get_back),
                CommandHandler("help", get_commands2),
            ],
        }
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
