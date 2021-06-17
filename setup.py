import os


def write_dot_env_file(env_file):
    with open(env_file) as f:
        for line in f:
            k, v = line.partition("=")[::2]
            # print('{}:{}'.format(k, v))
            os.environ[k.strip()] = v.rstrip("\n")


def main():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.isfile(env_file):
        write_dot_env_file(env_file)
    else:
        pass


if __name__ == "__main__":
    main()
