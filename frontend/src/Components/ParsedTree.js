import React from "react";
// eslint-disable-next-line no-unused-vars
import tw from "twin.macro";

import { ResultContainer } from "./ResultContainer";

export const ParsedTree = ({ title, parsedTree, image }) => {
  return (
    <ResultContainer title={title}>
      <div tw="p-4 w-full flex flex-col overflow-auto">
        <pre tw="mx-auto text-indigo-700 font-mono  text-xs md:text-base">
          {parsedTree}
        </pre>

        {image && (
          <div tw="flex w-full">
            <img
              tw="mt-6 mx-auto p-2 border-2 rounded-2xl"
              src={`data:image/png;base64,${image}`}
              alt="tree"
            />
          </div>
        )}
      </div>
    </ResultContainer>
  );
};
