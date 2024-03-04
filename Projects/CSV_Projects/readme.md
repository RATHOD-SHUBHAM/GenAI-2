# CSV_Projects:
Query a CSV file using LLM, by creating vector embeddings.

# Wine Suggestion

The problem we want to tackle is personalized wine recommendations.

## Workflow
So, to tackle our problem
* We want first to understand the taste of the user,
* Then search the database for the wines that may be a good recommendation, and
* Decide which one is the final recommendation.

To get user input we will use a simple questionnaire inside Streamlit with the following questions:
  - Preferred Taste Profile;
  - Level of experience;
  - Red or White wine preference;
  - Favorite Flavours;
  - Pairing intent;
  - Open field to add any information about your taste.

## Architecture
For the solution, we will have two calls to the LLM API. 

1. In the first call, we will give the LLM the user's taste preferences and instruct it to create a string query that will be used to search the vector database for similarities.

We can identify the wine descriptions that most closely match the individual's preferences using the results of the similarity search.

This alone, however, is insufficient for making the final decision because this basic similarity search ignores certain qualities, such as red versus white wine. 

2. For this reason, we provide the LLM with the user's original taste preferences together with the top three wines that came up in the similarity search, and we ask it to choose the best wine for it and explain why.

## Project Structure
1. VectorDB: Create embeddings from the CSV file and store it in DB.
2. Chain: To query LLMs.
3. App: The main app that links Chain and DB together.

## Main App
This code can be divided into three main parts:

1. The form to get the user input;
2. The interaction of the chains and the vector database;
3. Then display of the final recommendation.

---

<img width="2256" alt="ss" src="https://github.com/RATHOD-SHUBHAM/GenAI-2/assets/58945964/1c86cf58-199c-48fe-9daa-2e063dd546a4">

---

# Food Advisors

LLM-powered application to tackle an everyday issue: what should I eat today?

The user may express his preferences using human-readable language on the app, and it will return the recipes that most closely match his tastes.


## Workflow
So, to tackle our problem
* We want first to understand the taste of the user,
* Then search the database for the food that may be a good recommendation.

To get user input we will use a simple questionnaire inside Streamlit with the following questions:
  - Kind of meal;
  - Maximum Prep Time;
  - Ingredients to include;
  - Favorite Flavours;
  - Open field to add any information about your taste.


## Steps:
The first step is to store our data in a vector database. Once the database is available, we can query it by performing similarity searches. <br>
This will be done by the LLM, the core of the application, which will be responsible for understanding the user preferences and retrieving an appropriate query.

Summing up,
1. Preprocess data.
2. Store data in a vector database.
3. Build the LLM pipeline.
4. Build a Streamlit application for controlling the job flow.

## Architecture
For the solution, we will have one call to the LLM API. 

1. In this call, we will give the LLM the user's taste preferences and instruct it to create a string query that will be used to search the vector database for similarities.

We can identify the recipe descriptions that most closely match the individual's preferences using the results of the similarity search.


## Project Structure
1. VectorDB: Create embeddings from the CSV file and store it in DB.
2. Chain: To query LLMs.
3. App: The main app that links Chain and DB together.

## Main App
This code can be divided into three main parts:

1. The form to get the user input;
2. The interaction of the chain and the vector database;
3. Then display all recommendations.

---

![ss](https://github.com/RATHOD-SHUBHAM/GenAI-2/assets/58945964/09ba15de-90f8-4e48-bcb1-d14911bbeeb7)

---