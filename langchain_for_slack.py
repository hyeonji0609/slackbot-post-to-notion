from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
import dotenv 
import re
import logging

class ChatGPT:
    def __init__(self):
        dotenv.load_dotenv()
        self.template = '''Please summarize the following briefly: {text}'''
        self.combine_template = '''{text}

        Please write the results of the summary in the following format in korean:
        title : The title of the content in korean
        context : 
            1. Summarize shortly the main points in bullet points in korean.
            2. Each summarized sentence must start with an emoji that fits the meaning of the each sentence.
            3. Use various emojis to make the summary more interesting.
        '''
    def extract_url(self, text):
        url_pattern = re.compile(
            r'<(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)>'
        )
        # 정규 표현식을 사용하여 URL 추출
        urls = url_pattern.findall(text)
        clean_urls = [url.strip('<>') for url in urls]

        return clean_urls

    def langchain(self, text, model='gpt-3.5-turbo-16k'):
        url, *rest = self.extract_url(text)
        
        loader = WebBaseLoader(url)
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3000,     # 쪼개는 글자수
            chunk_overlap=10,   # 오버랩 글자수
        )

        docs = WebBaseLoader(url).load_and_split(text_splitter)

        prompt = PromptTemplate(template=self.template, input_variables=['text'])
        combine_prompt = PromptTemplate(template=self.combine_template, input_variables=['text'])

        llm = ChatOpenAI(temperature=0, 
                        model_name=model)

        chain = load_summarize_chain(llm, 
                                    map_prompt=prompt, 
                                    combine_prompt=combine_prompt, 
                                    chain_type="map_reduce", 
                                    verbose=False)
        
        summary  = chain.run(docs)

        return summary, url