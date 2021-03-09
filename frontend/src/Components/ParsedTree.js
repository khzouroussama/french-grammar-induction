import React from "react";
// eslint-disable-next-line no-unused-vars
import tw from "twin.macro";

import { ResultContainer } from "./ResultContainer";

export const ParsedTree = ({ parsedTree }) => {
  return (
    <ResultContainer title="Parsed Tree">
      <div tw="p-4 w-full flex overflow-auto">
        <pre tw="mx-auto text-blue-900 font-mono  text-xs md:text-base">
          {parsedTree}
        </pre>
      </div>
    </ResultContainer>
  );
};
