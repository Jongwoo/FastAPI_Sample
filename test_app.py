#!/usr/bin/env python3
"""
Simple test script to verify the FastAPI application works correctly
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app.domain.task_service import TaskService
from app.infra.task_repository_impl import InMemoryTaskRepository
from app.domain.task_models import TaskCreateRequest

def test_task_service():
    """Test the task service functionality"""
    print("Testing Task Service...")
    
    # Create repository and service
    repository = InMemoryTaskRepository()
    service = TaskService(repository)
    
    # Test creating a task
    print("1. Creating a task...")
    task = service.create_task("Test Task", "This is a test task")
    print(f"   Created task: {task}")
    
    # Test getting all tasks
    print("2. Getting all tasks...")
    tasks = service.get_all_tasks()
    print(f"   Total tasks: {len(tasks)}")
    for task in tasks:
        print(f"   - {task.title}: {task.description}")
    
    # Test creating another task
    print("3. Creating another task...")
    task2 = service.create_task("Second Task", "Another test task")
    print(f"   Created task: {task2}")
    
    # Test getting all tasks again
    print("4. Getting all tasks after creating second one...")
    tasks = service.get_all_tasks()
    print(f"   Total tasks: {len(tasks)}")
    for task in tasks:
        print(f"   - ID: {task.id}, Title: {task.title}, Completed: {task.completed}")
    
    print("✅ All tests passed!")

def test_error_handling():
    """Test error handling"""
    print("\nTesting Error Handling...")
    
    repository = InMemoryTaskRepository()
    service = TaskService(repository)
    
    # Test creating task with empty title
    print("1. Testing empty title validation...")
    try:
        service.create_task("", "Empty title test")
        print("   ❌ Should have raised ValueError")
    except ValueError as e:
        print(f"   ✅ Correctly raised ValueError: {e}")
    
    # Test creating task with whitespace title
    print("2. Testing whitespace title validation...")
    try:
        service.create_task("   ", "Whitespace title test")
        print("   ❌ Should have raised ValueError")
    except ValueError as e:
        print(f"   ✅ Correctly raised ValueError: {e}")
    
    print("✅ Error handling tests passed!")

if __name__ == "__main__":
    print("=== FastAPI Task Service Test ===\n")
    
    try:
        test_task_service()
        test_error_handling()
        print("\n🎉 All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
