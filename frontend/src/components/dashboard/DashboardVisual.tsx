'use client';

import React, { useEffect, useRef, useState, useMemo } from 'react';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';

interface TaskItem {
  id: string;
  title: string;
  status: 'pending' | 'in-progress' | 'completed';
  progress: number;
  createdAt: Date;
}

const DashboardVisual = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const prefersReducedMotion = useReducedMotion();
  const [isMobile, setIsMobile] = useState(false);
  
  // Generate initial task items using useMemo to avoid impure function calls during render
  const initialTasks = useMemo((): TaskItem[] => [
    { id: '1', title: 'Review project proposal', status: 'pending', progress: 0, createdAt: new Date() },
    { id: '2', title: 'Update documentation', status: 'in-progress', progress: 60, createdAt: new Date() },
    { id: '3', title: 'Fix authentication bug', status: 'completed', progress: 100, createdAt: new Date() },
    { id: '4', title: 'Prepare weekly report', status: 'pending', progress: 0, createdAt: new Date() },
    { id: '5', title: 'Team meeting', status: 'in-progress', progress: 30, createdAt: new Date() },
  ], []);

  const [tasks, setTasks] = React.useState<TaskItem[]>(initialTasks);

  // Animation settings
  const animationSpeed = 0.7; // Lower is slower
  const floatAmplitude = isMobile ? 8 : 15; // Reduced amplitude on mobile
  const horizontalRange = isMobile ? 40 : 100; // Reduced range on mobile

  // Check if user prefers reduced motion
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    const handleReduceMotionChange = () => {
      // This effect is handled by framer-motion's useReducedMotion hook
    };

    mediaQuery.addEventListener('change', handleReduceMotionChange);
    return () => mediaQuery.removeEventListener('change', handleReduceMotionChange);
  }, []);

  // Check for mobile responsiveness
  useEffect(() => {
    const checkIsMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkIsMobile();
    window.addEventListener('resize', checkIsMobile);
    return () => window.removeEventListener('resize', checkIsMobile);
  }, []);

  // Function to update task status over time
  useEffect(() => {
    if (prefersReducedMotion) return; // Skip animations if user prefers reduced motion
    
    const interval = setInterval(() => {
      setTasks(prevTasks => {
        return prevTasks.map(task => {
          // Random chance to update task status - using Math.random here is OK in a callback
          if (Math.random() > 0.7 && task.status !== 'completed') {
            if (task.status === 'pending' && Math.random() > 0.5) {
              return { ...task, status: 'in-progress', progress: Math.min(100, task.progress + 20) };
            } else if (task.status === 'in-progress' && Math.random() > 0.6) {
              return { ...task, status: 'completed', progress: 100 };
            }
          }
          
          // For in-progress tasks, increment progress
          if (task.status === 'in-progress' && task.progress < 100) {
            return { ...task, progress: Math.min(100, task.progress + 5) };
          }
          
          return task;
        });
      });
    }, 3000); // Update every 3 seconds

    return () => clearInterval(interval);
  }, [prefersReducedMotion]);

  // Function to add new tasks periodically
  useEffect(() => {
    if (prefersReducedMotion) return; // Skip animations if user prefers reduced motion
    
    const interval = setInterval(() => {
      const newTask: TaskItem = {
        id: `${Date.now()}`,
        title: `New task ${tasks.length + 1}`,
        status: 'pending',
        progress: 0,
        createdAt: new Date(),
      };
      
      setTasks(prev => [...prev.slice(-4), newTask]); // Keep only last 5 tasks
    }, 5000); // Add new task every 5 seconds

    return () => clearInterval(interval);
  }, [tasks.length, prefersReducedMotion]);


  // Render nothing on mobile if user prefers reduced motion
  if (isMobile) {
    return (
      <div 
        data-testid="dashboard-visual" 
        className="hidden md:flex items-center justify-center w-full h-full p-4"
      >
        <div className="text-center text-slate-500 text-sm">
          Task visualization
        </div>
      </div>
    );
  }

  return (
    <div 
      ref={containerRef}
      data-testid="dashboard-visual"
      className="relative w-full h-full overflow-hidden"
      style={{ minHeight: '400px' }}
    >
      {/* Background decorative elements */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-1/4 left-1/4 w-24 h-24 rounded-full bg-indigo-500 blur-2xl"></div>
        <div className="absolute bottom-1/3 right-1/4 w-32 h-32 rounded-full bg-purple-500 blur-2xl"></div>
        <div className="absolute top-1/2 left-1/2 w-16 h-16 rounded-full bg-blue-500 blur-xl"></div>
      </div>

      {/* Floating task items */}
      <AnimatePresence>
        {tasks.map((task, index) => (
          <motion.div
            key={task.id}
            initial={{ 
              opacity: 0, 
              y: 50,
              scale: 0.8
            }}
            animate={{ 
              opacity: 1, 
              y: 0,
              scale: 1
            }}
            exit={{ 
              opacity: 0, 
              scale: 0.8,
              y: -50
            }}
            transition={{
              type: "spring",
              stiffness: 100,
              damping: 20,
              mass: 1,
              delay: index * 0.2
            }}
            className="absolute"
            style={{
              top: `${20 + (index * 15)}%`,
              left: `${10 + (index % 3) * 25}%`,
              zIndex: index + 1
            }}
          >
            <motion.div
              animate={{
                y: [0, floatAmplitude, 0],
                x: [0, horizontalRange, 0, -horizontalRange, 0],
                rotate: [0, 2, -2, 0]
              }}
              transition={{
                duration: 4 * animationSpeed,
                repeat: Infinity,
                ease: "easeInOut",
                delay: index * 0.5
              }}
              className={`relative p-3 rounded-xl backdrop-blur-md border ${
                task.status === 'completed' 
                  ? 'bg-green-500/10 border-green-500/30' 
                  : task.status === 'in-progress'
                  ? 'bg-blue-500/10 border-blue-500/30'
                  : 'bg-slate-800/30 border-slate-700/50'
              } shadow-lg w-32`}
            >
              <div className="flex items-center justify-between mb-1">
                <div className={`w-2 h-2 rounded-full ${
                  task.status === 'completed' 
                    ? 'bg-green-400' 
                    : task.status === 'in-progress'
                    ? 'bg-blue-400'
                    : 'bg-slate-500'
                }`}></div>
                <span className="text-xs text-slate-400">
                  {task.status === 'completed' ? 'Done' : task.status === 'in-progress' ? 'In Progress' : 'Pending'}
                </span>
              </div>
              
              <p className="text-xs text-slate-300 truncate mb-2">{task.title}</p>
              
              {/* Progress bar */}
              <div className="w-full h-1.5 bg-slate-700/50 rounded-full overflow-hidden">
                <motion.div
                  className={`h-full ${
                    task.status === 'completed' 
                      ? 'bg-green-400' 
                      : task.status === 'in-progress'
                      ? 'bg-blue-400'
                      : 'bg-slate-500'
                  }`}
                  initial={{ width: 0 }}
                  animate={{ width: `${task.progress}%` }}
                  transition={{ duration: 0.5 }}
                />
              </div>
              
              {/* Checkmark animation for completed tasks */}
              {task.status === 'completed' && (
                <motion.div
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 0.2 }}
                  className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-green-500 flex items-center justify-center"
                >
                  <svg 
                    className="w-3 h-3 text-white" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
                  </svg>
                </motion.div>
              )}
            </motion.div>
          </motion.div>
        ))}
      </AnimatePresence>

      {/* Floating particles for extra visual interest */}
      {!prefersReducedMotion && [...Array(8)].map((_, i) => {
        // Generate deterministic values based on index to avoid Math.random during render
        const particleX = (i * 123.456) % 100; // Deterministic based on index
        const particleY = (i * 987.654) % 100; // Deterministic based on index
        
        return (
          <motion.div
            key={`particle-${i}`}
            className="absolute w-1 h-1 rounded-full bg-slate-600"
            initial={{ 
              x: particleX, 
              y: particleY,
              opacity: 0.3
            }}
            animate={{
              y: [null, -20, null],
              x: [null, (i * 45.678) % 40 - 20, null], // Deterministic based on index
              opacity: [0.3, 0.7, 0.3],
            }}
            transition={{
              duration: 3 + (i * 0.3) % 2, // Deterministic based on index
              repeat: Infinity,
              ease: "easeInOut",
              delay: i * 0.5
            }}
            style={{
              top: `${particleY}%`,
              left: `${particleX}%`,
            }}
          />
        );
      })}

      {/* Subtle grid lines for depth */}
      <div className="absolute inset-0 opacity-5 pointer-events-none">
        <div className="grid grid-cols-4 gap-8 h-full w-full">
          {[...Array(4)].map((_, i) => (
            <div key={`grid-line-${i}`} className="border-r border-slate-400"></div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DashboardVisual;