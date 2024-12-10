import { useState } from 'react';
import axios from 'axios';

const useDeleteTask = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleDeleteTask = async (taskId) => {
    // if (window.confirm("Are you sure you want to delete this task?")) {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.delete(`/task/delete-task/${taskId}`, {
          withCredentials: true,
        });
        
        console.log("Task deleted:", response.data);
      } catch (err) {
        console.error("Error deleting task:", err);
        setError("An error occurred while deleting the task. Please try again.");
      } finally {
        setLoading(false);
      }
    // }
  };

  return {
    handleDeleteTask,
    loading,
    error,
  };
};

export default useDeleteTask;
