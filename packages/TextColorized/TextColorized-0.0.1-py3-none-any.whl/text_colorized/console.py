class TextColor:
    import os
    os.system('color')
    __HEADER = '\033[95m'
    __OKBLUE = '\033[94m'
    __OKCYAN = '\033[96m'
    __OKGREEN = '\033[92m'
    __WARNING = '\033[93m'
    __FAIL = '\033[91m'
    __ENDC = '\033[0m'
    __BOLD = '\033[1m'
    __UNDERLINE = '\033[4m'

    def warning(self, m):
        print(f"{self.__WARNING}{m}{self.__ENDC}")

    def header(self, m):
        m_len = (len(m)+6)
        print(f"{self.__HEADER}{'=' * m_len}{self.__ENDC}")
        print(f"{self.__HEADER}|| {m} ||{self.__ENDC}")
        print(f"{self.__HEADER}{'=' * m_len }{self.__ENDC}")

    def footer(self, m):
        m_len = (len(m)+6)
        print(f"{self.__OKCYAN}{'=' * m_len}{self.__ENDC}")
        print(f"{self.__OKCYAN}|| {m} ||{self.__ENDC}")
        print(f"{self.__OKCYAN}{'=' * m_len }{self.__ENDC}")

    def underline(self, m):
        print(f"{self.__UNDERLINE}{m}{self.__ENDC}")

    def blue(self, m):
        print(f"{self.__UNDERLINE}{' ' * len(m)}{self.__ENDC}")
        print(f"{self.__OKBLUE}{m}{self.__ENDC}")

    def cyan(self, m):
        print(f"{self.__OKCYAN}{m}{self.__ENDC}")

    def fail(self, m: str):
        print(f"{self.__FAIL}{m}{self.__ENDC}")

    def assertion(self, m: str):
        print(f"{self.__OKGREEN}{m}{self.__ENDC}")

    def bold(self, m: str):
        print(f"{self.__BOLD}{m}{self.__ENDC}")

    def print(self, m: str):
        print(f"{m}")


console = TextColor()
