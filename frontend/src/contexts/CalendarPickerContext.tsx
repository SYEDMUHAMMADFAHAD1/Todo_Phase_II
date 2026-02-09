import React, { createContext, useContext, useState, ReactNode } from 'react';

interface CalendarPickerContextType {
  showCalendarPicker: boolean;
  setShowCalendarPicker: (show: boolean) => void;
  taskTitle: string;
  setTaskTitle: (title: string) => void;
  taskDescription: string;
  setTaskDescription: (desc: string) => void;
  onTaskCreated?: () => void;
}

const CalendarPickerContext = createContext<CalendarPickerContextType | undefined>(undefined);

export function CalendarPickerProvider({ 
  children, 
  onTaskCreated 
}: { 
  children: ReactNode; 
  onTaskCreated?: () => void; 
}) {
  const [showCalendarPicker, setShowCalendarPicker] = useState(false);
  const [taskTitle, setTaskTitle] = useState('');
  const [taskDescription, setTaskDescription] = useState('');

  return (
    <CalendarPickerContext.Provider 
      value={{ 
        showCalendarPicker, 
        setShowCalendarPicker,
        taskTitle,
        setTaskTitle,
        taskDescription,
        setTaskDescription,
        onTaskCreated
      }}
    >
      {children}
    </CalendarPickerContext.Provider>
  );
}

export function useCalendarPicker() {
  const context = useContext(CalendarPickerContext);
  if (context === undefined) {
    throw new Error('useCalendarPicker must be used within a CalendarPickerProvider');
  }
  return context;
}