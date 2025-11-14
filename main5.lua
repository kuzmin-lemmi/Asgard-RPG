-- main5.lua
-- Наследие Асгарда — Великая интеграция (Модули 1–3)
-- Без local и без math.randomseed; с «прогревом» random и флагом first_visit

---------------------------------------------------
-- 0) Прогрев генератора случайных чисел (без seed)
---------------------------------------------------
math.random(); math.random(); math.random()

---------------------------------------------------
-- 1) Досье Аватара
---------------------------------------------------
player = {
    name = "",
    health = 100,
    actionPoints = 4,
    strength = 1,
    tech = 1,
    luck = 1,
    isAlive = true,
    inventory = {
        aid_kits = 2,
        key_cards = 0
    }
}

---------------------------------------------------
-- 2) Досье врага (страж уровня)
---------------------------------------------------
enemy = {
    name = "Ржавый Дрон-Санитар",
    health = 30,
    damage = 3,
    isAlive = true
}

---------------------------------------------------
-- 3) Протокол «Аватар» (инициализация)
---------------------------------------------------
io.write("...Протокол 'Аватар' активен...")
io.write("\nВведите ваше имя: ")
player.name = io.read()

skillPoints = 10
print("\nДобро пожаловать, " .. player.name .. "!")
print("У вас есть " .. skillPoints .. " очков для распределения.")

io.write("Сколько очков (из " .. skillPoints .. ") вложить в СИЛУ? ")
pointsToAdd = tonumber(io.read())
player.strength = player.strength + pointsToAdd
skillPoints = skillPoints - pointsToAdd

print("...Осталось " .. skillPoints .. " очков...")
io.write("Сколько очков вложить в ТЕХНИКУ? ")
pointsToAdd = tonumber(io.read())
player.tech = player.tech + pointsToAdd
skillPoints = skillPoints - pointsToAdd

print("...Осталось " .. skillPoints .. " очков...")
io.write("Сколько очков вложить в УДАЧУ? ")
pointsToAdd = tonumber(io.read())
player.luck = player.luck + pointsToAdd
skillPoints = skillPoints - pointsToAdd

print("\n========================================")
print("    ДОСЬЕ НАСЛЕДНИКА АКТИВИРОВАНО")
print("========================================")
print(" ИМЯ: " .. player.name)
print(" ЗДОРОВЬЕ: " .. player.health)
print(" ОЧКИ ДЕЙСТВИЙ: " .. player.actionPoints)
print("    СИЛА (СИЛ): " .. player.strength)
print("    ТЕХНИКА (ТЕХ): " .. player.tech)
print("    УДАЧА (УДЧ): " .. player.luck)
print("========================================")

io.write("\nНажмите Enter, чтобы продолжить...")
io.read()

if package.config:sub(1,1) == "\\" then os.execute("cls") else os.execute("clear") end

---------------------------------------------------
-- 4) Уровень 1: «Внешний периметр» (цикл уровня)
---------------------------------------------------
level1_cleared = false
first_visit = true

