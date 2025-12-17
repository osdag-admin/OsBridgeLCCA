"use client"

import { useState, useEffect } from "react"

// Form sequence constant
const FORM_SEQUENCE = [
  'Foundation',
  'Sub-Structure',
  'Super-Structure',
  'Miscellaneous',
  'Economic Parameter',
  'Carbon Emission Data',
  'Carbon Emission Cost Data',
  'Bridge and Traffic',
  'Maintenance and Repair Data',
  'Demolition and Recycling',
];

// Navigation Hook
export const useFormNavigation = (currentForm, onNavigate) => {
  const getCurrentIndex = () => FORM_SEQUENCE.indexOf(currentForm);
  const canGoNext = () => getCurrentIndex() < FORM_SEQUENCE.length - 1;
  const canGoBack = () => getCurrentIndex() > 0;
  
  const getNextForm = () => {
    const nextIndex = getCurrentIndex() + 1;
    return nextIndex < FORM_SEQUENCE.length ? FORM_SEQUENCE[nextIndex] : null;
  };
  
  const getPreviousForm = () => {
    const prevIndex = getCurrentIndex() - 1;
    return prevIndex >= 0 ? FORM_SEQUENCE[prevIndex] : null;
  };

  return {
    canGoNext: canGoNext(),
    canGoBack: canGoBack(),
    getNextForm,
    getPreviousForm,
    navigate: onNavigate
  };
};

// Confirmation Modal Component
export const ConfirmationModal = ({ isOpen, onClosed, onConfirm, type, nextForm }) => {
  if (!isOpen) return null;

  const isNext = type === 'next';
  const title = isNext ? 'Save and Continue?' : 'Go Back?';
  const message = isNext 
    ? `Do you want to save your current progress and navigate to ${nextForm}?`
    : 'Are you sure you want to go back? Any unsaved changes will be lost.';
  const confirmText = isNext ? 'Save & Continue' : 'Go Back';
  const cancelText = 'Cancel';

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 className="text-lg font-semibold mb-4">{title}</h3>
        <p className="text-gray-600 mb-6">{message}</p>
        <div className="flex justify-end gap-3">
          <button
            onClick={onClosed}
            className="px-4 py-2 text-gray-600 border border-gray-300 rounded hover:bg-gray-50"
          >
            {cancelText}
          </button>
          <button
            onClick={onConfirm}
            className={`px-4 py-2 rounded text-white ${
              isNext 
                ? 'bg-blue-600 hover:bg-blue-700' 
                : 'bg-red-600 hover:bg-red-700'
            }`}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
};

export default {useFormNavigation,ConfirmationModal};