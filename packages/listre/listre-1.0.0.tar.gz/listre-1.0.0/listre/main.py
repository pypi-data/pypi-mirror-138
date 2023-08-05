import re

"""
reモジュールがクッソ便利だからなんかそれをリスト対応させたらめちゃくちゃ強くね？（小並感）から生まれたモジュール
"""

def search(pattern: list or str, search: list or str) -> tuple or None:
    """pattern: 検索する文字列/正規表現のやつです。\n
    search: 検索対象の文字列/リストです。
    return: 検索に引っかかった場合はtupleが帰ってきます。\n
    (patternリストのどこか, searchリストのどこか, マッチオブジェクト)\n\n
    検索に引っかからなかった場合はNoneが帰ってきます。\n\n
    また、どちらかがリストまたは文字列ではない場合にもNoneが帰ってきます。
    """
    if type(pattern) == list:
        if type(search) == list:
            for i in range(len(search)):
                for j in range(len(pattern)):
                    if re.search(pattern[j], search[i]):
                        return (i, j, re.search(pattern[j], search[i]))
            return None
        elif type(search) == str:
            for j in range(len(pattern)):
                if re.search(pattern[j], search):
                    return (0, j, re.search(pattern[j], search))
            return None
        else:
            return None
    elif type(pattern) == str:
        if type(search) == list:
            for i in range(len(search)):
                if re.search(pattern,search[i]):
                    return (i, 0, re.search(pattern,search[i]))
            return None
        elif type(search) == str:
            if re.search(pattern,search):
                return (0, 0, re.search(pattern,search))
            return None
    else:
        return None