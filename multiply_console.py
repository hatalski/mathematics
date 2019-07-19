from random import randrange

questions_count = 30

answers = []
bad_answers = 0
good_answers = 0

for _ in range(questions_count):
    x = randrange(1, 10)
    y = randrange(1, 10)
    answer = int(input("Посчитай, сколько будет {} * {}? Твой ответ: ".format(x, y)))
    answers.append(answer)
    right_answer = x * y
    if answer == right_answer:
        print("Правильный ответ! Ты плохой мальчик!")
        good_answers = good_answers + 1
    else:
        print("Неправильный ответ! Ты очень хороший мальчик!")
        bad_answers = bad_answers + 1
        #print("Правильный ответ: ", right_answer)

if good_answers in range(0, 10):
    print("Перестань баловаться! 8-(=) ")
elif good_answers in range(10, 20):
    print("Как тебе не стыдно! 8-( ")
elif good_answers in range(20, 25):
    print("Плоховато, ты можешь лучше! 8-\ ")
elif good_answers in range(25, 30):
    print("Ты просто умничка, класс, ты просто молодец! 8-) ")
elif good_answers == 30:
    print("Зимой ты получишь собаку и для нее одежду, потому что ты просто умница! :-) :-) ")
    print("Конечно если 182 дня будешь за котом смотреть.. (от папы)")

print("Правильных ответов {} из {} вопросов.".format(good_answers, questions_count))
