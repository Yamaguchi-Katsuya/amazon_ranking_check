from colorama import Fore
from amazon import AmazonOperation


def ranking_check():
    print(Fore.BLUE + "ランキングチェック処理を開始します\n")
    print(Fore.WHITE)
    amazon_operation = AmazonOperation()
    try:
        amazon_operation.driver_start()
        is_ranking = amazon_operation.ranking_check()
        if is_ranking:
            print(Fore.BLUE + "ランキング圏内です！\n")
            amazon_operation.take_ranking_screen_shot()
        else:
            print(Fore.YELLOW + "ランキング圏外でした...\n")
    except Exception as e:
            print(Fore.RED + f"\nmessage: {e}\n" )
    finally:
        amazon_operation.driver_close()


if __name__ == '__main__':
    ranking_check()