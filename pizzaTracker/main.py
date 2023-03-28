from fastapi import FastAPI

app = FastAPI()

@app.post("/create")
async def create():
    print("it worked")
    return {"message": "Success!"}

if __name__ == "__main__":
    main()