#gas_cheker
Чекает газ в заданных сетях, показывает выделяет цветом елси недостаточно газа, софт создан для отработки тестнетов.

    # Форматируем баланс
    if rounded_balance > 0.05:
        balance_str = f"{GREEN}{balance_str}{RESET}"
    elif 0.0001 <= rounded_balance < 0.0009:
        balance_str = f"{YELLOW}{balance_str}{RESET}"
    elif rounded_balance == 0.0000:
        balance_str = f"{RED}{balance_str}{RESET}"
    else:
        balance_str = f"{balance_str}"


Использование:

<img width="602" alt="Снимок экрана 2024-09-10 в 15 52 53" src="https://github.com/user-attachments/assets/6d310c67-d6f0-49d9-af71-879aabd7ef97">

Пример работы:

![image](https://github.com/user-attachments/assets/c97dcde0-667c-46ad-8fb5-b7a47ffa7e53)

