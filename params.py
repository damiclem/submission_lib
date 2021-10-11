class ScriptParam:
    def __init__(self, name: str, flag: str = "", value: str = "", required: bool = False):
        self.name = name
        self.flag = flag
        self.value = value
        self.required = required

    def __repr__(self):
        return "{} {}".format(self.flag, self.value).strip()


if __name__ == '__main__':
    pass
