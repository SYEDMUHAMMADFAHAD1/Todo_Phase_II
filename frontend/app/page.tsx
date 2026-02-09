'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';

export default function HomePage() {
  const features = [
    {
      icon: '📝',
      title: 'Create Tasks with AI',
      description: 'Use our intelligent AI assistant to create and manage tasks effortlessly.'
    },
    {
      icon: '⏰',
      title: 'Smart Date & Time Reminders',
      description: 'Never miss a deadline with our automated reminder system.'
    },
    {
      icon: '🔔',
      title: '1 Hour Before Alerts',
      description: 'Get notified one hour before your scheduled tasks begin.'
    },
    {
      icon: '🤖',
      title: 'AI Assistant Support',
      description: 'Get help with task management through our friendly AI assistant.'
    },
    {
      icon: '📈',
      title: 'Track Progress',
      description: 'Monitor your pending and completed tasks with detailed analytics.'
    },
    {
      icon: '🔒',
      title: 'Secure & Private',
      description: 'Your data is encrypted and stored securely with industry best practices.'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-950 to-black text-white">
      {/* Header */}
      <header className="py-6 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center">
              <span className="text-xl font-bold">T</span>
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              TaskFlow
            </h1>
          </div>
          <div className="flex space-x-4">
            <Link 
              href="/signin" 
              className="px-4 py-2 rounded-lg font-medium text-slate-300 hover:text-white hover:bg-slate-800/50 transition-colors duration-200"
            >
              Sign In
            </Link>
            <Link 
              href="/signup" 
              className="px-4 py-2 rounded-lg font-medium bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 transition-all duration-200 shadow-lg shadow-indigo-500/20 hover:shadow-indigo-500/30"
            >
              Create Account
            </Link>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <section className="max-w-4xl mx-auto text-center mb-20">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Manage your tasks <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">smarter</span> with AI-powered Todo
            </h1>
            <p className="text-xl text-slate-400 mb-10 max-w-2xl mx-auto">
              Boost your productivity with our intelligent task management system. 
              Create, organize, and track tasks with AI assistance and smart reminders.
            </p>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="flex flex-col sm:flex-row justify-center gap-4"
          >
            <Link 
              href="/signin"
              className="px-8 py-4 rounded-xl font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 transition-all duration-200 shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/40 text-lg"
            >
              Sign In to Dashboard
            </Link>
            <Link 
              href="/signup"
              className="px-8 py-4 rounded-xl font-semibold bg-slate-800/50 text-white hover:bg-slate-700/50 transition-colors duration-200 border border-slate-700/50 text-lg"
            >
              Create New Account
            </Link>
          </motion.div>
        </section>

        {/* Features Section */}
        <section className="mb-20">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">Powerful Features for Productivity</h2>
            <p className="text-slate-400 max-w-2xl mx-auto">
              Our platform offers everything you need to manage your tasks efficiently
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ y: -5 }}
                className="bg-slate-800/30 backdrop-blur-sm rounded-2xl p-6 border border-slate-700/50 hover:border-slate-600/50 transition-all duration-300"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-slate-400">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* CTA Section */}
        <section className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="bg-gradient-to-r from-slate-800/50 to-slate-900/50 rounded-2xl p-8 border border-slate-700/50"
          >
            <h2 className="text-3xl font-bold mb-4">Ready to boost your productivity?</h2>
            <p className="text-slate-400 mb-6 max-w-2xl mx-auto">
              Join thousands of users who trust our platform to manage their tasks efficiently.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link 
                href="/signup"
                className="px-8 py-4 rounded-xl font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 transition-all duration-200 shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/40"
              >
                Get Started Free
              </Link>
              <Link 
                href="/signin"
                className="px-8 py-4 rounded-xl font-semibold bg-slate-800/50 text-white hover:bg-slate-700/50 transition-colors duration-200 border border-slate-700/50"
              >
                Sign In to Account
              </Link>
            </div>
          </motion.div>
        </section>
      </main>

      {/* Footer */}
      <footer className="py-8 px-4 sm:px-6 lg:px-8 border-t border-slate-800/50">
        <div className="max-w-7xl mx-auto text-center text-slate-500 text-sm">
          <p>© {new Date().getFullYear()} TaskFlow. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}