import csv
import os
from transformers import pipeline


model_names = {
    "RoBERTa": "cardiffnlp/twitter-roberta-base-sentiment-latest",
    "DistilBERT": "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
}

loaded_models = {}

reviews = [
    "The application works perfectly. I use it every day.",
    "The delivery was late, and the package was damaged.",
    "The product is acceptable, but nothing special.",
    "Excellent customer support and fast service!",
    "The software crashes every time I open it.",
    "The headphones have clear sound and comfortable ear cushions.",
    "I am disappointed with the quality of this product.",
    "The website is easy to navigate and looks modern.",
    "The food arrived cold and tasted terrible.",
    "The staff were friendly and helped me solve the problem.",
    "The battery lasts much longer than I expected.",
    "This is the worst purchase I have made this year.",
    "The service was fine, but the price was a little high.",
    "Setup was simple, and everything worked on the first try.",
    "The instructions are confusing and difficult to follow.",
    "I love the design, and the product feels very durable.",
    "The order arrived two days earlier than expected.",
    "The camera quality is poor in low light.",
    "Nothing was wrong with the item, but it did not impress me.",
    "Customer support ignored my messages for several days.",
    "The new update fixed the bugs and improved performance.",
    "The chair is uncomfortable after sitting for an hour.",
    "The subscription is affordable and offers great value.",
    "The app is slow and drains my phone battery.",
    "The hotel room was clean, quiet, and comfortable.",
    "The product stopped working after only one week.",
    "The packaging was neat, and the item matched the description.",
    "The meal was okay, although the portions were small.",
    "I received the wrong item and had to return it.",
    "The course was informative, engaging, and well organized.",
    "The printer works as expected, with no major issues.",
    "I would not recommend this service to anyone.",
    "The screen is bright, sharp, and easy to read.",
    "The repair took longer than promised, but the result is good.",
    "The price is reasonable for the features provided.",
    "The instructions were clear, and installation took ten minutes.",
    "The sound quality is average, and the controls feel cheap.",
    "I had a wonderful experience from start to finish.",
    "The product looks nice, but it does not work properly.",
    "The support team resolved my issue quickly and professionally."
]

# Приклади для додаткового дослідження
special_types = ["Короткий", "Довгий", "Саркастичний", "Суперечливий"]
special_reviews = [
    "Great!",
    "I purchased this laptop a month ago and have been using it every day. "
    "The display is sharp, the keyboard feels comfortable, and most tasks run smoothly. "
    "However, the fan is loud, the battery runs out much sooner than advertised, "
    "and the customer service team has not answered my emails. "
    "Overall, I have both positive and negative impressions.",
    "Fantastic! The app deleted all my files again. Exactly what I needed.",
    "I love the design, but the product is unreliable and breaks constantly."
]


def analyze(texts, model_name):

    if model_name not in loaded_models:
        print("\nЗавантаження моделі", model_name, "...")
        loaded_models[model_name] = pipeline(
            "text-classification",
            model=model_names[model_name],
            device=-1
        )

    model = loaded_models[model_name]
    predictions = model(texts, truncation=True, max_length=512)
    results = []

    for i in range(len(texts)):
        label = predictions[i]["label"]
        confidence = round(predictions[i]["score"] * 100, 2)


        if label == "LABEL_0":
            label = "Negative"
        elif label == "LABEL_1":
            if model_name == "RoBERTa":
                label = "Neutral"
            else:
                label = "Positive"
        elif label == "LABEL_2":
            label = "Positive"
        else:
            label = label.capitalize()

        results.append({
            "text": texts[i],
            "label": label,
            "confidence": confidence
        })

    return results


def show_results(results, model_name):
    print("\n--- Результати:", model_name, "---")
    for i in range(len(results)):
        result = results[i]
        print("\n", i + 1, ". ", result["text"], sep="")
        print("    Тональність:", result["label"])
        print("    Впевненість:", str(result["confidence"]) + "%")


def count_results(results):
    positive = 0
    negative = 0
    neutral = 0

    for result in results:
        if result["label"] == "Positive":
            positive += 1
        elif result["label"] == "Negative":
            negative += 1
        elif result["label"] == "Neutral":
            neutral += 1

    return positive, negative, neutral


def show_statistics(results, model_name):
    positive, negative, neutral = count_results(results)
    print("\n--- Статистика:", model_name, "---")
    print("Усього відгуків:", len(results))
    print("Позитивних:", positive)
    print("Негативних:", negative)

    if model_name == "RoBERTa":
        print("Нейтральних:", neutral)
    else:
        print("Нейтральних: модель не підтримує цей клас")


def save_csv(results, model_name, category):

    new_file = not os.path.exists("results.csv")
    encoding = "utf-8"
    if new_file:
        encoding = "utf-8-sig"

    with open("results.csv", "a", encoding=encoding, newline="") as file:
        writer = csv.writer(file)

        if new_file:
            writer.writerow(["model", "category", "text", "sentiment", "confidence_percent"])

        for result in results:
            writer.writerow([
                model_name,
                category,
                result["text"],
                result["label"],
                result["confidence"]
            ])

    print("Результати додано у results.csv")


def compare_models(texts, category):
    first = analyze(texts, "RoBERTa")
    second = analyze(texts, "DistilBERT")
    differences = 0

    print("\n--- Порівняння двох моделей ---")
    for i in range(len(texts)):
        print("\n", i + 1, ". ", texts[i], sep="")
        print("  RoBERTa:   ", first[i]["label"], "(", first[i]["confidence"], "%)")
        print("  DistilBERT:", second[i]["label"], "(", second[i]["confidence"], "%)")

        if first[i]["label"] != second[i]["label"]:
            differences += 1
            print("  >>> РІЗНІ РЕЗУЛЬТАТИ")

    show_statistics(first, "RoBERTa")
    show_statistics(second, "DistilBERT")
    print("\nВідмінностей:", differences, "із", len(texts))
    print("Різні результати не завжди означають, що модель помилилася.")

    save_csv(first, "RoBERTa", category)
    save_csv(second, "DistilBERT", category)
    return first, second


