import React from "react";
// eslint-disable-next-line no-unused-vars
import tw from "twin.macro";

import { ResultContainer } from "./ResultContainer";

export const MultipleResults = ({ title, results }) => {
  const detected = results.valide.length;
  const total = results.valide.length + results.not_valide.length;
  return (
    <ResultContainer title={title}>
      <div tw="p-4 w-full flex flex-col overflow-auto">
        <h1 tw="my-2 mx-auto text-3xl text-pink-600 font-bold bg-pink-100 p-6 rounded-3xl">
          Evaluation :{" "}
          {`${detected} Sentences detected from ${total} (${(
            (detected * 100) /
            total
          ).toFixed(2)}%)`}
        </h1>
        <h4 tw="my-2 mx-auto text-2xl text-pink-700 font-bold">
          Valide Sentences
        </h4>
        <div tw="flex flex-col w-full">
          {results.valide.map((result, indx) => (
            <div
              key={indx}
              tw="mx-auto text-indigo-700 font-mono  text-xs md:text-base"
            >
              <div tw="bg-indigo-100 p-4 px-6 rounded-2xl  mb-2">
                {result[0]}
              </div>
              <div tw="w-full flex">
                <pre tw="mx-auto my-2">{result[1]}</pre>
              </div>
            </div>
          ))}
        </div>
      </div>
      <h4 tw="my-2 mx-auto text-2xl text-pink-700 font-bold">
        Invalide Sentences
      </h4>
      <div tw="flex flex-col w-full ">
        {results.not_valide.map((result, indx) => (
          <div
            key={indx}
            tw="mx-auto text-indigo-700 font-mono  text-xs md:text-base flex flex-col"
          >
            <div tw="bg-indigo-100 p-4 px-6 rounded-2xl mb-2">{result} </div>
          </div>
        ))}
      </div>
    </ResultContainer>
  );
};
