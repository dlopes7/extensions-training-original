import requests
import random
import time
import autodynatrace


@autodynatrace.trace
def call_ship():
    url = f"http://192.168.0.{random.randint(1, 30)}"
    try:
        print(requests.get(url, timeout=5))
    except Exception as e:
        print(e)


def main():
    while True:
        call_ship()
        time.sleep(5)


if __name__ == '__main__':
    main()
