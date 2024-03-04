from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
from dotenv import load_dotenv
import os
import streamlit as st
from chains import Chain

load_dotenv()
os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
os.environ['environment'] = "gcp-starter"

index_name = "wine-db"
embedding = OpenAIEmbeddings()
chain_obj = Chain()


def query_db(query, vectordb):
    docs = vectordb.similarity_search(query)
    print(docs[0].page_content)
    return docs


def main():
    # Todo: Grab the data from db
    vectordb = Pinecone.from_existing_index(
        index_name=index_name,
        embedding=embedding
    )

    # Todo: Ask questions needed to query the db and store them
    # 1. Get the chain from LLM
    query_chain, query_response_format, query_output_parser = chain_obj.build_query_chain()

    # 2. Inorder to run query chain - i need user input about taste, experience, wine_color, flavor, pairing, complement and the response format
    st.sidebar.subheader("1. Preferred Taste Profile")
    taste = st.sidebar.selectbox(
        "", ["Select an option", "Very sweet", "Sweet", "Neutral", "Dry", "Very dry"]
    )

    st.sidebar.subheader("2. Wine Experience")
    experience = st.sidebar.selectbox(
        "",
        [
            "Select an option",
            "Novice (just starting)",
            "Casual drinker (have tried a few)",
            "Enthusiast (drink regularly)",
            "Connoisseur (very knowledgeable)",
        ],
    )

    st.sidebar.subheader("3. Red vs. White")
    wine_color = st.sidebar.selectbox(
        "",
        [
            "Select an option",
            "Prefer red",
            "Prefer white",
            "Like both equally",
            "No preference",
        ],
    )

    st.sidebar.subheader("4. Favorite Flavors")
    flavors = [
        "Fruity",
        "Earthy",
        "Floral",
        "Spicy",
        "Oaky/Woody",
        "Citrusy",
        "Buttery",
        "Herbal",
    ]
    flavor = st.sidebar.multiselect("", flavors)

    st.sidebar.subheader("5. Pairing Intent")
    pairing = st.sidebar.selectbox(
        "",
        [
            "Select an option",
            "Casual drinking",
            "Romantic dinner",
            "Seafood meal",
            "Red meat dish",
            "Poultry dish",
            "Vegetarian meal",
            "Dessert",
            "No specific pairing",
        ],
    )

    st.sidebar.subheader(
        "6. Any complement of the answers above with other foods or tastes you like the most."
    )
    complement = st.sidebar.text_input("Complement the answers above")

    # 3. Run the Chain
    if st.sidebar.button('Generate Recommendation'):

        # print(taste,experience,wine_color,flavor,pairing,complement)
        response = query_chain.run(
            {
                "taste": taste,
                "experience": experience,
                "wine_color": wine_color,
                "flavor": flavor,
                "pairing": pairing,
                "complement": complement,
                "response_format_instruction": query_response_format,
            }
        )

        print('response: ')
        print(response)

        query = query_output_parser.parse(response)['query_string']
        print('query')
        print(query)

        # Todo: Once the input query is ready - Query the DB
        docs = query_db(query=query, vectordb=vectordb)
        print('docs:')
        print(docs)
        print(len(docs))

        # Extract the metadata - collect the wine options
        wine_options = [
            {
                "name": doc.metadata["name"],
                "country": doc.metadata["country"],
                "province": doc.metadata["province"],
                "variety": doc.metadata["variety"],
                "winery": doc.metadata["winery"],
            }
            for doc in docs
        ]

        print(wine_options)
        print(len(wine_options))

        wine_1 = wine_options[0]
        wine_2 = wine_options[1]
        wine_3 = wine_options[2]
        wine_4 = wine_options[3]

        # Todo: Recommend Wine to user
        recommened_chain, recommended_response_format, recommended_output_parser = chain_obj.build_recommendation_chain()
        recommended_response = recommened_chain.run(
            {
                "taste": taste,
                "experience": experience,
                "wine_color": wine_color,
                "flavor": flavor,
                "pairing": pairing,
                "complement": complement,
                "wine_1": wine_1,
                "wine_2": wine_2,
                "wine_3": wine_3,
                "wine_4": wine_4,
                "response_format_instructions": recommended_response_format,
            }
        )

        recommendation = recommended_output_parser.parse(recommended_response)['recommendation']
        explanation = recommended_output_parser.parse(recommended_response)['explanation']

        print(" ----- #### ---- ### --- ")
        print('recommendation: ')
        print(recommendation)
        print('explanation: ')
        print(explanation)

        # It can be written using next keyword
        # matching_wine = next(
        #     (wine for wine in wine_options if wine["name"] == recommendation), None
        # )
        matching_wine = None
        for wine in wine_options:
            if wine['name'] == recommendation:
                matching_wine = wine

        print(matching_wine)

        st.write("---")
        if matching_wine:
            st.write(
                f"""
                    ### 🍷 **Recommended Wine**
                        {recommendation}

                    ---
                    **Country**: {matching_wine['country']}

                    **Province**: {matching_wine['province']}

                    **Variety**: {matching_wine['variety']}

                    **Winery**: {matching_wine['winery']}

                    **Explanation**: 
                    {explanation}
                """
            )
        else:
            st.write(
                f"""
                    ### 🍷 **Recommended Wine**
                        {recommendation}

                    **Explanation**: 
                        {explanation}
                """
            )


# Main Function
if __name__ == '__main__':
    main()


