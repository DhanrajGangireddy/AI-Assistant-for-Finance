from fastapi import APIRouter, HTTPException
from service.qa_chain import rag_chain,suggestion_chain
from models.schemas import QuestionInput, AnswerOutput,ChatHistory
import asyncio

router = APIRouter()

@router.post("/ask", response_model=ChatHistory)
async def ask_question(text: QuestionInput):
    try:
        response, suggestions = await asyncio.gather(
            rag_chain.ainvoke(text.question),
            suggestion_chain.ainvoke(text.question)
        )
        
        suggested_questions = [q.strip() for q in suggestions.split("\n") 
                              if q.strip() and not q.strip().isdigit()][1:4]
    
        return ChatHistory(status='success',status_code='S-10018',
                           data=AnswerOutput(answer=response,suggestion=suggested_questions)
        )    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    