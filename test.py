from langchain_google_genai import GoogleGenerativeAIEmbeddings

emb = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
vec = emb.embed_query("test")
print(len(vec))