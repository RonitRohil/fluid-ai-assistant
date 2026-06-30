import json

from app.config import DATA_DIR


class EmployeeService:
    def search(self, query: str) -> dict:
        employees = self._load()
        q = query.lower()
        matches = [
            e
            for e in employees
            if q in e["name"].lower()
            or q in e["id"].lower()
            or q in e["department"].lower()
            or q in e["role"].lower()
        ]
        if not matches:
            return {"error": f"No employee found matching '{query}'"}
        return {"employees": matches}

    def _load(self) -> list:
        with open(DATA_DIR / "employees.json") as f:
            return json.load(f)


employee_service = EmployeeService()
