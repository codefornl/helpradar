# Wat staat hier
In deze map staan vooralsnog jupyter notebooks die de gescrapte hulpvraag en aanbod analyzeren.

# Hoe te gebruiken.
- installeer de packages in requirement.txt
- start je notebook op, bijvoorbeeld met jupyter lab

# eerste notebook: initiatives-nltk.ipynb
- Eerst importeren we de nodige packages
- Daarna maken we een setting op pandas om lange teksten te importen.
- Daarna wordt er een verbinding gemaakt met corana-data.db, te downloaden op https://github.com/codefornl/corona-data/blob/master/corona-data.db en wordt de data in een pandas dataframe geladen
- Op dit dataframe vinden een aantal NLP preprocessing stappen plaats
    - type setting van 'description' en 'group' column
    - toevoegen van labeld op 'group' column
    - cleaning van 'description' colukn door cleanen, stemming en tokenizing
- Daarna drie voorbeelden:
    - Classificatie op de labels aanbod en vraag door middel van TF-IDF vectors
    - Topic classificatie door middel van LDA. 
    - gewogen TFIDF term analyze. Welke term komt het vaakst voor (ongewogen en gewogen). 

# tweede notebook: initiatives-spacy.ipynb
- Lijkt op het eerste, maar dit is een variant met de spacy library voor NLP.

# todo:
- classifier verbeteren
- doc2vec voorbeeld
- Toewerken naar NLP proces waarbij de initiatieven door worden ingedeeld naar de groepen van LOT-C