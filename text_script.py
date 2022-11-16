from faker import Faker

faker = Faker()
while True:
    s = faker.unique.sentence(6)
    print(s)
    if len(s) >= 1000:
        break
