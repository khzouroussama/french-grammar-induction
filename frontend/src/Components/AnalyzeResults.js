import React from "react";
import tw from "twin.macro";
import { motion } from "framer-motion";
import { ParsedTree } from "./ParsedTree";
import { TaggedSentence } from "./TaggedSentence";

const Container = tw(
  motion.div
)`sm:m-1 lg:m-2 p-4 rounded-3xl bg-blue-50 flex flex-col shadow`;

export const AnalyzeResults = ({ result }) => {
  return (
    <Container
      animate={{ y: [-10, 0], opacity: [0, 1] }}
      transition={{ ease: "easeIn", duration: 0.4 }}
    >
      <h1 tw="text-3xl mx-auto text-indigo-500 my-2 uppercase">Results</h1>
      <TaggedSentence tagged_sent={result.tagged} />
      <ParsedTree parsedTree={result.parsed} />
    </Container>
  );
};
