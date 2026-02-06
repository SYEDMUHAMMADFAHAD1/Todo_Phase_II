import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  actions?: React.ReactNode;
  footer?: React.ReactNode;
}

export default function Card({
  children,
  className = '',
  title,
  actions,
  footer,
}: CardProps) {
  return (
    <div className={`bg-background rounded-xl border border-border shadow-sm overflow-hidden ${className}`}>
      {(title || actions) && (
        <div className="px-6 py-4 border-b border-border flex items-center justify-between">
          {title && (
            <h3 className="text-lg font-semibold text-foreground">
              {title}
            </h3>
          )}
          {actions && (
            <div className="flex items-center space-x-2">
              {actions}
            </div>
          )}
        </div>
      )}
      <div className="px-6 py-4">
        {children}
      </div>
      {footer && (
        <div className="px-6 py-4 bg-muted/10 border-t border-border">
          {footer}
        </div>
      )}
    </div>
  );
}