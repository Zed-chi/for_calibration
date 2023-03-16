from terminaltables import AsciiTable


current_signals = {
    "forward_norm":[4, 8, 12, 16, 20],
    "reversed_norm":[20, 16, 12, 8, 4],
    "forward_below":[0, 5, 10, 15, 20],
    "reversed_below":[20, 15, 10, 5, 0],
}


def choose_current_signal():        
    if input("Выход тока в сторону увеличения [4-20][0-20]? [y-n]: ").lower() == "y":
        flow = "forward_"        
    else:
        flow = "reversed_"

    if input("Диапазон тока от 4мА? [y-n]: ").lower() == "y":
        signal_name = flow + "norm"
    else:
        signal_name = flow + "below"
    return current_signals[signal_name]


def main():
    cur_list = choose_current_signal()
    low = float(input("Нижний предел единиц измерения: "))
    high = float(input("Верхний предел единиц измерения: "))
    span = max(low, high) - min(low, high)
    step = span / 4
    pressures = []

    if low < high:
        count = low
        for i in range(5):
            pressures.append(count)
            count += step
    else:
        count = high
        for i in range(5):
            pressures.append(count)
            count -= step
    print(pressures)
    results = {str(x): {} for x in pressures}
    for i in range(5):
        pres = str(pressures[i])
        input_cur = float(input(f"Ток при давлении {pres}: "))
        table_cur = cur_list[i]
        dev = round((input_cur - table_cur) / 16 * 100, 3)
        results[pres]["up"] = {"table": table_cur, "real": input_cur, "dev": dev}
        print(f" - Отклонение {input_cur} от {table_cur} = {dev}")

    for i in [*range(5)][::-1]:
        pres = str(pressures[i])
        input_cur = float(input(f"Ток при давлении {pres}: "))
        table_cur = cur_list[i]
        dev = round((input_cur - table_cur) / 16 * 100, 3)
        results[pres]["down"] = {"table": table_cur, "real": input_cur, "dev": dev}
        print(f" - Отклонение {input_cur} от {table_cur} = {dev}")

    for i in range(5):
        pres = str(pressures[i])
        results[pres]["var"] = round(
            abs(results[pres]["down"]["dev"] - results[pres]["up"]["dev"]), 3
        )
    data = []
    headers = ["Давл", "мА↓", "▲мА↓", "▲", "мА↑", "▲мА↑", "▲", "Вар"]
    data.append(headers)
    for i in pressures:
        pres = str(i)
        data.append(
            [
                pres,
                results[pres]["down"]["table"],
                results[pres]["down"]["real"],
                results[pres]["down"]["dev"],
                results[pres]["up"]["table"],
                results[pres]["up"]["real"],
                results[pres]["up"]["dev"],
                results[pres]["var"],
            ]
        )

    table = AsciiTable(data, title="Измерения")

    print("\n", table.table)


if __name__ == "__main__":
    main()