while level1_cleared == false do
    -- мягкий респаун после гибели (для повторной попытки)
    if player.isAlive == false then
        player.isAlive = true
        player.health = 100
    end

    if first_visit == true then
        print("\n========================================")
        print("    УРОВЕНЬ 1: ВНЕШНИЙ ПЕРИМЕТР")
        print("========================================")
        print("\nЛедяной ветер бьёт в лицо, забивая снежную крошку под воротник.")
        print("Ты стоишь у 'Внешнего Периметра' горы Асгард. Это не просто дверь —")
        print("это кладбище технологий. Огромные ржавые прожекторы смотрят в серое небо,")
        print("как глазницы мёртвых гигантов. Раздавленные останки охранного Дрона-Санитара")
        print("наполовину вмерзли в лёд у подножия массивного КПП.")
        print("Его стальные ворота безнадёжно заклинило, но рядом, на стене,")
        print("тускло мерцает экран терминала, покрытый коркой инея.")
        print("Воздух пахнет озоном и ржавчиной. Это твой первый шаг в гробницу Древних.")
        first_visit = false
    end

    print("\nТвой взгляд цепляется за две вещи:")
    print("[1] Массивная решётчатая дверь, заклинившая и покрытая льдом.")
    print("[2] Настенный терминал, тускло искрящий рядом с дверью.")
    io.write("\nТвоё действие: ")
    level_choice = io.read()

    -- ===== Путь 1: ДВЕРЬ (проверка СИЛЫ) =====
    if level_choice == "1" then
        print("\n>>> ВЫБОР: ДВЕРЬ")
        print("Ты упираешься плечом в холодный металл. Механизм заперт намертво,")
        print("но руны силы на твоих перчатках тихо пульсируют. Пора проверить СИЛУ.")

        difficulty = math.random(10)
        print("Сложность: " .. difficulty .. " | Твоя СИЛА: " .. player.strength)

        if player.strength >= difficulty then
            print("\nУСПЕХ! С оглушительным скрежетом ржавый засов ломается.")
            print("ПУТЬ ОТКРЫТ.")

            -- Сброс врага перед боем
            enemy.name = "Ржавый Дрон-Санитар"
            enemy.health = 30
            enemy.damage = 3
            enemy.isAlive = true

            -- ===== АРЕНА (БОЙ) =====
            print("\n========================================")
            print("               СИГНАЛ ТРЕВОГИ")
            print("========================================")
            print(" ПРОТИВНИК: " .. enemy.name)
            print(" ЗДОРОВЬЕ ВРАГА: " .. enemy.health)
            print("========================================")

            while player.isAlive == true and enemy.isAlive == true do
                player.actionPoints = 4
                print("\n========================================")
                print("      ХОД НАСЛЕДНИКА | ОД: " .. player.actionPoints)
                print("========================================")

                while player.actionPoints > 0 and enemy.isAlive == true do
                    if enemy.health < 0 then enemy.health = 0 end
                    print(" ГЕРОЙ: " .. player.health .. " HP  |  ВРАГ: " .. enemy.health .. " HP")

                    print("+----------------------- ДЕЙСТВИЯ -----------------------+")
                    print("|  [1] Атака (2 ОД)                                      |")
                    print("|  [2] Использовать Аптечку (3 ОД)                       |")
                    print("|  [9] Закончить ход                                     |")
                    print("+--------------------------------------------------------+")
                    io.write("> Введите номер действия: ")
                    choice = io.read()

                    if choice == "1" then
                        if player.actionPoints >= 2 then
                            player.actionPoints = player.actionPoints - 2

                            damage = 0
                            critical_hit = false
                            if math.random(100) <= player.luck then
                                critical_hit = true
                                damage = player.strength * 2
                            else
                                damage = player.strength
                            end

                            enemy.health = enemy.health - damage
                            if enemy.health < 0 then enemy.health = 0 end

                            if critical_hit == true then
                                print("\n>>> КРИТИЧЕСКИЙ УДАР! Вы нанесли " .. damage .. " урона!")
                            else
                                print("\n>>> АТАКА! Вы нанесли " .. damage .. " урона.")
                            end

                            if enemy.health <= 0 then
                                print(">>> " .. enemy.name .. " повержен!")
                                enemy.isAlive = false
                                break
                            else
                                print(" У врага осталось " .. enemy.health .. " HP.")
                            end
                        else
                            print("\n>>> НЕДОСТАТОЧНО ОД ДЛЯ АТАКИ!")
                        end

                    elseif choice == "2" then
                        if player.actionPoints >= 3 then
                            if player.inventory.aid_kits > 0 then
                                player.actionPoints = player.actionPoints - 3
                                player.inventory.aid_kits = player.inventory.aid_kits - 1

                                heal_amount = 25
                                player.health = player.health + heal_amount
                                if player.health > 100 then player.health = 100 end

                                print("\n>>> ЛЕЧЕНИЕ! Вы использовали Аптечку (+25 HP).")
                                print("Здоровье: " .. player.health .. " | Осталось аптечек: " .. player.inventory.aid_kits)
                            else
                                print("\n>>> ОШИБКА! У вас нет аптечек!")
                            end
                        else
                            print("\n>>> НЕДОСТАТОЧНО ОД ДЛЯ ИСПОЛЬЗОВАНИЯ ПРЕДМЕТА!")
                        end

                    elseif choice == "9" then
                        print("\n>>> ВЫБОР: ЗАКОНЧИТЬ ХОД!")
                        break
                    else
                        print("\n>>> НЕИЗВЕСТНАЯ КОМАНДА! Вы теряете 1 ОД.")
                        player.actionPoints = player.actionPoints - 1
                    end

                    if player.actionPoints <= 0 then
                        print("\n...Очки Действий иссякли...")
                    end
                end -- конец while действий игрока

                print("\n--- ХОД ИГРОКА ЗАВЕРШЕН ---")

                if enemy.isAlive == true then
                    print("\n...Ход " .. enemy.name .. "...")
                    damage = enemy.damage
                    player.health = player.health - damage
                    if player.health < 0 then player.health = 0 end

                    print(">>> Дрон атакует и наносит " .. damage .. " урона!")
                    if player.health <= 0 then
                        print(">>> ВАШ АВАТАР ПОВЕРЖЕН! СИГНАЛ ПОТЕРЯН...")
                        player.isAlive = false
                    else
                        print(" У вас осталось " .. player.health .. " HP.")
                    end
                end
            end -- конец while боя

            print("\n========================================")
            print("               БОЙ ОКОНЧЕН")
            print("========================================")
            if player.isAlive == true then
                print(" ПОБЕДА! " .. enemy.name .. " лежит у ваших ног.")
                print("Дрон повержен. Ты замечаешь на его корпусе...")
                print("... КЛЮЧ-КАРТА УРОВНЯ 1 ПОЛУЧЕНА! ...")
                player.inventory.key_cards = player.inventory.key_cards + 1
                level1_cleared = true
            else
                print(" ПОРАЖЕНИЕ. Ваш Аватар деактивирован.")
                print("...Сигнал Аватара потерян... Перезапуск протокола уровня...")
            end
            print("========================================")

        else
            print("\nПРОВАЛ. Дверь не поддаётся. Путь заблокирован.")
        end -- конец проверки силы

    -- ===== Путь 2: ТЕРМИНАЛ (проверка ТЕХНИКИ) =====
    elseif level_choice == "2" then
        print("\n>>> ВЫБОР: ТЕРМИНАЛ")
        print("Ты стираешь иней с панели. Символы древнего интерфейса вспыхивают,")
        print("предлагая запрос доступа. Это твой шанс испытать ТЕХНИКУ.")

        difficulty = math.random(10)
        print("Сложность взлома: " .. difficulty .. " | Твоя ТЕХНИКА: " .. player.tech)

        if player.tech >= difficulty then
            print("\nУСПЕХ! На экране вспыхивает: 'ДОСТУП РАЗРЕШЕН'. Замок щёлкает.")
            print("ПУТЬ ОТКРЫТ.")

            enemy.name = "Ржавый Дрон-Санитар"
            enemy.health = 30
            enemy.damage = 3
            enemy.isAlive = true

            print("\n========================================")
            print("               СИГНАЛ ТРЕВОГИ")
            print("========================================")
            print(" ПРОТИВНИК: " .. enemy.name)
            print(" ЗДОРОВЬЕ ВРАГА: " .. enemy.health)
            print("========================================")

            while player.isAlive == true and enemy.isAlive == true do
                player.actionPoints = 4
                print("\n========================================")
                print("      ХОД НАСЛЕДНИКА | ОД: " .. player.actionPoints)
                print("========================================")

                while player.actionPoints > 0 and enemy.isAlive == true do
                    if enemy.health < 0 then enemy.health = 0 end
                    print(" ГЕРОЙ: " .. player.health .. " HP  |  ВРАГ: " .. enemy.health .. " HP")

                    print("+----------------------- ДЕЙСТВИЯ -----------------------+")
                    print("|  [1] Атака (2 ОД)                                      |")
                    print("|  [2] Использовать Аптечку (3 ОД)                       |")
                    print("|  [9] Закончить ход                                     |")
                    print("+--------------------------------------------------------+")
                    io.write("> Введите номер действия: ")
                    choice = io.read()

                    if choice == "1" then
                        if player.actionPoints >= 2 then
                            player.actionPoints = player.actionPoints - 2

                            damage = 0
                            critical_hit = false
                            if math.random(100) <= player.luck then
                                critical_hit = true
                                damage = player.strength * 2
                            else
                                damage = player.strength
                            end

                            enemy.health = enemy.health - damage
                            if enemy.health < 0 then enemy.health = 0 end

                            if critical_hit == true then
                                print("\n>>> КРИТИЧЕСКИЙ УДАР! Вы нанесли " .. damage .. " урона!")
                            else
                                print("\n>>> АТАКА! Вы нанесли " .. damage .. " урона.")
                            end

                            if enemy.health <= 0 then
                                print(">>> " .. enemy.name .. " повержен!")
                                enemy.isAlive = false
                                break
                            else
                                print(" У врага осталось " .. enemy.health .. " HP.")
                            end
                        else
                            print("\n>>> НЕДОСТАТОЧНО ОД ДЛЯ АТАКИ!")
                        end

                    elseif choice == "2" then
                        if player.actionPoints >= 3 then
                            if player.inventory.aid_kits > 0 then
                                player.actionPoints = player.actionPoints - 3
                                player.inventory.aid_kits = player.inventory.aid_kits - 1

                                heal_amount = 25
                                player.health = player.health + heal_amount
                                if player.health > 100 then player.health = 100 end

                                print("\n>>> ЛЕЧЕНИЕ! Вы использовали Аптечку (+25 HP).")
                                print("Здоровье: " .. player.health .. " | Осталось аптечек: " .. player.inventory.aid_kits)
                            else
                                print("\n>>> ОШИБКА! У вас нет аптечек!")
                            end
                        else
                            print("\n>>> НЕДОСТАТОЧНО ОД ДЛЯ ИСПОЛЬЗОВАНИЯ ПРЕДМЕТА!")
                        end

                    elseif choice == "9" then
                        print("\n>>> ВЫБОР: ЗАКОНЧИТЬ ХОД!")
                        break
                    else
                        print("\n>>> НЕИЗВЕСТНАЯ КОМАНДА! Вы теряете 1 ОД.")
                        player.actionPoints = player.actionPoints - 1
                    end

                    if player.actionPoints <= 0 then
                        print("\n...Очки Действий иссякли...")
                    end
                end -- конец while действий игрока

                print("\n--- ХОД ИГРОКА ЗАВЕРШЕН ---")

                if enemy.isAlive == true then
                    print("\n...Ход " .. enemy.name .. "...")
                    damage = enemy.damage
                    player.health = player.health - damage
                    if player.health < 0 then player.health = 0 end

                    print(">>> Дрон атакует и наносит " .. damage .. " урона!")
                    if player.health <= 0 then
                        print(">>> ВАШ АВАТАР ПОВЕРЖЕН! СИГНАЛ ПОТЕРЯН...")
                        player.isAlive = false
                    else
                        print(" У вас осталось " .. player.health .. " HP.")
                    end
                end
            end -- конец while боя

            print("\n========================================")
            print("               БОЙ ОКОНЧЕН")
            print("========================================")
            if player.isAlive == true then
                print(" ПОБЕДА! " .. enemy.name .. " лежит у ваших ног.")
                print("Дрон повержен. Ты замечаешь на его корпусе...")
                print("... КЛЮЧ-КАРТА УРОВНЯ 1 ПОЛУЧЕНА! ...")
                player.inventory.key_cards = player.inventory.key_cards + 1
                level1_cleared = true
            else
                print(" ПОРАЖЕНИЕ. Ваш Аватар деактивирован.")
                print("...Сигнал Аватара потерян... Перезапуск протокола уровня...")
            end
            print("========================================")

    -- ===== Иное / ожидание =====
    else
        print("\n>>> ВЫБОР: ОЖИДАНИЕ")
        print("Ты стоишь неподвижно, и ветер воет сильнее. Нужно действовать.")
    end
end -- КОНЕЦ while уровня

print("\n>>> ПРОЕКТНАЯ ВЕХА: УРОВЕНЬ 1 ЗАВЕРШЁН.")
print("Ключ-карты: " .. player.inventory.key_cards)
end