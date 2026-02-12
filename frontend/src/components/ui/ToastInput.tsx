import { useState } from "react";

interface ToastInputProps {
  message: string;
  defaultValue?: string;
  onSubmit: (value: string) => void;
  onClose: () => void;
}

const ToastInput = ({ message, defaultValue = "", onSubmit, onClose }: ToastInputProps) => {
  const [value, setValue] = useState(defaultValue);

  return (
    <div className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50 
                    bg-gray-900 text-white p-4 rounded-lg shadow-lg 
                    flex flex-col gap-3 w-[90%] max-w-md">
      <span>{message}</span>
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="px-2 py-1 rounded bg-gray-800 text-white w-full"
      />
      <div className="flex justify-end gap-2">
        <button
          onClick={() => { onSubmit(value); onClose(); }}
          className="px-3 py-1 bg-green-500 hover:bg-green-600 rounded"
        >
          OK
        </button>
        <button
          onClick={onClose}
          className="px-3 py-1 bg-red-500 hover:bg-red-600 rounded"
        >
          Cancel
        </button>
      </div>
    </div>
  );
};

export default ToastInput;
