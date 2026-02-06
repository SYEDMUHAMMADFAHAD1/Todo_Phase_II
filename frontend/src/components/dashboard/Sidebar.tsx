'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { motion } from 'framer-motion';
import DashboardVisual from './DashboardVisual'; // Import the new component

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar = ({ isOpen, onClose }: SidebarProps) => {
  const pathname = usePathname();

  const navItems = [
    { name: 'Dashboard', href: '/authenticated/dashboard', icon: '📊' },
    { name: 'All Tasks', href: '/authenticated/dashboard', icon: '📋' },
    { name: 'Pending', href: '/authenticated/dashboard?filter=pending', icon: '⏳' },
    { name: 'Completed', href: '/authenticated/dashboard?filter=completed', icon: '✅' },
    { name: 'Settings', href: '/authenticated/settings', icon: '⚙️' },
  ];

  // Only show DashboardVisual on the dashboard page
  const isDashboardPage = pathname === '/authenticated/dashboard';

  return (
    <>
      {/* Backdrop for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/50 backdrop-blur-sm lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <motion.aside
        initial={{ x: '-100%' }}
        animate={{ x: isOpen ? 0 : '-100%' }}
        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
        className="fixed top-0 left-0 z-30 h-full w-64 bg-slate-900/90 backdrop-blur-xl border-r border-slate-700/50 shadow-2xl lg:relative lg:translate-x-0"
      >
        <div className="flex h-full flex-col pt-16 pb-4">
          {isDashboardPage ? (
            // Show DashboardVisual on dashboard page
            <div className="flex-1 flex flex-col px-4">
              <div className="flex-1">
                <DashboardVisual />
              </div>
              <nav className="space-y-1 mt-4">
                {navItems.map((item) => (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`group flex items-center rounded-xl px-4 py-3 text-sm font-medium transition-all duration-200 ${
                      pathname === item.href
                        ? 'bg-indigo-600/20 text-indigo-300 border-l-4 border-indigo-400'
                        : 'text-slate-300 hover:bg-slate-800/50 hover:text-white'
                    }`}
                  >
                    <span className="mr-3 text-lg">{item.icon}</span>
                    {item.name}
                  </Link>
                ))}
              </nav>
            </div>
          ) : (
            // Show regular navigation on other pages
            <nav className="flex-1 space-y-1 px-4">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`group flex items-center rounded-xl px-4 py-3 text-sm font-medium transition-all duration-200 ${
                    pathname === item.href
                      ? 'bg-indigo-600/20 text-indigo-300 border-l-4 border-indigo-400'
                      : 'text-slate-300 hover:bg-slate-800/50 hover:text-white'
                  }`}
                >
                  <span className="mr-3 text-lg">{item.icon}</span>
                  {item.name}
                </Link>
              ))}
            </nav>
          )}

          <div className="px-4 mt-auto pt-4 border-t border-slate-700/50">
            <div className="flex items-center space-x-3 p-3 rounded-xl bg-slate-800/50">
              <div className="h-10 w-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold">
                {localStorage.getItem('userInitial') || 'U'}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">
                  {localStorage.getItem('userName') || 'User Name'}
                </p>
                <p className="text-xs text-slate-400 truncate">
                  {localStorage.getItem('userEmail') || 'user@example.com'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </motion.aside>
    </>
  );
};

export default Sidebar;