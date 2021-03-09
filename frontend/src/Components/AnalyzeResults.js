import React from "react";
import tw from "twin.macro";
import { ParsedTree } from "./ParsedTree";
import { TaggedSentence } from "./TaggedSentence";

const Container = tw.div`m-2 p-4 rounded-3xl bg-blue-50 flex flex-col w-full shadow`;
export const AnalyzeResults = ({ result }) => {
  return (
    <Container>
      <h1 tw="text-3xl mx-auto text-indigo-500 my-2 uppercase">Results</h1>
      <TaggedSentence tagged_sent={result.tagged} />
      <ParsedTree parsedTree={result.parsed} />
    </Container>
  );
};
