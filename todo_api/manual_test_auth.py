#!/usr/bin/env python3
"""Manual test script for Phase IV authenticated API."""

import httpx

BASE_URL = "http://localhost:8000"


def test_phase_iv_api():
    """Test the authenticated API manually."""
    client = httpx.Client(base_url=BASE_URL, timeout=10.0)

    print("=" * 60)
    print("Phase IV - Authenticated Todo API Manual Tests")
    print("=" * 60)

    # Test 1: Health check
    print("\n[1] Health Check")
    resp = client.get("/health")
    print(f"    GET /health -> {resp.status_code}")
    print(f"    Response: {resp.json()}")
    assert resp.status_code == 200
    print("    [OK] PASSED")

    # Test 2: Unauthenticated access should fail
    print("\n[2] Unauthenticated Access (should fail)")
    resp = client.get("/tasks")
    print(f"    GET /tasks (no auth) -> {resp.status_code}")
    assert resp.status_code == 401
    print("    [OK] PASSED - Returns 401 as expected")

    # Test 3: Register User A
    print("\n[3] Register User A")
    user_a = {"email": "alice@example.com", "password": "alicepass123"}
    resp = client.post("/auth/register", json=user_a)
    print(f"    POST /auth/register -> {resp.status_code}")
    print(f"    Response: {resp.json()}")
    assert resp.status_code == 201
    assert "password" not in resp.json()
    assert "password_hash" not in resp.json()
    print("    [OK] PASSED - User registered, password not exposed")

    # Test 4: Duplicate registration should fail
    print("\n[4] Duplicate Registration (should fail)")
    resp = client.post("/auth/register", json=user_a)
    print(f"    POST /auth/register (duplicate) -> {resp.status_code}")
    assert resp.status_code == 409
    print("    [OK] PASSED - Returns 409 Conflict")

    # Test 5: Login User A (OAuth2 form)
    print("\n[5] Login User A (OAuth2 form)")
    resp = client.post("/auth/login", data={
        "username": user_a["email"],
        "password": user_a["password"]
    })
    print(f"    POST /auth/login -> {resp.status_code}")
    token_data = resp.json()
    print(f"    Response: token_type={token_data.get('token_type')}, access_token=<{len(token_data.get('access_token', ''))} chars>")
    assert resp.status_code == 200
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    token_a = token_data["access_token"]
    print("    [OK] PASSED - Got JWT token")

    # Test 6: Login User A (JSON body)
    print("\n[6] Login User A (JSON body)")
    resp = client.post("/auth/login/json", json=user_a)
    print(f"    POST /auth/login/json -> {resp.status_code}")
    assert resp.status_code == 200
    print("    [OK] PASSED - JSON login works")

    # Test 7: Get current user
    print("\n[7] Get Current User (/auth/me)")
    headers_a = {"Authorization": f"Bearer {token_a}"}
    resp = client.get("/auth/me", headers=headers_a)
    print(f"    GET /auth/me -> {resp.status_code}")
    print(f"    Response: {resp.json()}")
    assert resp.status_code == 200
    assert resp.json()["email"] == user_a["email"]
    print("    [OK] PASSED")

    # Test 8: Invalid token should fail
    print("\n[8] Invalid Token (should fail)")
    resp = client.get("/auth/me", headers={"Authorization": "Bearer invalid-token"})
    print(f"    GET /auth/me (bad token) -> {resp.status_code}")
    assert resp.status_code == 401
    print("    [OK] PASSED - Returns 401")

    # Test 9: Create tasks for User A
    print("\n[9] Create Tasks for User A")
    resp = client.post("/tasks", json={"title": "Alice Task 1"}, headers=headers_a)
    print(f"    POST /tasks -> {resp.status_code}")
    task1 = resp.json()
    print(f"    Response: {task1}")
    assert resp.status_code == 201
    assert task1["title"] == "Alice Task 1"

    resp = client.post("/tasks", json={"title": "Alice Task 2"}, headers=headers_a)
    assert resp.status_code == 201
    print("    [OK] PASSED - Created 2 tasks")

    # Test 10: List tasks for User A
    print("\n[10] List Tasks for User A")
    resp = client.get("/tasks", headers=headers_a)
    print(f"    GET /tasks -> {resp.status_code}")
    tasks = resp.json()
    print(f"    Response: {len(tasks)} tasks")
    assert resp.status_code == 200
    assert len(tasks) == 2
    print("    [OK] PASSED")

    # Test 11: Register User B
    print("\n[11] Register User B")
    user_b = {"email": "bob@example.com", "password": "bobpass123"}
    resp = client.post("/auth/register", json=user_b)
    assert resp.status_code == 201

    resp = client.post("/auth/login", data={
        "username": user_b["email"],
        "password": user_b["password"]
    })
    token_b = resp.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    print("    [OK] PASSED - User B registered and logged in")

    # Test 12: User B should NOT see User A's tasks
    print("\n[12] User Isolation - User B sees empty list")
    resp = client.get("/tasks", headers=headers_b)
    print(f"    GET /tasks (User B) -> {resp.status_code}")
    print(f"    Response: {resp.json()}")
    assert resp.status_code == 200
    assert resp.json() == []
    print("    [OK] PASSED - User B sees no tasks")

    # Test 13: User B cannot access User A's task
    print("\n[13] User Isolation - User B cannot GET User A's task")
    task_id = task1["id"]
    resp = client.get(f"/tasks/{task_id}", headers=headers_b)
    print(f"    GET /tasks/{task_id} (User B) -> {resp.status_code}")
    assert resp.status_code == 404
    print("    [OK] PASSED - Returns 404 (not 403 for security)")

    # Test 14: User B cannot update User A's task
    print("\n[14] User Isolation - User B cannot UPDATE User A's task")
    resp = client.put(f"/tasks/{task_id}", json={"title": "Hacked!"}, headers=headers_b)
    print(f"    PUT /tasks/{task_id} (User B) -> {resp.status_code}")
    assert resp.status_code == 404
    print("    [OK] PASSED")

    # Test 15: User B cannot delete User A's task
    print("\n[15] User Isolation - User B cannot DELETE User A's task")
    resp = client.delete(f"/tasks/{task_id}", headers=headers_b)
    print(f"    DELETE /tasks/{task_id} (User B) -> {resp.status_code}")
    assert resp.status_code == 404
    print("    [OK] PASSED")

    # Test 16: User B cannot toggle User A's task
    print("\n[16] User Isolation - User B cannot TOGGLE User A's task")
    resp = client.patch(f"/tasks/{task_id}/toggle", headers=headers_b)
    print(f"    PATCH /tasks/{task_id}/toggle (User B) -> {resp.status_code}")
    assert resp.status_code == 404
    print("    [OK] PASSED")

    # Test 17: User A can still access their task
    print("\n[17] User A Can Still Access Their Task")
    resp = client.get(f"/tasks/{task_id}", headers=headers_a)
    print(f"    GET /tasks/{task_id} (User A) -> {resp.status_code}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Alice Task 1"
    print("    [OK] PASSED")

    # Test 18: Toggle task
    print("\n[18] Toggle Task Completion")
    resp = client.patch(f"/tasks/{task_id}/toggle", headers=headers_a)
    print(f"    PATCH /tasks/{task_id}/toggle -> {resp.status_code}")
    print(f"    is_complete: {resp.json()['is_complete']}")
    assert resp.status_code == 200
    assert resp.json()["is_complete"] is True
    print("    [OK] PASSED")

    # Test 19: Update task
    print("\n[19] Update Task")
    resp = client.put(f"/tasks/{task_id}", json={"title": "Alice Task 1 (Updated)"}, headers=headers_a)
    print(f"    PUT /tasks/{task_id} -> {resp.status_code}")
    print(f"    New title: {resp.json()['title']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Alice Task 1 (Updated)"
    print("    [OK] PASSED")

    # Test 20: Delete task
    print("\n[20] Delete Task")
    resp = client.delete(f"/tasks/{task_id}", headers=headers_a)
    print(f"    DELETE /tasks/{task_id} -> {resp.status_code}")
    assert resp.status_code == 204

    resp = client.get(f"/tasks/{task_id}", headers=headers_a)
    assert resp.status_code == 404
    print("    [OK] PASSED - Task deleted")

    # Test 21: Wrong password login
    print("\n[21] Wrong Password Login (should fail)")
    resp = client.post("/auth/login", data={
        "username": user_a["email"],
        "password": "wrongpassword"
    })
    print(f"    POST /auth/login (wrong pwd) -> {resp.status_code}")
    assert resp.status_code == 401
    print("    [OK] PASSED")

    # Test 22: Validation - short password
    print("\n[22] Validation - Short Password (should fail)")
    resp = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "short"
    })
    print(f"    POST /auth/register (short pwd) -> {resp.status_code}")
    assert resp.status_code == 422
    print("    [OK] PASSED")

    # Test 23: Validation - invalid email
    print("\n[23] Validation - Invalid Email (should fail)")
    resp = client.post("/auth/register", json={
        "email": "not-an-email",
        "password": "validpass123"
    })
    print(f"    POST /auth/register (bad email) -> {resp.status_code}")
    assert resp.status_code == 422
    print("    [OK] PASSED")

    print("\n" + "=" * 60)
    print("ALL 23 TESTS PASSED!")
    print("=" * 60)
    print("\nPhase IV Authentication Summary:")
    print("  - JWT-based authentication working")
    print("  - Password hashing with bcrypt")
    print("  - User registration with validation")
    print("  - OAuth2 and JSON login endpoints")
    print("  - Protected task endpoints")
    print("  - Complete user isolation (multi-tenant)")
    print("  - Proper error responses (401, 404, 409, 422)")

    client.close()


if __name__ == "__main__":
    test_phase_iv_api()
