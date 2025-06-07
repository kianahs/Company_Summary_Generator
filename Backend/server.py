import sys
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from run import main

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RequestData(BaseModel):
    company: str
    url: str
    free_plan: bool = True


@app.on_event("startup")
async def startup_event():
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@app.post("/run")
async def run_summary(data: RequestData):
    try:
        summary = await main(company=data.company, url=data.url, free_plan=data.free_plan)
        # return {"message": f"Summary generation for {len(summary)} complete!", }
        return {
            "message": f"Summary generation for {data.company} complete!",
            "model": "llama3-70b-8192" if data.free_plan else "gpt-4.1-mini",
            "summary": summary
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# import sys
# import asyncio

# from fastapi import FastAPI, Request
# from pydantic import BaseModel

# from run import main

# app = FastAPI()


# class RequestData(BaseModel):
#     company: str
#     url: str
#     free_plan: bool = True


# @app.post("/run")
# async def run_summary(data: RequestData):
#     await main(company=data.company,
#                url=data.url, free_plan=data.free_plan)
#     return {
#         "message": f"Summary generation for {data.company} complete!",
#         "model": "llama3-70b-8192" if data.free_plan else "gpt-4.1-mini"
#     }


# # uvicorn server:app --reload
