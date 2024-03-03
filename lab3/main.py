if __name__ == "__main__":
    dict = {}

    known_numbers = [89156311602, 89678395615, 89859771985, 89109807351, 89108471943]
    numbers = []

    with open("decrypted.txt") as file:
        for line in file:
            my_number = int(line.split(":")[1])
            numbers.append(my_number)

            for his_number in known_numbers:
                salt = my_number - his_number

                if salt not in dict:
                    dict[salt] = 0

                dict[salt] += 1

    key = list(filter(lambda k: dict[k] == 5, dict))[0]
    print(f"Salt: {key}")

    with open("decrypted_numbers.txt", "w") as file:
        file.write("\n".join(map(lambda num: str(num - key), numbers)))
