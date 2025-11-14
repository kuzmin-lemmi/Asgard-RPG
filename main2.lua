-- МОДУЛЬ 1: ПРОТОКОЛ "АВАТАР"
-- Урок 4: Финальное Досье

-- --- Инициализация Аватара ---
io.write("...Протокол 'Аватар' активен...")
io.write("\n...Запрашиваю идентификацию Наследника...")
io.write("\nВведите ваше имя: ") 
characterName = io.read() 

-- --- Статические данные ---
health = 100
actionPoints = 5 -- Очки Действий (ОД) для боя
isAlive = true

-- --- Распределение Очков Навыков ---
skillPoints = 10 
strength = 1
tech = 1
luck = 1

print("\nДобро пожаловать, " .. characterName .. "!") 
print("У вас есть " .. skillPoints .. " очков для распределения.")
print("Ваши базовые характеристики: СИЛА [1], ТЕХНИКА [1], УДАЧА [1].")

-- 3. Распределяем СИЛУ
io.write("Сколько очков (из " .. skillPoints .. ") вложить в СИЛУ? ")
pointsToAdd_text = io.read() 
pointsToAdd = tonumber(pointsToAdd_text) 

strength = strength + pointsToAdd 
skillPoints = skillPoints - pointsToAdd 

-- 4. Распределяем ТЕХНИКУ
print("...Осталось " .. skillPoints .. " очков...")
io.write("Сколько очков вложить в ТЕХНИКУ? ")
pointsToAdd_text = io.read()
pointsToAdd = tonumber(pointsToAdd_text) 

tech = tech + pointsToAdd 
skillPoints = skillPoints - pointsToAdd 

-- 5. Распределяем УДАЧУ
print("...Осталось " .. skillPoints .. " очков...")
io.write("Сколько очков вложить в УДАЧУ? ")
pointsToAdd_text = io.read() 
pointsToAdd = tonumber(pointsToAdd_text) 

luck = luck + pointsToAdd 
skillPoints = skillPoints - pointsToAdd


-- --- ФИНАЛЬНОЕ ДОСЬЕ ПЕРСОНАЖА ---
print("\n========================================")
print("    ПРОТОКОЛ 'АВАТАР' ЗАВЕРШЕН")
print("    ДОСЬЕ НАСЛЕДНИКА АКТИВИРОВАНО")
print("========================================")
print(" ИМЯ: " .. characterName)
print(" ЗДОРОВЬЕ: " .. health)
print(" ОЧКИ ДЕЙСТВИЙ: " .. actionPoints)
print("----------------------------------------")
print(" ХАРАКТЕРИСТИКИ С.Т.У.")
print("    СИЛА (СИЛ): " .. strength)
print("    ТЕХНИКА (ТЕХ): " .. tech)
print("    УДАЧА (УДЧ): " .. luck)
print("----------------------------------------")
print(" ОСТАЛОСЬ ОЧКОВ НАВЫКОВ: " .. skillPoints)
print("========================================")