from selenium import webdriver
import os

driver = webdriver.Chrome('C:\chromedriver.exe')

def main():
    tankStatistics = []
    tankman = 'goldaxe10' #input("Введите ник игрока, которого будем парсить: ")
    try:
        os.mkdir(r'C:\tankstats')
        print(r'Папка успешно создана C:\tankstats')
    except:
        print(r'Папка уже создана в директории C:\tankstats')
    driver.get('https://worldoftanks.ru/ru/community/accounts/#wot&at_search={}'.format(tankman))
    nickname = driver.find_element_by_xpath("//*[@data-bind='attr: {href: profileUrl}']").text
    cntBattles = driver.find_element_by_xpath("//*[@data-bind='text: formattedBattles']").text
    winratio = driver.find_element_by_xpath("//*[@data-bind='text: formattedWinsRatio']").text
    exp = driver.find_element_by_xpath("//*[@data-bind='text: formattedExperience']").text

    print(
        "Результаты поиска для {0}:\n Никнейм: {1} | Количество боёв: {2} | Винрейт: {3} | "
        "Количество опыта {4}".format(tankman, nickname, cntBattles, winratio, exp)
    )

    # Кликаем по нику игрока, чтобы перейти в его статистику
    driver.find_element_by_xpath("//*[@data-bind='attr: {href: profileUrl}']").click()
    driver.implicitly_wait(10)
    # Разворачиваем список с танками. Самое долгое
    driver.find_element_by_xpath("//a[@class='link-more link-more__no-arrow']").click()
    # Ожидание, пока элемент "spinner-box" перейдёт в режим отображения "display: none;"
    driver.implicitly_wait(100)
    x = driver.find_element_by_xpath('//div[@class="spinner-box spinner-box__size4" and @style="display: none;"]')
    # Получаем список танков игрока
    tankList = driver.find_elements_by_xpath(
         "//div[@data-bind='outsideClick: {visible: vehicle.isAchievementsVisible, "
         "callback: vehicle.bindedClosePopover}']")
    # Получаем статистику танков в список
    for tank in tankList:
        tankStats = ''
        for i in tank.text:
            if i == '–' or i == '%':
                continue
            else:
                tankStats += str(i)
        tankStatsList = tankStats.splitlines()

        # нужный костыль
        for i in tankStatsList:
            if i == '':
                tankStatsList.remove(i)
        for i in tankStatsList:
            if i == '':
                tankStatsList.remove(i)

        tankStatistics.append(tankStatsList)

    driver.quit()

    # Вёрстка html-таблицы и запись в неё данных статистики
    with open(r'C:\tankstats\index.html','a', encoding='utf-8') as tankmanInformation:
        tankmanInformation.write(
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML  4.01//EN" "http://www.w3.org/TR/html4/strict.dtd>\n'
            '\t<head>\n'
            '\t\t<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n'
            '\t\t<title>Танкист {0}</title>\n'
            '\t</head>\n'
            '\t<body>\n'
            '\t\t<table border="1" width="100%" cellpadding="5">\n'
            '\t\t\t<tr>\n'
            '\t\t\t\t<th>Никнейм {1}</th>\n'
            '\t\t\t\t<th>Количество боёв {2}</th>\n'
            '\t\t\t\t<th>Винрейт {3}</th>\n'
            '\t\t\t\t<th>Опыт {4}</th>\n'
            '\t\t\t</tr>\n'
            '\t\t\t<tr>\n'
            '\t\t\t\t<th>Уровень технки</th>\n'
            '\t\t\t\t<th>Название технки</th>\n'
            '\t\t\t\t<th>Количество боёв</th>\n'
            '\t\t\t\t<th>Винрейт</th>\n'
            '\t\t\t\t<th>Средний урон</th>\n'
            '\t\t\t\t<th>Средний опыт</th>\n'
            '\t\t\t\t<th>K/D</th>\n'
            '\t\t\t</tr>\n'.format(tankman, nickname, cntBattles, winratio, exp)
        )

        for stats in tankStatistics:
            tankmanInformation.write(
                '\t\t\t<tr>\n'
            )

            for i in  stats:
                tankmanInformation.write(
                    '\t\t\t\t<th>{}</th>\n'.format(str(i))
                )
            tankmanInformation.write(
                '\t\t\t</tr>\n'
            )

        tankmanInformation.write(
            '\t\t</table>\n'
            '\t</body>\n'
            '</html>\n'
        )


if __name__== '__main__':
    main()




