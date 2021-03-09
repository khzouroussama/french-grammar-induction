import React from "react";
import tw from "twin.macro";

import { ResultContainer } from "./ResultContainer";

export const ParsedTree = ({ parsedTree }) => {
  return (
    <ResultContainer title="Parsed Tree">
      <div tw="w-full flex">
        <pre tw="mx-auto text-gray-600 font-bold ">{parsedTree}</pre>
      </div>
    </ResultContainer>
  );
};
