from cls_grammar_recognizer import GrammarRecognizer


def main(is_need_instruction=True):
    if is_need_instruction:
        print('Инструкция:\n'
              '+---------------------------------------------------------------------------------------------+\n'
              '|    ->   | определяется как | разделяет левую и правую части правила                         |\n'
              '+---------+------------------+----------------------------------------------------------------+\n'
              '|    |    |       или        | разделяет альтернативы                                         |\n'
              '+---------+------------------+----------------------------------------------------------------+\n'
              '|  (...)  |    разделение    | скобки используются дял более явного обозначения альтернатив   |\n'
              '+---------+------------------+----------------------------------------------------------------+\n'
              '|  [...]  |    может быть    | цепочка, записанная внутри скобок может отсутствовать          |\n'
              '+---------+------------------+----------------------------------------------------------------+\n'
              '|  {...}  |  повтор ноль или | цепочка может многократно повторяться или отсутствовать        |\n'
              '|         |    более раз     |                                                                |\n'  
              '+---------+------------------+----------------------------------------------------------------+\n'
              '|  {...}* |  повтор один или | цепочка может повторятся один или более раз                    |\n'
              '|         |    более раз     |                                                                |\n'
              '+---------------------------------------------------------------------------------------------+\n'
              'Нетерминалы заключаются в угловые скобки (< >)\n'
              'Для вывода символов <, >, (, ), [, ], {, }, |, -, *, \'\n'
              'их следует заключить в одинарные кавычки\n'
              'Первое введенное правило считается за стартовое\n')

    GR = GrammarRecognizer()

    is_turn_on = True
    status = 0  # 0 -- write rules, 1 -- check lines
    while is_turn_on:
        match status:
            case 0:
                match input('rule: '):
                    case '0':
                        if len(GR.get_token_data()) != 0:
                            status = 1
                            print('Rules added\n')

                            # print(GR.get_token_data())
                        else:
                            print('Rules_data is empty! Add some rules\n')

                    case user_input:
                        if user_input.replace(' ', '') != '':
                            try:
                                GR.save_rule_line(user_input)
                            except Exception as ex:
                                print(ex)
                                print('Rule not added to data\n')

            case 1:
                match input('line: '):
                    case 'exit()':
                        is_turn_on = False
                    case user_input:
                        try:
                            is_right, index = GR.is_line_right(user_input)
                            if is_right:
                                print('Line is right!\n')
                            elif index >= len(user_input):
                                print(f'Line is wrong! Wrong end by index={index}\n')
                            else:
                                print(f'Line is wrong! Wrong letter "{user_input[index]}" by index={index}\n')

                        except Exception as ex:
                            print(ex)
                            print('Add missing rule\n')
                            status = 0

    print('Goodbye!')


if __name__ == '__main__':
    main()


'''



