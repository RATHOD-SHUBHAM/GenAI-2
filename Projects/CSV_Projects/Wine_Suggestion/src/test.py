from chains import Chain

class Test:
    # Function to test Chain >> build Query function
    def query_chain_test(self, query_chain, response_format_instruction):
        response = query_chain.run(
            {
                "taste": 'dry',
                "experience": 'casual drinker',
                "wine_color": 'prefer red',
                "flavor": 'spicy',
                "pairing": 'meat',
                "complement": 'bitter flavor',
                "response_format_instruction": response_format_instruction
            }
        )

        return response


    def test_query_chain(self):
        chain_obj = Chain()
        query_chain, query_response_format, query_output_parser = chain_obj.build_query_chain()
        print("Query Chain is: ")
        print(query_chain)
        print('\n')
        print("Response Format is: ")
        print(query_response_format)
        print('\n')
        print("Output Format is: ")
        print(query_output_parser)

        query_chain_test_response = self.query_chain_test(query_chain=query_chain, response_format_instruction=query_response_format)
        print('\n')
        print("##############")
        print("Test Response is: ")
        print(query_chain_test_response)



if __name__ == '__main__':
    test_chain_obj = Test()
    test_chain_obj.test_query_chain()