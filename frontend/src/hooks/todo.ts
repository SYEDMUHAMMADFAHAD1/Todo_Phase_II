import { useState, useCallback, useEffect } from 'react';
import { apiClient } from '@/lib/api-client';
import { useAuthContext } from '@/contexts/AuthContext';

export interface Todo {
  id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface TodoCreateInput {
  title: string;
  description?: string;
}

export interface TodoUpdateInput {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

export interface UseTodoReturn {
  todos: Todo[];
  loading: boolean;
  error: string | null;
  createTodo: (input: TodoCreateInput) => Promise<Todo>;
  updateTodo: (id: string, input: TodoUpdateInput) => Promise<Todo>;
  deleteTodo: (id: string) => Promise<void>;
  toggleTodo: (id: string) => Promise<Todo>;
  fetchTodos: () => Promise<void>;
  refetch: () => Promise<void>;
}

export function useTodo(): UseTodoReturn {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { session, isLoading: authLoading } = useAuthContext(); // Get session and auth loading state

  const fetchTodos = useCallback(async () => {
    // Wait for auth to be loaded before making requests
    if (authLoading) {
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Ensure we have a valid session before making the request
      if (!session) {
        console.warn('No active session when fetching todos');
        setTodos([]);
        return;
      }

      console.log('Fetching todos from /tasks...');
      const data = await apiClient.get<Todo[]>('/tasks');
      console.log('Todos fetched successfully:', data);
      setTodos(data);
    } catch (err) {
      // Handle both Error instances and plain objects
      let errorMessage = 'Failed to fetch todos';

      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === 'object' && err !== null && 'message' in err) {
        errorMessage = (err as any).message;
      }

      setError(errorMessage);
      console.error('Error fetching todos:', err);
    } finally {
      setLoading(false);
    }
  }, [session, authLoading]);

  const createTodo = useCallback(
    async (input: TodoCreateInput): Promise<Todo> => {
      // Wait for auth to be loaded before making requests
      if (authLoading) {
        throw new Error('Authentication is still loading...');
      }

      try {
        setError(null);

        // Ensure we have a valid session before making the request
        if (!session) {
          throw new Error('No active session. Please sign in.');
        }

        console.log('Creating todo with data:', input);
        const newTodo = await apiClient.post<Todo>('/tasks', input);
        console.log('Todo created successfully:', newTodo);
        setTodos((prev) => [...prev, newTodo]);
        return newTodo;
      } catch (err) {
        // Handle both Error instances and plain objects
        let errorMessage = 'Failed to create todo';

        if (err instanceof Error) {
          errorMessage = err.message;
        } else if (typeof err === 'object' && err !== null && 'message' in err) {
          errorMessage = (err as any).message;
        }

        setError(errorMessage);
        console.error('Error creating todo:', err);
        throw new Error(errorMessage);
      }
    },
    [session, authLoading]
  );

  const updateTodo = useCallback(
    async (id: string, input: TodoUpdateInput): Promise<Todo> => {
      // Wait for auth to be loaded before making requests
      if (authLoading) {
        throw new Error('Authentication is still loading...');
      }

      try {
        setError(null);

        // Ensure we have a valid session before making the request
        if (!session) {
          throw new Error('No active session. Please sign in.');
        }

        const updated = await apiClient.put<Todo>(`/tasks/${id}`, input);
        setTodos((prev) =>
          prev.map((todo) => (todo.id === id ? updated : todo))
        );
        return updated;
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to update todo';
        setError(errorMessage);
        console.error('Error updating todo:', err);
        throw new Error(errorMessage);
      }
    },
    [session, authLoading]
  );

  const deleteTodo = useCallback(async (id: string) => {
    // Wait for auth to be loaded before making requests
    if (authLoading) {
      throw new Error('Authentication is still loading...');
    }

    try {
      setError(null);

      // Ensure we have a valid session before making the request
      if (!session) {
        throw new Error('No active session. Please sign in.');
      }

      // Optimistically remove the task from local state for immediate UI update
      setTodos((prev) => prev.filter((todo) => todo.id !== id));

      // Then delete from the backend
      await apiClient.delete(`/tasks/${id}`);
      
      // Optionally refetch to ensure consistency (remove if optimistic update is sufficient)
      // await fetchTodos();
    } catch (err) {
      // If deletion fails, restore the task to the list
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete todo';
      setError(errorMessage);
      console.error('Error deleting todo:', err);
      
      // Refetch tasks to restore consistent state after failure
      await fetchTodos();
      throw new Error(errorMessage);
    }
  }, [session, authLoading, fetchTodos]);

  const toggleTodo = useCallback(
    async (id: string): Promise<Todo> => {
      // Wait for auth to be loaded before making requests
      if (authLoading) {
        throw new Error('Authentication is still loading...');
      }

      // Ensure we have a valid session before making the request
      if (!session) {
        throw new Error('No active session. Please sign in.');
      }

      const todo = todos.find((t) => t.id === id);
      if (!todo) throw new Error('Todo not found');
      return updateTodo(id, { is_completed: !todo.is_completed });
    },
    [todos, updateTodo, session, authLoading]
  );

  useEffect(() => {
    fetchTodos();
  }, [fetchTodos]);

  return {
    todos,
    loading,
    error,
    createTodo,
    updateTodo,
    deleteTodo,
    toggleTodo,
    fetchTodos,
    refetch: fetchTodos,
  };
}
