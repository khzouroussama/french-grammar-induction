import React from "react";
import tw from "twin.macro";
import { motion } from "framer-motion";
import { ParsedTree } from "./ParsedTree";
import { TaggedSentence } from "./TaggedSentence";

const Container = tw(motion.div)`sm:m-1 lg:m-2 p-4 flex flex-col`;

export const AnalyzeResults = ({ result }) => {
  return (
    <Container
      layout
      animate={{ opacity: [0, 1], y: [100, 0] }}
      transition={{ duration: 0.2 }}
    >
      <h1 tw="bg-clip-text text-transparent bg-gradient-to-r from-yellow-600 to-indigo-400 text-xl mx-auto my-2 uppercase font-extrabold">
        Results
      </h1>
      <TaggedSentence tagged_sent={result.tagged} />
      <ParsedTree parsedTree={result.parsed} image={result.image} />
    </Container>
  );
};
