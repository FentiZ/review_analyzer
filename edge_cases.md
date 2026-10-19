# Додаткове дослідження складних відгуків

Короткі, довгі, саркастичні та суперечливі відгуки проаналізовано двома моделями.

## Короткий
**Текст:** Great!

- RoBERTa: Positive (93.82%)
- DistilBERT: Positive (99.99%)

## Довгий
**Текст:** I purchased this laptop a month ago and have been using it every day. The display is sharp, the keyboard feels comfortable, and most tasks run smoothly. However, the fan is loud, the battery runs out much sooner than advertised, and the customer service team has not answered my emails. Overall, I have both positive and negative impressions.

- RoBERTa: Positive (64.64%)
- DistilBERT: Negative (85.26%)

## Саркастичний
**Текст:** Fantastic! The app deleted all my files again. Exactly what I needed.

- RoBERTa: Positive (97.41%)
- DistilBERT: Negative (93.66%)

## Суперечливий
**Текст:** I love the design, but the product is unreliable and breaks constantly.

- RoBERTa: Negative (89.68%)
- DistilBERT: Negative (99.61%)

## Інтерпретація
- Короткий відгук: моделі мають дуже мало контексту.
- Довгий відгук: містить як позитивні, так і негативні характеристики.
- Саркастичний відгук: позитивна лексика може означати негативне ставлення.
- Суперечливий відгук: одночасно описує переваги та недоліки.

Остаточно оцінити правильність прогнозу можна лише шляхом порівняння з очікуваною тональністю, визначеною людиною.
