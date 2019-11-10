import re

# inputStr = "hello 111 world 111"
# replacedStr = re.sub("\d+", "222", inputStr)
# inputStr = "hello crifan, nihao crifan"
# replacedStr = re.sub(r"hello (\w+), nihao \1", "crifanli", inputStr)
# print("replacedStr=", replacedStr)      # crifanli


def pythonReSubDemo():
    """
        demo Pyton re.sub
    """
    inputStr = "hello 123 world 456"

    def _add111(matched):
        print(matched)
        intStr = matched.group("number")  # 123
        intValue = int(intStr)
        addedValue = intValue + 111  # 234
        addedValueStr = str(addedValue)
        return addedValueStr

    replacedStr = re.sub("(?P<number>\d+)", _add111, inputStr)
    print("replacedStr=", replacedStr)  # hello 234 world 567


if __name__ == "__main__":
    pythonReSubDemo()