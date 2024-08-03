from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def get_user_input(prompt):
    return input(prompt)

def search_wikipedia(browser, query):
    search_url = "https://ru.wikipedia.org/wiki/{}".format(query)
    browser.get(search_url)

def list_paragraphs(browser):
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    for i, paragraph in enumerate(paragraphs):
        print(f"Параграф {i + 1}: {paragraph.text}\n")
        user_input = get_user_input("Введите 'n' для следующего параграфа или 'q' для выхода: ").strip().lower()
        if user_input == 'q':
            break

def list_internal_links(browser):
    links = browser.find_elements(By.XPATH, "//div[@id='bodyContent']//a[@href]")
    internal_links = [link for link in links if link.get_attribute("href").startswith("https://ru.wikipedia.org/wiki/")]

    for i, link in enumerate(internal_links):
        print(f"Ссылка {i + 1}: {link.text} - {link.get_attribute('href')}")

    return internal_links

def main():
    browser = webdriver.Firefox()

    try:
        initial_query = get_user_input("Введите запрос для поиска на Википедии: ")
        search_wikipedia(browser, initial_query)

        while True:
            user_action = get_user_input(
                "Выберите действие: \n1. Листать параграфы текущей статьи\n2. Перейти на одну из связанных страниц\n3. Выйти из программы\nВведите номер действия: ").strip()

            if user_action == '1':
                list_paragraphs(browser)
            elif user_action == '2':
                internal_links = list_internal_links(browser)

                link_choice = int(get_user_input("Введите номер ссылки для перехода: ").strip())
                if 1 <= link_choice <= len(internal_links):
                    browser.get(internal_links[link_choice - 1].get_attribute("href"))

                    while True:
                        sub_action = get_user_input(
                            "Выберите действие: \n1. Листать параграфы статьи\n2. Перейти на одну из внутренних статей\nВведите номер действия: ").strip()

                        if sub_action == '1':
                            list_paragraphs(browser)
                            break
                        elif sub_action == '2':
                            internal_links = list_internal_links(browser)
                            link_choice = int(get_user_input("Введите номер ссылки для перехода: ").strip())
                            if 1 <= link_choice <= len(internal_links):
                                browser.get(internal_links[link_choice - 1].get_attribute("href"))
                            else:
                                print("Неправильный выбор ссылки.")
                        else:
                            print("Неправильный ввод, попробуйте снова.")
            elif user_action == '3':
                break
            else:
                print("Неправильный ввод, попробуйте снова.")
    finally:
        browser.quit()

if __name__ == "__main__":
    main()