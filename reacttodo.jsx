import { useState } from 'react';
import './TodoList.css';

function TodoList() {
  const [todos, setTodos] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const handleAddTodo = () => {
    if (inputValue.trim() === '') return;
    setTodos([...todos, inputValue.trim()]);
    setInputValue('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleAddTodo();
    }
  };

  return (
    <div className="todo-container">
      <h1>Simple Todo List</h1>

      <div className="input-area">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Add a new todo..."
        />
        <button onClick={handleAddTodo}>Add</button>
      </div>

      <ul className="todo-list">
        {todos.length === 0 ? (
          <p className="empty-message">No todos yet. Add one!</p>
        ) : (
          todos.map((todo, index) => (
            <li key={index} className="todo-item">
              {todo}
            </li>
          ))
        )}
      </ul>
    </div>
  );
}

export default TodoList;