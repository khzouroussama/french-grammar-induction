import React from "react";
// eslint-disable-next-line no-unused-vars
import tw from "twin.macro";

import { ResultContainer } from "./ResultContainer";

const TaggedWord = ({ word, tag }) => (
  <div tw="py-2 px-4 my-2">
    <div tw="relative">
      <div tw="absolute text-xs bottom-0 right-0 transform translate-y-3/4 translate-x-1/2 bg-yellow-400 text-indigo-500 font-bold  px-2 rounded-2xl w-auto shadow">
        {tag}
      </div>
      <span tw="text-lg bg-indigo-100 rounded-lg text-gray-600 p-2 shadow border-2 border-yellow-400">
        {word}
      </span>
    </div>
  </div>
);

export const TaggedSentence = ({ tagged_sent }) => {
  return (
    <ResultContainer title="POS Tagging">
      {tagged_sent.map((tagged_word, idx) => (
        <TaggedWord key={idx} word={tagged_word[0]} tag={tagged_word[1]} />
      ))}
    </ResultContainer>
  );
};
