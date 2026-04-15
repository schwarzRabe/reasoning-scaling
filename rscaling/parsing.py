"""Извлечение ответов из текста модели и сравнение с эталоном.

Код сравнения ответов — из оригинальных evaluation-скриптов:
    GSM8K:  openai/grade-school-math  (Cobbe et al., 2021)
    MATH:   hendrycks/math            (Hendrycks et al., 2021)

Верифицировано в 00_setup.ipynb: тесты + проверка совпадения
результатов с оригинальными пакетами.
"""

import re
import numpy as np

ANS_RE = re.compile(r"#### (\-?[0-9\.\,]+)")


def extract_answer_gsm8k(text):
    '''Находит #### в тексте, возвращает число после него.
    Источник: openai/grade-school-math/dataset.py:extract_answer'''
    match = ANS_RE.search(text)
    if match:
        return match.group(1).strip().replace(",", "")
    return None


def is_correct_gsm8k(prediction, target):
    '''GSM8K: строковое сравнение после strip.'''
    if prediction is None:
        return False
    return prediction.strip() == target.strip()


def last_boxed_only_string(text):
    '''Находит последний \\boxed{...} или \\fbox{...}.
    Считает вложенные скобки. Возвращает подстроку или None.'''
    idx = text.rfind('\\boxed')
    if idx < 0:
        idx = text.rfind('\\fbox')
        if idx < 0:
            return None
    i = idx
    depth = 0
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[idx : i + 1]
        i += 1
    return None


def remove_boxed(text):
    '''Убирает \\boxed{} обёртку: \\boxed{42} -> 42'''
    left = '\\boxed{'
    try:
        assert text[:len(left)] == left
        assert text[-1] == '}'
        return text[len(left):-1]
    except Exception:
        return None


def extract_answer_math(text):
    '''Извлекает ответ из последнего \\boxed{...} в тексте.'''
    boxed = last_boxed_only_string(text)
    if boxed is None:
        return None
    return remove_boxed(boxed)


def accuracy(correct):
    '''Доля правильных.'''
    if len(correct) == 0:
        return 0.0
    return sum(correct) / len(correct)


def bootstrap_ci(correct, n_bootstrap=10000, confidence=0.95, seed=42):
    '''Bootstrap 95% CI для accuracy. Возвращает (mean, lower, upper).'''
    rng = np.random.RandomState(seed)
    arr = np.array(correct, dtype=float)
    n = len(arr)
    if n == 0:
        return (0.0, 0.0, 0.0)
    means = np.array([
        rng.choice(arr, size=n, replace=True).mean()
        for _ in range(n_bootstrap)
    ])
    alpha = (1 - confidence) / 2
    lower = float(np.percentile(means, 100 * alpha))
    upper = float(np.percentile(means, 100 * (1 - alpha)))
    return (float(arr.mean()), lower, upper)


def _fix_fracs(string):
    substrs = string.split("\\frac")
    new_str = substrs[0]
    if len(substrs) > 1:
        substrs = substrs[1:]
        for substr in substrs:
            new_str += "\\frac"
            if substr[0] == "{":
                new_str += substr
            else:
                try:
                    assert len(substr) >= 2
                except:
                    return string
                a = substr[0]
                b = substr[1]
                if b != "{":
                    if len(substr) > 2:
                        post_substr = substr[2:]
                        new_str += "{" + a + "}{" + b + "}" + post_substr
                    else:
                        new_str += "{" + a + "}{" + b + "}"
                else:
                    if len(substr) > 2:
                        post_substr = substr[2:]
                        new_str += "{" + a + "}" + b + post_substr
                    else:
                        new_str += "{" + a + "}" + b
    string = new_str
    return string


def _fix_a_slash_b(string):
    if len(string.split("/")) != 2:
        return string
    a = string.split("/")[0]
    b = string.split("/")[1]
    try:
        a = int(a)
        b = int(b)
        assert string == "{}/{}".format(a, b)
        new_string = "\\frac{" + str(a) + "}{" + str(b) + "}"
        return new_string
    except:
        return string


def _remove_right_units(string):
    # "\\text{ " only ever occurs (at least in the val set) when describing units
    if "\\text{ " in string:
        splits = string.split("\\text{ ")
        assert len(splits) == 2
        return splits[0]
    else:
        return string


def _fix_sqrt(string):
    if "\\sqrt" not in string:
        return string
    splits = string.split("\\sqrt")
    new_string = splits[0] 
    for split in splits[1:]:
        if split[0] != "{":
            a = split[0]
            new_substr = "\\sqrt{" + a + "}" + split[1:]
        else:
            new_substr = "\\sqrt" + split
        new_string += new_substr
    return new_string


def _strip_string(string):
    # linebreaks  
    string = string.replace("\n", "")
    #print(string)

    # remove inverse spaces
    string = string.replace("\\!", "")
    #print(string)

    # replace \\ with \
    string = string.replace("\\\\", "\\")
    #print(string)

    # replace tfrac and dfrac with frac
    string = string.replace("tfrac", "frac")
    string = string.replace("dfrac", "frac")
    #print(string)

    # remove \left and \right
    string = string.replace("\\left", "")
    string = string.replace("\\right", "")
    #print(string)
    
    # Remove circ (degrees)
    string = string.replace("^{\\circ}", "")
    string = string.replace("^\\circ", "")

    # remove dollar signs
    string = string.replace("\\$", "")
    
    # remove units (on the right)
    string = _remove_right_units(string)

    # remove percentage
    string = string.replace("\\%", "")
    string = string.replace("\%", "")

    # " 0." equivalent to " ." and "{0." equivalent to "{." Alternatively, add "0" if "." is the start of the string
    string = string.replace(" .", " 0.")
    string = string.replace("{.", "{0.")
    # if empty, return empty string
    if len(string) == 0:
        return string
    if string[0] == ".":
        string = "0" + string

    # to consider: get rid of e.g. "k = " or "q = " at beginning
    if len(string.split("=")) == 2:
        if len(string.split("=")[0]) <= 2:
            string = string.split("=")[1]

    # fix sqrt3 --> sqrt{3}
    string = _fix_sqrt(string)

    # remove spaces
    string = string.replace(" ", "")

    # \frac1b or \frac12 --> \frac{1}{b} and \frac{1}{2}, etc. Even works with \frac1{72} (but not \frac{72}1). Also does a/b --> \\frac{a}{b}
    string = _fix_fracs(string)

    # manually change 0.5 --> \frac{1}{2}
    if string == "0.5":
        string = "\\frac{1}{2}"

    # NOTE: X/Y changed to \frac{X}{Y} in dataset, but in simple cases fix in case the model output is X/Y
    string = _fix_a_slash_b(string)

    return string


def is_equiv(str1, str2, verbose=False):
    if str1 is None and str2 is None:
        print("WARNING: Both None")
        return True
    if str1 is None or str2 is None:
        return False

    try:
        ss1 = _strip_string(str1)
        ss2 = _strip_string(str2)
        if verbose:
            print(ss1, ss2)
        return ss1 == ss2
    except:
        return str1 == str2
