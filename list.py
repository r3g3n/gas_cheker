from web3 import Web3
import sys
import argparse

# URL провайдеров
mainnet_provider_url = "https://eth.merkle.io"      # Ethereum
sepolia_provider_url = "https://multi-tame-rain.ethereum-sepolia.quiknode.pro/"    # Sepolia
plume_provider_url = "https://testnet-rpc.plumenetwork.xyz/http" # Plume
holesky_provider_url = "https://ethereum-holesky-rpc.publicnode.com" # Holesky
kakarot_provider_url = "https://sepolia-rpc.kakarot.org" # Kakarot
base_provider_url = "https://base-rpc.publicnode.com" # Base
op_provider_url = "https://1rpc.io/op" # Optimism
arb_provider_url = "https://arb1.arbitrum.io/rpc" # Arbitrum
story_provider_url = "https://story-rpc01.originstake.com" # Story
scroll_provider_url = "https://rpc.scroll.io" # Scroll
espresso_provider_url = "https://kyoto-rpc.altlayer.io" # Espresso Testnet
zero_provider_url = "https://rpc.zerion.io/v1/zero-sepolia" # Zero Testnet
morph_provider_url = "https://rpc-quicknode-holesky.morphl2.io" # Morph Testnet

# Подключение к сетям через Web3
web3_providers = {
    'eth': Web3(Web3.HTTPProvider(mainnet_provider_url)),
    'sepolia': Web3(Web3.HTTPProvider(sepolia_provider_url)),
    'plume': Web3(Web3.HTTPProvider(plume_provider_url)),
    'holesky': Web3(Web3.HTTPProvider(holesky_provider_url)),
    'kakarot': Web3(Web3.HTTPProvider(kakarot_provider_url)),
    'base': Web3(Web3.HTTPProvider(base_provider_url)),
    'op': Web3(Web3.HTTPProvider(op_provider_url)),
    'arb': Web3(Web3.HTTPProvider(arb_provider_url)),
    'story': Web3(Web3.HTTPProvider(story_provider_url)),
    'scroll': Web3(Web3.HTTPProvider(scroll_provider_url)),
    'espresso': Web3(Web3.HTTPProvider(espresso_provider_url)),
    'zero': Web3(Web3.HTTPProvider(zero_provider_url)),
    'morph': Web3(Web3.HTTPProvider(morph_provider_url))
}

# ANSI-коды для изменения цвета текста
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

def get_eth_balance(web3, wallet_address: str) -> float:
    """Получает баланс ETH для указанного адреса."""
    if web3.isConnected():
        # Преобразуем адрес в checksum формат
        checksum_address = web3.toChecksumAddress(wallet_address)

        # Получаем баланс
        balance_wei = web3.eth.get_balance(checksum_address)
        balance_eth = web3.fromWei(balance_wei, 'ether')
        return balance_eth
    else:
        raise ConnectionError("Не удалось подключиться к сети.")

def format_balance(balance: float) -> str:
    """Форматирует баланс с округлением до 4 знаков после запятой и выделением цветом в зависимости от величины баланса."""
    rounded_balance = round(balance, 4)
    balance_str = f"{rounded_balance:.4f}"

    if rounded_balance > 0.05:
        balance_str = f"{GREEN}{rounded_balance:.4f}{RESET}"
    elif rounded_balance == 0:
        balance_str = f"{RED}{rounded_balance:.4f}{RESET}"
    else:
        balance_str = f"{YELLOW}{rounded_balance:.4f}{RESET}"

    return balance_str

def process_accounts(file_path, networks, line_range):
    """Читает файл с адресами, проверяет баланс и выводит результат для указанных сетей."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Определение диапазона строк для обработки
            if line_range:
                start, end = map(int, line_range.split('-'))
                lines_to_process = lines[start-1:end]  # start-1 для индексации с нуля
            else:
                lines_to_process = lines
            
            for line in lines_to_process:
                name, address = line.strip().split(":")

                balances = []
                for network in networks:
                    if network in web3_providers:
                        try:
                            balance = get_eth_balance(web3_providers[network], address)
                            balance_str = format_balance(balance)
                            balances.append(f"{network.capitalize()}: {balance_str}")
                        except Exception as e:
                            balances.append(f"{network.capitalize()}: Ошибка - {e}")

                # Вывод результата в одну строку
                print(f"{name} [{address}] | {' | '.join(balances)}")
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def print_help():
    """Выводит справку по использованию скрипта."""
    print("Использование: python script.py -n <network1,network2,...> [или -all]")
    print("Опции:")
    print("  -l <start-end>  - Диапазон строк для обработки (например, '2-3')")
    print("Доступные сети:")
    print("  eth  - Cеть Ethereum")
    print("  sepolia  - Тестовая сеть Sepolia")
    print("  holesky  - Тестовая сеть Holesky")
    print("  plume    - Тестовая сеть Plume")
    print("  kakarot  - Тестовая сеть Kakarot")
    print("  story    - Тестовая сеть Story")
    print("  espresso - Тестовая сеть Espresso")
    print("  zero     - Тестовая сеть Zero")
    print("  morph    - Тестовая сеть Morph")
    print("  base     - Cеть Base")
    print("  op       - Cеть Optimism")
    print("  arb      - Cеть Arbitrum")
    print("  scroll   - Cеть Scroll")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Проверка баланса ETH на различных сетях.")
    parser.add_argument('-n', '--networks', type=str, help='Список сетей через запятую (например, "eth,sepolia,plume")')
    parser.add_argument('-l', '--lines', type=str, help='Диапазон строк для обработки (например, "2-3")')
    args = parser.parse_args()

    if args.networks:
        networks = args.networks.split(',')
        if 'all' in networks:
            networks = list(web3_providers.keys())
        elif not all(network in web3_providers for network in networks):
            print("Некоторые указанные сети недоступны. Проверьте справку с доступными сетями.")
            print_help()
            sys.exit(1)
    else:
        print_help()
        sys.exit(1)

    line_range = args.lines
    file_path = 'accs.txt'
    process_accounts(file_path, networks, line_range)
