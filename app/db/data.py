
# Dados para testes
employers_data = [
    {"name": "MetaTechA", "contact_email": "contact@company-a.com", "industry": "Tech"},
    {"name": "MoneySoftB", "contact_email": "contact@company-b.com", "industry": "Finance"},
]

jobs_data = [
    {"title": "Software Engineer", "description": "Develop web applications", "employer_id": 1},
    {"title": "Data Analyst", "description": "Analyze data and create reports", "employer_id": 1},
    {"title": "Technical Accountant", "description": "Manage financial records", "employer_id": 2},
    { "title": "Manager", "description": "Manage people who manage records", "employer_id": 2},
    # {"title": "Jr Developer", "description": "Develop small pieces of software", "employer_id": 1},
]

users_data = [
    {"username": "chrism", "email":"iamchris@email.com", "password": "a1234a", "role":"admin" },
    {"username": "jakebell", "email":"jakeb@email.com", "password": "sddfdg", "role":"user" },
    {"username": "kellynorton", "email":"thekell@email.com", "password": "nkf145", "role":"user" },
    {"username": "samweiss", "email":"samweiss@email.com", "password": "jkq256", "role":"admin" },
    {"username": "kimjung", "email":"kimjung@email.com", "password": "stim254", "role":"user" }
]

applications_data = [
    {"user_id": 2, "job_id": 1},
    {"user_id": 2, "job_id": 2},
    {"user_id": 1, "job_id": 2},
    {"user_id": 2, "job_id": 4},
]