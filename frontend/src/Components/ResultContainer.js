import React from "react";
// eslint-disable-next-line no-unused-vars
import tw from "twin.macro";

export const ResultContainer = ({ title, children }) => {
  return (
    <div tw="mt-8 relative flex flex-wrap rounded-2xl p-2 py-4 border-2 border-gray-200">
      <div tw="absolute right-1/2 transform -translate-y-full translate-x-1/2 text-xl text-blue-700 bg-blue-100 rounded-full p-1 px-4 shadow-inner">
        {title}
      </div>
      {children}
    </div>
  );
};
