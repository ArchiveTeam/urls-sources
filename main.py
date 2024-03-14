from queuer import Lists, Queuer


def main():
    lists = Lists(directory='.', interval=60)
    lists.daemon = True
    lists.start()
    queuer_ = Queuer(lists=lists, interval=10)
    queuer_.daemon = True
    queuer_.start()
    lists.join()
    queuer_.join()

if __name__ == '__main__':
    main()

