import uvicorn
from routers import university, new, test, major, user  # 导入user外部文件
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    responses={404: {"description": "Not found app"}},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins= "*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(university.router)
app.include_router(new.router)
app.include_router(test.router)
app.include_router(major.router)
app.include_router(user.router)

@app.get('/api')
async def hello():
    return {
        "data": 123
    }


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="0.0.0.0", port=8011, reload=True, debug=True)
