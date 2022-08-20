if __name__ == "__main__":
    import uvicorn
    uvicorn.run("project.main:app", host="0.0.0.0", port=8000, reload=True)