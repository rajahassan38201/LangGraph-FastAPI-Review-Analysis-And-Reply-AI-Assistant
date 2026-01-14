import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import TypedDict, Literal, Optional
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

# --- 1. LangGraph Logic (from your notebook) ---

# Initialize the OpenAI model
model = ChatOpenAI(model='gpt-4o-mini')

# Pydantic Schemas for structured output
class SentimentSchema(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description='Sentiment of the review')

class DiagnosisSchema(BaseModel):
    issue_type: Literal["UX", "Performance", "Bug", "Support", "Other"] = Field(description='The category of issue mentioned in the review')
    tone: Literal["angry", "frustrated", "disappointed", "calm"] = Field(description='The emotional tone expressed by the user')
    urgency: Literal["low", "medium", "high"] = Field(description='How urgent or critical the issue appears to be')

# Create structured models
structured_model = model.with_structured_output(SentimentSchema)
structured_model2 = model.with_structured_output(DiagnosisSchema)

# Define the State
class ReviewState(TypedDict):
    review: str
    sentiment: Literal["positive", "negative"]
    diagnosis: dict  # This will hold the dict from DiagnosisSchema.model_dump()
    response: str

# Node Functions
def find_sentiment(state: ReviewState):
    """Finds the sentiment of the review."""
    prompt = f'For the following review find out the sentiment \n {state["review"]}'
    sentiment = structured_model.invoke(prompt).sentiment
    return {'sentiment': sentiment}

def check_sentiment(state: ReviewState) -> Literal["positive_response", "run_diagnosis"]:
    """Checks the sentiment to decide the next step."""
    if state['sentiment'] == 'positive':
        return 'positive_response'
    else:
        return 'run_diagnosis'
    
def positive_response(state: ReviewState):
    """Generates a response for a positive review."""
    prompt = f"""Write a warm thank-you message in response to this review:
    \n\n\"{state['review']}\"\n\n
Also, kindly ask the user to leave feedback on our website."""
    response = model.invoke(prompt).content
    return {'response': response}

def run_diagnosis(state: ReviewState):
    """Diagnoses a negative review."""
    prompt = f"""Diagnose this negative review:\n\n{state['review']}\n
Return issue_type, tone, and urgency."""
    response_obj = structured_model2.invoke(prompt)
    return {'diagnosis': response_obj.model_dump()}

def negative_response(state: ReviewState):
    """Generates a response for a negative review based on diagnosis."""
    diagnosis = state['diagnosis']
    prompt = f"""You are a support assistant.
The user had a '{diagnosis['issue_type']}' issue, sounded '{diagnosis['tone']}', and marked urgency as '{diagnosis['urgency']}'.
Write an empathetic, helpful resolution message.
"""
    response = model.invoke(prompt).content
    return {'response': response}

# Define and compile the graph
graph = StateGraph(ReviewState)

graph.add_node('find_sentiment', find_sentiment)
graph.add_node('positive_response', positive_response)
graph.add_node('run_diagnosis', run_diagnosis)
graph.add_node('negative_response', negative_response)

graph.add_edge(START, 'find_sentiment')
graph.add_conditional_edges('find_sentiment', check_sentiment)
graph.add_edge('positive_response', END)
graph.add_edge('run_diagnosis', 'negative_response')
graph.add_edge('negative_response', END)

workflow = graph.compile()

# --- 2. FastAPI Application ---

app = FastAPI(
    title="Review Reply AI Server",
    description="API for processing customer reviews with LangGraph"
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic models for API input and output
class ReviewInput(BaseModel):
    review: str

class DiagnosisOutput(BaseModel):
    """Matches the DiagnosisSchema for API output."""
    issue_type: Literal["UX", "Performance", "Bug", "Support", "Other"]
    tone: Literal["angry", "frustrated", "disappointed", "calm"]
    urgency: Literal["low", "medium", "high"]

class ReviewOutput(BaseModel):
    """The final state returned to the frontend."""
    review: str
    sentiment: Literal["positive", "negative"]
    diagnosis: Optional[DiagnosisOutput] = None
    response: str

@app.post("/process-review", response_model=ReviewOutput)
async def process_review(data: ReviewInput):
    """
    Receives a customer review, processes it through the LangGraph workflow,
    and returns the complete analysis and response.
    """
    initial_state = {"review": data.review}
    
    # Run the LangGraph workflow
    final_state = workflow.invoke(initial_state)
    
    # The final_state is a dict that matches the ReviewOutput model
    return final_state

if __name__ == "__main__":
    print("Starting FastAPI server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)

