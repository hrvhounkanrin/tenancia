import os
import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)



def main():
    # reading .env file
    # environ.Env.read_env()
    pass


if __name__ == "__main__":
    main()
