from app.services.embedding import embedding_service_text
from app.services.vectorstore import search_vectorstore
from app.services.llm import get_openai_llm
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def qa_chain(history, new_message, top_k=5):
    """
    Question-answering chain that retrieves relevant documents and generates responses.
    
    Args:
        history: List of conversation history messages
        new_message: The new user message to process
        top_k: Number of top documents to retrieve
        
    Returns:
        Async generator yielding response chunks
    """
    try:
        # Build enhanced query by combining history context with new message
        enhanced_query = new_message
        
        # Add recent history context to the query if available
        if history and len(history) > 0:
            # Get the last few messages for context
            recent_messages = history[-3:]  # Last 3 messages
            context_parts = []
            for msg in recent_messages:
                if hasattr(msg, 'content'):
                    context_parts.append(msg.content)
            
            if context_parts:
                # Combine recent context with new message
                enhanced_query = f"Context: {' '.join(context_parts)}. Question: {new_message}"
        
        # Get query vector for similarity search using enhanced query
        query_vector = embedding_service_text(enhanced_query)
        if query_vector is None:
            # If embedding fails, return "content irrelevant"
            def no_content_generator():
                yield "内容不相关"
            return no_content_generator()
        
        # Retrieve relevant documents from vector store with lower threshold for better recall
        docs = search_vectorstore(query_vector, top_k, similarity_threshold=0.3)
        
        # Check if relevant documents were found
        if not docs or len(docs) == 0:
            def no_content_generator():
                yield "内容不相关"
            return no_content_generator()
        
        # Build context from retrieved documents
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Convert history to string format for prompt
        history_text = ""
        for msg in history:
            if hasattr(msg, 'content'):
                history_text += f"{msg.__class__.__name__}: {msg.content}\n"
        
        # Use custom prompt template with history
        prompt_template = PromptTemplate(
            input_variables=["context", "history", "question"],
            template="""
            You are a helpful assistant for question-answering tasks. 
            Use the following pieces of retrieved context to provide a comprehensive and detailed answer to the question.
            If you don't know the answer based on the provided context, just say that you don't know.
            Provide thorough explanations and include relevant details from the context.
            You can also use the conversation history to provide more contextual answers.
            
            History: {history}
            Question: {question} 
            Context: {context} 
            Answer:"""
        )
        
        # Get LLM instance
        llm = get_openai_llm()
        
        # Build chain
        chain = prompt_template | llm | StrOutputParser()
        
        # Return streaming output
        return chain.astream({
            "context": context,
            "history": history_text,
            "question": new_message
        })
        
    except Exception as e:
        print(f"Error in qa_chain: {e}")
        # Return "content irrelevant" on any error
        def no_content_generator():
            yield "内容不相关"
        return no_content_generator()
    




    