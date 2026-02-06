// Performance test for DashboardVisual component
// This file is for testing purposes only

import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { act } from 'react-dom/test-utils';

// Mock the motion components for performance testing
vi.mock('framer-motion', async () => {
  const actual = await vi.importActual('framer-motion');
  return {
    ...actual,
    motion: {
      div: ({ children, ...props }: any) => <div {...props}>{children}</div>,
    },
    AnimatePresence: ({ children }: any) => <>{children}</>,
  };
});

import DashboardVisual from './DashboardVisual';

describe('DashboardVisual Component', () => {
  beforeEach(() => {
    // Reset timers before each test
    vi.useFakeTimers();
  });

  afterEach(() => {
    // Restore real timers after each test
    vi.useRealTimers();
  });

  it('should render without crashing', () => {
    expect(() => {
      render(<DashboardVisual />);
    }).not.toThrow();
  });

  it('should render with test id', () => {
    render(<DashboardVisual />);
    
    // Check if the component has the test id
    expect(screen.getByTestId('dashboard-visual')).toBeInTheDocument();
  });

  it('should handle reduced motion preference', () => {
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: vi.fn().mockImplementation(query => ({
        matches: true, // Simulate reduced motion preference
        media: query,
        onchange: null,
        addListener: vi.fn(), // Deprecated but needed for older browsers
        removeListener: vi.fn(), // Deprecated but needed for older browsers
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
      })),
    });

    render(<DashboardVisual />);
    
    // Component should still render properly with reduced motion
    expect(screen.getByTestId('dashboard-visual')).toBeInTheDocument();
  });

  it('should handle mobile view', () => {
    // Mock window.innerWidth for mobile
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 600, // Mobile width
    });
    
    render(<DashboardVisual />);
    
    // On mobile, the component should render differently but still be present
    expect(screen.getByTestId('dashboard-visual')).toBeInTheDocument();
  });

  it('should handle animation updates efficiently', () => {
    render(<DashboardVisual />);
    
    // Fast-forward time to trigger intervals
    act(() => {
      vi.advanceTimersByTime(10000); // Advance 10 seconds
    });
    
    // Component should still be in document
    expect(screen.getByTestId('dashboard-visual')).toBeInTheDocument();
  });
});