from program_files.initializer_command import *


def playing_command(finished, PAUSE, NUMBER):
    """
    функция воспроизовдит основную часть игры, когда оба персонажа живы и можно играть
    данные на вход:
    finished - всегда подается False, в процессе фукнция может поменяться на True - в таком случае игра завершена
    PAUSE - сигнал, говорящий остановилась ли игра на паузу или нет
    NUMBER - упорядоченный номер уровня
    """

    # рисует на screen и в файле баррикады
    for list_count, list in enumerate(button_massive[NUMBER]):  # перебирает каждый список из buttons. в каждом списке
        # свой символ

        for button in list:  # перебирает все кнопки с одинаковым символом-индетификатором
            for fence in fence_massive[NUMBER][list_count]:  # перебирает каждую баррикаду из списка. в списке все
                # привязаны к одной кнопке

                key_number, angle = map.treatment_fence(fence, button, NUMBER)  # получает номер кнопки, к которой
                # привязана баррикада, получает угол

                draw.draw_fence(fence, key_number, angle)

    # проверяет дозволенные направление движения
    for count_player, player in enumerate(players[NUMBER]):
        for list in button_massive[NUMBER]:  # перебирает каждый список из buttons
            for button in list:
                map.collision(player, count_player, button, NUMBER)

    # обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            return finished, PAUSE
        if event.type == pygame.KEYDOWN:
            for motion_number, motion in enumerate(gamer1_keys + gamer2_keys):  # по нажатию кнопки w или ARROW_UP
                # персонаж прыгает. motion - кнопка из списка (gamer1_keys + gamer2_keys), motion_number - его номер

                if event.key == motion and motion_number == 1:
                    players[NUMBER][motion_number // 3].to_make_it_move(motion_number % 3)
                if event.key == motion and motion_number == 4:
                    players[NUMBER][motion_number // 3].to_make_it_move(motion_number % 3)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if WIDTH // 2 - 40 <= event.pos[0] <= WIDTH // 2 + 40 and 0 <= event.pos[1] <= 40:  # если курсор
                # мыши попал по кнопке паузы, что расположена наверху игрового окна

                PAUSE = True

    # непрерывное управление персонажами по оси Ох
    for motion_number, motion in enumerate(gamer1_keys + gamer2_keys):
        if pygame.key.get_pressed()[motion] and (motion_number % 3 != 1):
            players[NUMBER][motion_number // 3].to_make_it_move(motion_number % 3)

    # беспрерывная анимация, зарисовка персонажей, проверка, попал ли персонаж в смертельную жидкость, нажатие кнопки
    for count_player, player in enumerate(players[NUMBER]):

        # проверка на нажатие кнопки
        for list in button_massive[NUMBER]:  # перебирает каждый список из buttons
            for button in list:
                map.collision(player, count_player, button, NUMBER)

        # перемещает персонаж
        player.move()

        # зарисовывает каждую ячейку
        for list in button_massive[NUMBER]:  # перебирает каждый список из buttons
            for button in list:
                for gate in gates[NUMBER]:
                    draw.draw_cells(map.get_file()[NUMBER], player, count_player, button, gate, gates, NUMBER)
                    # зарисовка каждой игровой ячейки

    for count_player, player in enumerate(players[NUMBER]):

        # проверяет, столкнулся ли персонаж с жидкостью и остался ли персонаж в живых
        inform = player.inf()
        if not inform[3]:
            pass
        else:
            draw.draw_character(count_player, inform)

    for decoration in decorations[NUMBER]:  # рисует декор
        draw.draw_element(decoration)
    draw.draw_pause_button()

    pygame.display.update()
    screen.fill((255, 255, 255))

    return finished, PAUSE  # finished - окончена ли игра или нет, PAUSE - Остановлена ли игра на паузу или нет
