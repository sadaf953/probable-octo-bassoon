from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain


template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

#Improved error handling for Ollama
def create_ollama_llm(model_name="llama3.1"):
  """Creates an Ollama LLM instance with error handling"""
  try:
    llm = OllamaLLM(model=model_name)
    return llm
  except Exception as e:
    raise ValueError(f"Error creating Ollama LLM: {e}")

#Improved Function to Parse data

def parse_with_ollama(dom_chunks, parse_description):
    """Parses data using Ollama LLM with improved error handling."""
    llm = create_ollama_llm() #Initialize LLM with error handling
    prompt = ChatPromptTemplate.from_template(template)
    chain = LLMChain(llm=llm, prompt=prompt)  #Use LLMChain for better structure

    parsed_results = []
    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            response = chain.run({"dom_content": chunk, "parse_description": parse_description})
            print(f"Parsed batch: {i} of {len(dom_chunks)}")
            parsed_results.append(response)
        except Exception as e:
            print(f"Error parsing chunk {i}: {e}")
            parsed_results.append("") #Append empty string on error

    return "\n".join(parsed_results).strip() #Strip any extra whitespace

