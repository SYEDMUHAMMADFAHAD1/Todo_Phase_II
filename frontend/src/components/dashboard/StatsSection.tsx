'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { UseTodoReturn } from '@/hooks/todo';
import Skeleton from '@/components/common/Skeleton';

interface StatsSectionProps {
  todo: UseTodoReturn;
}

const StatCard = ({ 
  title, 
  value, 
  icon,
  gradient 
}: { 
  title: string; 
  value: number; 
  icon: string;
  gradient: string;
}) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = value;
    const duration = 1000;
    const increment = end / (duration / 16); // ~60fps
    
    const timer = setInterval(() => {
      start += increment;
      if (start >= end) {
        setCount(end);
        clearInterval(timer);
      } else {
        setCount(Math.floor(start));
      }
    }, 16);

    return () => clearInterval(timer);
  }, [value]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`bg-gradient-to-br ${gradient} backdrop-blur-sm rounded-2xl p-6 border border-slate-700/30 shadow-xl`}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-slate-300">{title}</p>
          <p className="text-4xl font-bold text-white mt-2">{count}</p>
        </div>
        <div className="h-12 w-12 rounded-full bg-white/10 flex items-center justify-center text-xl">
          {icon}
        </div>
      </div>
    </motion.div>
  );
};

const StatsSection = ({ todo }: StatsSectionProps) => {
  const completedCount = todo.todos.filter((t) => t.is_completed).length;
  const pendingCount = todo.todos.length - completedCount;
  const completionRate = todo.todos.length > 0 
    ? Math.round((completedCount / todo.todos.length) * 100) 
    : 0;

  if (todo.loading) {
    return (
      <div className="mb-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[...Array(4)].map((_, index) => (
            <Skeleton 
              key={index} 
              className="h-32 rounded-2xl" 
            />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="mb-8">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard 
          title="Total Tasks" 
          value={todo.todos.length} 
          icon="📋" 
          gradient="from-slate-800/50 to-slate-700/30" 
        />
        <StatCard 
          title="Completed" 
          value={completedCount} 
          icon="✅" 
          gradient="from-emerald-900/40 to-emerald-800/30" 
        />
        <StatCard 
          title="Pending" 
          value={pendingCount} 
          icon="⏳" 
          gradient="from-amber-900/40 to-amber-800/30" 
        />
        <div className={`bg-gradient-to-br from-indigo-900/40 to-indigo-800/30 backdrop-blur-sm rounded-2xl p-6 border border-slate-700/30 shadow-xl`}>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-300">Completion Rate</p>
              <p className="text-4xl font-bold text-white mt-2">{completionRate}%</p>
            </div>
            <div className="h-12 w-12 rounded-full bg-white/10 flex items-center justify-center text-xl">
              📊
            </div>
          </div>
          <div className="mt-4">
            <div className="w-full bg-slate-700/50 rounded-full h-2">
              <motion.div 
                className="bg-gradient-to-r from-indigo-500 to-purple-500 h-2 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${completionRate}%` }}
                transition={{ duration: 1, ease: "easeOut" }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatsSection;