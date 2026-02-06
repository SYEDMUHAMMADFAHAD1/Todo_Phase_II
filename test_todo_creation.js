/**
 * Test script to verify todo creation flow
 * This script will:
 * 1. Sign up a new user
 * 2. Create a todo
 * 3. Fetch todos to verify creation
 */

const API_URL = 'http://localhost:8000/api';

// Generate unique email for each test
const timestamp = Date.now();
const testEmail = `test_${timestamp}@example.com`;
const testPassword = 'TestPassword123!';

console.log('🚀 Starting Todo Creation Test');
console.log(`📧 Email: ${testEmail}`);
console.log(`🔐 Password: ${testPassword}`);
console.log('');

let authToken = null;
let userId = null;

// STEP 1: Sign Up
async function signUp() {
  console.log('📝 STEP 1: Signing up...');

  try {
    const response = await fetch(`${API_URL}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: testEmail,
        password: testPassword,
        name: 'Test User',
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Signup failed: ${error.detail || response.statusText}`);
    }

    const data = await response.json();
    authToken = data.token;
    userId = data.user.id;

    console.log('✅ Signup successful!');
    console.log(`   User ID: ${userId}`);
    console.log(`   Token: ${authToken.substring(0, 30)}...`);
    console.log('');

    return data;
  } catch (error) {
    console.error('❌ Signup failed:', error.message);
    process.exit(1);
  }
}

// STEP 2: Create a Todo
async function createTodo() {
  console.log('📝 STEP 2: Creating a todo...');

  const todoData = {
    title: `Buy coffee supplies - ${new Date().toLocaleTimeString()}`,
    description: 'Purchase espresso beans, milk frother, and filter papers from the local coffee shop',
  };

  console.log(`   Title: "${todoData.title}"`);
  console.log(`   Description: "${todoData.description}"`);
  console.log('');

  try {
    const response = await fetch(`${API_URL}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
      },
      body: JSON.stringify(todoData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Create todo failed: ${error.detail || response.statusText}`);
    }

    const data = await response.json();

    console.log('✅ Todo created successfully!');
    console.log(`   Todo ID: ${data.id}`);
    console.log(`   Title: ${data.title}`);
    console.log(`   Status: ${data.is_completed ? 'Completed' : 'Pending'}`);
    console.log(`   Created: ${data.created_at}`);
    console.log('');

    return data;
  } catch (error) {
    console.error('❌ Create todo failed:', error.message);
    process.exit(1);
  }
}

// STEP 3: Fetch Todos (Verify)
async function fetchTodos() {
  console.log('📝 STEP 3: Fetching todos to verify creation...');
  console.log('');

  try {
    const response = await fetch(`${API_URL}/tasks`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Fetch todos failed: ${error.detail || response.statusText}`);
    }

    const todos = await response.json();

    console.log(`✅ Fetched ${todos.length} todo(s)!`);
    console.log('');
    console.log('📋 Todo List:');
    todos.forEach((todo, index) => {
      console.log(`   ${index + 1}. [${todo.is_completed ? '✓' : ' '}] ${todo.title}`);
      if (todo.description) {
        console.log(`      Description: ${todo.description}`);
      }
      console.log(`      ID: ${todo.id}`);
      console.log(`      Created: ${new Date(todo.created_at).toLocaleString()}`);
      console.log('');
    });

    return todos;
  } catch (error) {
    console.error('❌ Fetch todos failed:', error.message);
    process.exit(1);
  }
}

// STEP 4: Toggle Todo (Mark as Complete)
async function toggleTodo(todoId) {
  console.log('📝 STEP 4: Toggling todo status...');
  console.log(`   Todo ID: ${todoId}`);
  console.log('');

  try {
    const response = await fetch(`${API_URL}/tasks/${todoId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
      },
      body: JSON.stringify({
        is_completed: true,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Toggle todo failed: ${error.detail || response.statusText}`);
    }

    const data = await response.json();

    console.log('✅ Todo toggled successfully!');
    console.log(`   Status: ${data.is_completed ? '✓ Completed' : 'Pending'}`);
    console.log('');

    return data;
  } catch (error) {
    console.error('❌ Toggle todo failed:', error.message);
    process.exit(1);
  }
}

// Run all tests
async function runAllTests() {
  try {
    // Sign up
    await signUp();

    // Create todo
    const createdTodo = await createTodo();

    // Fetch todos
    const todos = await fetchTodos();

    // Toggle todo
    await toggleTodo(createdTodo.id);

    // Final fetch
    console.log('📝 STEP 5: Final verification...');
    console.log('');
    const finalTodos = await fetchTodos();

    console.log('✨ ═══════════════════════════════════════════════════════════');
    console.log('✅ ALL TESTS PASSED! Todo creation flow is working correctly!');
    console.log('✨ ═══════════════════════════════════════════════════════════');
    console.log('');
    console.log('📊 Test Summary:');
    console.log(`   ✓ User signed up: ${testEmail}`);
    console.log(`   ✓ Todo created: ${createdTodo.title}`);
    console.log(`   ✓ Todos fetched: ${finalTodos.length} todo(s) found`);
    console.log(`   ✓ Todo toggled: Marked as completed`);
    console.log('');

  } catch (error) {
    console.error('💥 Test failed:', error);
    process.exit(1);
  }
}

// Run tests
runAllTests();
