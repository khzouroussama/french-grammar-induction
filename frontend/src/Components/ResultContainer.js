import React from "react";
import { motion } from "framer-motion";
// eslint-disable-next-line no-unused-vars
import tw from "twin.macro";

export const ResultContainer = ({ title, children }) => {
  return (
    <motion.div
      layout
      tw="mt-8 relative flex flex-wrap rounded-2xl p-2 py-4 border-2 border-indigo-200 bg-white shadow-lg"
    >
      <div tw="absolute border right-1/2 transform -translate-y-full translate-x-1/2 text-lg font-bold text-pink-700 bg-indigo-100 shadow-inner rounded-full p-1 px-4 ">
        {title}
      </div>
      {children}
    </motion.div>
  );
};