def save_report(first, second):
    positive1, negative1, neutral1 = count_results(first)
    positive2, negative2, neutral2 = count_results(second)
    differences = 0

    with open("report.md", "w", encoding="utf-8") as file:
        file.write("# Звіт: Review Analyzer\n\n")
        file.write("## Мета\nАналіз тональності відгуків готовими моделями Hugging Face.\n\n")
        file.write("## Моделі\n")
        file.write("- RoBERTa: " + model_names["RoBERTa"] + "\n")
        file.write("- DistilBERT: " + model_names["DistilBERT"] + "\n\n")
        file.write("## Статистика\n")
        file.write("- RoBERTa: " + str(positive1) + " Positive, " + str(negative1)
                   + " Negative, " + str(neutral1) + " Neutral.\n")
        file.write("- DistilBERT: " + str(positive2) + " Positive, " + str(negative2)
                   + " Negative. Neutral не підтримується.\n\n")
        file.write("## Порівняння всіх відгуків\n")

        for i in range(len(first)):
            file.write("\n" + str(i + 1) + ". " + first[i]["text"] + "\n")
            file.write("- RoBERTa: " + first[i]["label"] + " ("
                       + str(first[i]["confidence"]) + "%)\n")
            file.write("- DistilBERT: " + second[i]["label"] + " ("
                       + str(second[i]["confidence"]) + "%)\n")
            if first[i]["label"] != second[i]["label"]:
                differences += 1

        file.write("\n## Висновок\n")
        file.write("Моделі дали різні оцінки у " + str(differences)
                   + " із " + str(len(first)) + " випадків. ")
        file.write("Це не завжди помилка: деякі відгуки містять змішані оцінки. ")
        file.write("RoBERTa підтримує Neutral, а DistilBERT — ні. ")
        file.write("Оцінка впевненості не гарантує правильності відповіді. ")
        file.write("Сарказм та суперечливі тексти можуть спричиняти помилки.\n")

    print("Звіт збережено у report.md")


def save_special_report(first, second):
    with open("edge_cases.md", "w", encoding="utf-8") as file:
        file.write("# Дослідження складних відгуків\n\n")

        for i in range(len(special_reviews)):
            file.write("## " + special_types[i] + "\n")
            file.write(special_reviews[i] + "\n\n")
            file.write("- RoBERTa: " + first[i]["label"] + " ("
                       + str(first[i]["confidence"]) + "%)\n")
            file.write("- DistilBERT: " + second[i]["label"] + " ("
                       + str(second[i]["confidence"]) + "%)\n\n")

        file.write("## Пояснення\n")
        file.write("- Короткий відгук має мало контексту.\n")
        file.write("- Довгий відгук містить і переваги, і недоліки.\n")
        file.write("- Сарказм може мати позитивні слова, але негативний зміст.\n")
        file.write("- Суперечливий відгук поєднує позитивні й негативні оцінки.\n")
        file.write("Результати моделей потрібно перевіряти за змістом тексту.\n")

    print("Звіт збережено у edge_cases.md")


print("Review Analyzer — аналіз тональності за допомогою Hugging Face")

while True:
    print("\n========== REVIEW ANALYZER ==========")
    print("1. Проаналізувати один свій відгук")
    print("2. Проаналізувати всі 40 відгуків")
    print("3. Порівняти дві моделі на 40 відгуках")
    print("4. Перевірити складні відгуки")
    print("5. Ввести декілька власних відгуків")
    print("0. Вийти")

    try:
        choice = input("Оберіть пункт: ").strip()

        if choice == "0":
            print("Роботу завершено.")
            break

        elif choice == "1":
            text = input("Введіть відгук англійською: ").strip()
            if text == "":
                print("Помилка: відгук порожній.")
            else:
                results = analyze([text], "RoBERTa")
                show_results(results, "RoBERTa")
                show_statistics(results, "RoBERTa")
                save_csv(results, "RoBERTa", "manual")

        elif choice == "2":
            results = analyze(reviews, "RoBERTa")
            show_results(results, "RoBERTa")
            show_statistics(results, "RoBERTa")
            save_csv(results, "RoBERTa", "all_40")

        elif choice == "3":
            first, second = compare_models(reviews, "comparison")
            save_report(first, second)

        elif choice == "4":
            first, second = compare_models(special_reviews, "special")
            save_special_report(first, second)

        elif choice == "5":
            texts = []
            print("Введіть відгуки по одному. Порожній рядок завершує введення.")
            while True:
                text = input("Відгук " + str(len(texts) + 1) + ": ").strip()
                if text == "":
                    break
                texts.append(text)

            if len(texts) == 0:
                print("Помилка: не введено жодного відгуку.")
            else:
                results = analyze(texts, "RoBERTa")
                show_results(results, "RoBERTa")
                show_statistics(results, "RoBERTa")
                save_csv(results, "RoBERTa", "manual")

        else:
            print("Невідомий пункт меню. Введіть число від 0 до 5.")

    except (KeyboardInterrupt, EOFError):
        print("\nПрограму зупинено.")
        break
    except Exception as error:
        print("Сталася помилка:", error)
        print("Перевірте інтернет, встановлення бібліотек та доступ до файлів.")
