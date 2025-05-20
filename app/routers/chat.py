from fastapi import APIRouter, HTTPException
from langchain_core.messages import BaseMessage
from app.services.rag_chain import rag_chain
from app.schemas.chat import ChatRequest
import traceback

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        print("User input:", request.msg)
        
        chain = rag_chain()
        response = chain.invoke({"input": request.msg})
        answer = response.get("answer")
        print("answer:", answer)

        if isinstance(answer, BaseMessage):
            answer = answer.content

        return {"response": str(answer)}

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        if "quota" in str(e).lower():
            raise HTTPException(
                status_code=429,
                detail="⚠️ Error: You have exceeded your OpenAI quota. Please check your API billing."
            )
        raise HTTPException(
            status_code=500,
            detail="⚠️ Error: Something went wrong. Please try again later."
        )
