
import React from 'react';
import { cn } from '@/lib/utils';

interface PresentationSlideProps {
  children: React.ReactNode;
  className?: string;
  background?: string;
}

const PresentationSlide = ({ children, className, background = "bg-gradient-to-br from-blue-50 to-indigo-100" }: PresentationSlideProps) => {
  return (
    <div className={cn(
      "w-full h-screen flex flex-col justify-center items-center p-8 relative overflow-hidden",
      background,
      className
    )}>
      {children}
    </div>
  );
};

export default PresentationSlide;
