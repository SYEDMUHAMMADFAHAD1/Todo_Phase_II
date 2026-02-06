#!/usr/bin/env node

/**
 * Comprehensive e2e test for Todo App
 * Tests:
 * 1. Sign Up - create new user
 * 2. Sign In - sign in with created user
 * 3. Session - verify session
 * 4. Create Todo - create a task
 * 5. Update Todo - mark as completed
 */

const API_BASE = 'http://localhost:8000/api';

async function makeRequest(endpoint, method = 'GET', body = null, token = null) {
  const headers = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const options = {
    method,
    headers,
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  console.log(`\n📡 ${method} ${endpoint}`);
  if (body) console.log('  Body:', JSON.stringify(body));

  const response = await fetch(`${API_BASE}${endpoint}`, options);
  const data = await response.json();

  if (!response.ok) {
    console.error('  ❌ Error:', data);
    throw new Error(data.detail || `Request failed (${response.status})`);
  }

  console.log('  ✅ Success');
  return data;
}

async function test() {
  let token = null;
  let userId = null;
  let todoId = null;

  try {
    console.log('\n======================================');
    console.log('  TESTING TODO APP FULL WORKFLOW');
    console.log('======================================\n');

    // TEST 1: Sign Up
    console.log('\n🔵 TEST 1: Sign Up');
    console.log('-'.repeat(40));
    const timestamp = Date.now();
    const signupResponse = await makeRequest('/auth/signup', 'POST', {
      email: `test${timestamp}@example.com`,
      password: 'TestPassword123!',
      name: 'Test User',
    });

    token = signupResponse.token;
    userId = signupResponse.user.id;
    console.log(`  User ID: ${userId}`);
    console.log(`  Token: ${token.substring(0, 50)}...`);
    console.log(`  Email: ${signupResponse.user.email}`);

    // TEST 2: Get Session
    console.log('\n🔵 TEST 2: Get Session');
    console.log('-'.repeat(40));
    const sessionResponse = await makeRequest('/auth/session', 'GET', null, token);
    console.log(`  User: ${sessionResponse.user.email}`);
    console.log(`  Session ID: ${sessionResponse.session.id}`);

    // TEST 3: Create Todo
    console.log('\n🔵 TEST 3: Create Todo');
    console.log('-'.repeat(40));
    const createTodoResponse = await makeRequest('/tasks', 'POST', {
      title: 'Test Task',
      description: 'This is a test task',
    }, token);

    todoId = createTodoResponse.id;
    console.log(`  Todo ID: ${todoId}`);
    console.log(`  Title: ${createTodoResponse.title}`);
    console.log(`  Status: ${createTodoResponse.status}`);

    // TEST 4: Get Todos
    console.log('\n🔵 TEST 4: Get Todos');
    console.log('-'.repeat(40));
    const getTodosResponse = await makeRequest('/tasks', 'GET', null, token);
    console.log(`  Total Todos: ${getTodosResponse.length}`);
    console.log(`  First Todo: ${getTodosResponse[0].title} (${getTodosResponse[0].status})`);

    // TEST 5: Update Todo Status
    console.log('\n🔵 TEST 5: Update Todo Status to COMPLETED');
    console.log('-'.repeat(40));
    const updateTodoResponse = await makeRequest(
      `/tasks/${todoId}`,
      'PUT',
      { status: 'COMPLETED' },
      token
    );
    console.log(`  Updated Status: ${updateTodoResponse.status}`);
    console.log(`  Updated At: ${updateTodoResponse.updated_at}`);

    // TEST 6: Get Todo and verify status
    console.log('\n🔵 TEST 6: Verify Todo Status');
    console.log('-'.repeat(40));
    const getTodoResponse = await makeRequest(`/tasks/${todoId}`, 'GET', null, token);
    console.log(`  Todo Title: ${getTodoResponse.title}`);
    console.log(`  Current Status: ${getTodoResponse.status}`);

    if (getTodoResponse.status !== 'COMPLETED') {
      throw new Error('Todo status was not updated correctly!');
    }

    console.log('\n======================================');
    console.log('  ✅ ALL TESTS PASSED!');
    console.log('======================================\n');

    console.log('Summary:');
    console.log(`  ✅ Sign Up: User created (${signupResponse.user.email})`);
    console.log(`  ✅ Session: Retrieved session successfully`);
    console.log(`  ✅ Create Todo: Task created (${createTodoResponse.title})`);
    console.log(`  ✅ Get Todos: Retrieved ${getTodosResponse.length} todo(s)`);
    console.log(`  ✅ Update Todo: Status changed to COMPLETED`);
    console.log(`  ✅ Verify Todo: Status verified as COMPLETED`);

  } catch (error) {
    console.error('\n❌ TEST FAILED:', error.message);
    process.exit(1);
  }
}

test();
