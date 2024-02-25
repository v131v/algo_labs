import datetime
import re
import pandas


def maskerization_passport(passport: str) -> str:
    return passport[:2] + re.sub(r"\d", "*", passport[2:])


def generalization_doctor(doctor: str) -> str:
    doctor_types = [
        [
            "Аллерголог",
            "Анестезиолог",
            "Гастроэнтеролог",
            "Гериатр",
            "Гистолог",
            "Гинеколог",
            "Гематолог",
            "Гематолог",
            "Генетик",
            "Дерматолог",
        ],
        [
            "Иглорефлексотерапевт",
            "Иммунолог",
            "Иммуногенетик",
            "Иммунотерапевт",
            "Инфекционист",
            "Кардиолог",
            "Кардиоревматолог",
            "Кардиохирург",
            "Косметолог",
            "Кинезиотерапевт",
        ],
        [
            "Клинический психолог",
            "Клинический фармаколог",
            "Мануальный терапевт",
            "Медицинский генетик",
            "Невролог",
            "Неонатолог",
            "Нефролог",
            "Онколог",
            "Ортопед",
            "Оториноларинголог",
        ],
        [
            "Офтальмолог",
            "Педиатр",
            "Пластический хирург",
            "Проктолог",
            "Психиатр",
            "Психотерапевт",
            "Пульмонолог",
            "Ревматолог",
            "Рентгенолог",
            "Сексолог",
        ],
        [
            "Стоматолог",
            "Судебный медик",
            "Терапевт",
            "Травматолог",
            "Уролог",
            "Физиотерапевт",
            "Флеболог",
            "Хирург",
            "Эндокринолог",
            "Эпидемиолог",
        ],
    ]

    for i, t in enumerate(doctor_types):
        if doctor in t:
            return f"doctor_type_{i}"


def generalization_date_start(date_start: str) -> str:
    timestamp = datetime.datetime.strptime(date_start, "%Y-%m-%dT%H:%M")
    m = timestamp.month % 12
    if m <= 2:
        return "Winter"
    elif m <= 5:
        return "Spring"
    elif m <= 8:
        return "Summer"
    else:
        return "Autem"


def aggregation_price(price: str) -> str:
    return str((int(price) // 2500) * 2500)


def generalization_card(card: str) -> str:
    code_to_bank = {
        "547948": "MC",
        "427680": "VISA",
        "220220": "MIR",
        "524468": "MC",
        "437772": "VISA",
        "220070": "MIR",
        "542104": "MC",
        "418868": "VISA",
        "220024": "MIR",
        "510126": "MC",
        "410584": "VISA",
        "220215": "MIR",
    }
    return code_to_bank[card.replace(" ", "")[:6]]


def aggregate(seq: str) -> str:
    seq = seq.split("|")
    seq.sort()
    return seq[-1]


def anonimyze(df: pandas.DataFrame) -> pandas.DataFrame:
    df = df.drop("Name", axis=1)
    df["Passport"] = df["Passport"].apply(maskerization_passport)
    df = df.drop("Snils", axis=1)

    df["Doctor"] = df["Doctor"].apply(generalization_doctor)
    df["Symptoms"] = df["Symptoms"].apply(aggregate)
    df["Analyzis"] = df["Analyzis"].apply(aggregate)

    df["DateStart"] = df["DateStart"].apply(generalization_date_start)
    df = df.drop("DateEnd", axis=1)

    df["Price"] = df["Price"].apply(aggregation_price)
    df["Card"] = df["Card"].apply(generalization_card)

    return df


def calc_k_anonymity(df: pandas.DataFrame, cols):
    k = 1
    if len(df) < 51000:
        k = 10
    elif len(df) < 105000:
        k = 7
    elif len(df) < 260000:
        k = 5

    values = df.groupby(cols).size().reset_index(name="Count")

    bad_val = {"total": 0}
    k_anon = list()
    deleted = 0
    max_deletions = int(len(values) * 0.05)

    for _, v in values.iterrows():
        cnt = v["Count"]
        # k_anon = min(max(cnt, k), k_anon)
        k_anon.append(cnt)
        if cnt == 1 and deleted < max_deletions:
            deleted += 1
            continue

        if cnt < k:
            cnt = str(cnt)
            if cnt not in bad_val:
                bad_val[cnt] = 0
            bad_val[cnt] += 1
            bad_val["total"] += 1

    to_delete = values[values["Count"] == 1].index.tolist()
    to_delete = to_delete[:max_deletions]
    # values.drop(to_delete, inplace=True)

    k_anon.sort()

    return (
        bad_val,
        values[values["Count"] == 1][: int(len(k_anon) * 0.05)],
        k_anon[int(len(k_anon) * 0.95)],
    )
