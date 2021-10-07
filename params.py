class ScriptParam:
    def __init__(self, name: str, flag: str = "", value: str = ""):
        self.name = name
        self.flag = flag
        self.value = value

    def __repr__(self):
        return "{} {}".format(self.flag, self.value).strip()


if __name__ == '__main__':
    pass
