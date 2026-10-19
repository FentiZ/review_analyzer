# Звіт до практичної роботи: Review Analyzer

## Мета роботи
Використання попередньо навчених моделей Hugging Face для визначення тональності англомовних відгуків без самостійного навчання нейромережі.

## Використані моделі
1. RoBERTa — `cardiffnlp/twitter-roberta-base-sentiment-latest`. Класи: Positive, Neutral, Negative.
2. DistilBERT — `distilbert/distilbert-base-uncased-finetuned-sst-2-english`. Класи: Positive, Negative.

## Статистика
| Модель | Усього | Positive | Negative | Neutral |
|---|---:|---:|---:|---:|
| RoBERTa | 40 | 22 | 17 | 1 |
| DistilBERT | 40 | 18 | 22 | Не підтримує |

Кількість відмінностей у класифікації: **5 із 40**.

## Результати для всіх відгуків
| № | Відгук | RoBERTa | DistilBERT |
|---:|---|---|---|
| 1 | The application works perfectly. I use it every day. | Positive (97.73%) | Positive (99.98%) |
| 2 | The delivery was late, and the package was damaged. | Negative (89.94%) | Negative (99.97%) |
| 3 | The product is acceptable, but nothing special. | Negative (49.02%) | Negative (98.69%) |
| 4 | Excellent customer support and fast service! | Positive (97.18%) | Positive (99.99%) |
| 5 | The software crashes every time I open it. | Negative (87.90%) | Negative (99.97%) |
| 6 | The headphones have clear sound and comfortable ear cushions. | Positive (85.45%) | Positive (99.88%) |
| 7 | I am disappointed with the quality of this product. | Negative (93.56%) | Negative (99.98%) |
| 8 | The website is easy to navigate and looks modern. | Positive (92.47%) | Positive (99.92%) |
| 9 | The food arrived cold and tasted terrible. | Negative (94.66%) | Negative (99.96%) |
| 10 | The staff were friendly and helped me solve the problem. | Positive (80.57%) | Positive (99.98%) |
| 11 | The battery lasts much longer than I expected. | Positive (60.68%) | Negative (99.34%) |
| 12 | This is the worst purchase I have made this year. | Negative (95.24%) | Negative (99.98%) |
| 13 | The service was fine, but the price was a little high. | Positive (53.08%) | Positive (97.13%) |
| 14 | Setup was simple, and everything worked on the first try. | Positive (92.72%) | Negative (88.00%) |
| 15 | The instructions are confusing and difficult to follow. | Negative (88.26%) | Negative (99.96%) |
| 16 | I love the design, and the product feels very durable. | Positive (98.38%) | Positive (99.99%) |
| 17 | The order arrived two days earlier than expected. | Neutral (73.31%) | Negative (97.63%) |
| 18 | The camera quality is poor in low light. | Negative (81.45%) | Negative (99.98%) |
| 19 | Nothing was wrong with the item, but it did not impress me. | Negative (76.96%) | Negative (99.94%) |
| 20 | Customer support ignored my messages for several days. | Negative (86.63%) | Negative (99.95%) |
| 21 | The new update fixed the bugs and improved performance. | Positive (83.42%) | Positive (99.92%) |
| 22 | The chair is uncomfortable after sitting for an hour. | Negative (80.70%) | Negative (99.86%) |
| 23 | The subscription is affordable and offers great value. | Positive (96.07%) | Positive (99.98%) |
| 24 | The app is slow and drains my phone battery. | Negative (92.53%) | Negative (99.92%) |
| 25 | The hotel room was clean, quiet, and comfortable. | Positive (89.48%) | Positive (99.98%) |
| 26 | The product stopped working after only one week. | Negative (86.12%) | Negative (99.96%) |
| 27 | The packaging was neat, and the item matched the description. | Positive (96.74%) | Positive (99.96%) |
| 28 | The meal was okay, although the portions were small. | Positive (89.62%) | Positive (99.94%) |
| 29 | I received the wrong item and had to return it. | Negative (84.38%) | Negative (99.96%) |
| 30 | The course was informative, engaging, and well organized. | Positive (97.62%) | Positive (99.99%) |
| 31 | The printer works as expected, with no major issues. | Positive (70.03%) | Negative (93.78%) |
| 32 | I would not recommend this service to anyone. | Negative (91.25%) | Negative (93.83%) |
| 33 | The screen is bright, sharp, and easy to read. | Positive (94.64%) | Positive (99.98%) |
| 34 | The repair took longer than promised, but the result is good. | Positive (85.92%) | Positive (99.97%) |
| 35 | The price is reasonable for the features provided. | Positive (68.69%) | Positive (99.78%) |
| 36 | The instructions were clear, and installation took ten minutes. | Positive (73.05%) | Negative (99.32%) |
| 37 | The sound quality is average, and the controls feel cheap. | Negative (92.26%) | Negative (99.98%) |
| 38 | I had a wonderful experience from start to finish. | Positive (98.75%) | Positive (99.99%) |
| 39 | The product looks nice, but it does not work properly. | Negative (89.62%) | Negative (99.97%) |
| 40 | The support team resolved my issue quickly and professionally. | Positive (65.61%) | Positive (99.02%) |

## Неоднозначні випадки та можливі помилки
Відгуки № 3, 13, 19, 28, 34, 37 і 39 містять змішані або помірні оцінки. У таких випадках моделі можуть визначати різні класи; це треба звіряти з контекстом, а не автоматично називати помилкою.

Сарказм також може призводити до хибної класифікації: формально позитивні слова можуть описувати негативний досвід. Довгі та суперечливі відгуки часто містять аргументи різної полярності. Режим 4 програми дозволяє перевірити ці випадки окремо.

Важливо: оцінка впевненості є оцінкою моделі для обраного класу, а не гарантією правильності. DistilBERT не має нейтрального класу, тому змушена відносити нейтральні відгуки до Positive або Negative.

## Висновок
Програма автоматично класифікує відгуки, рахує статистику, порівнює дві попередньо навчені моделі й зберігає результати у CSV. Для аналізу нейтральних текстів RoBERTa є зручнішою через підтримку трьох класів. Розбіжності між моделями потребують людської перевірки.
