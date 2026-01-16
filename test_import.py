print("Starting import test...")
try:
    print("1. Importing FastAPI...")
    from fastapi import FastAPI
    print("   SUCCESS")
    
    print("2. Creating app...")
    app = FastAPI()
    print("   SUCCESS")
    
    print("3. Importing a2wsgi...")
    from a2wsgi import ASGIMiddleware
    print("   SUCCESS")
    
    print("4. Creating ASGIMiddleware...")
    application = ASGIMiddleware(app)
    print("   SUCCESS")
    
    print("5. Importing Storage...")
    from db.storage import Storage
    print("   SUCCESS")
    
    print("6. Creating Storage instance...")
    storage = Storage()
    print("   SUCCESS")
    
    print("\nAll imports successful!")
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
