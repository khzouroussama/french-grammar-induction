import React from "react";
import tw from "twin.macro";
import { motion } from "framer-motion";
import { ParsedTree } from "./ParsedTree";
import { TaggedSentence } from "./TaggedSentence";
import { MultipleResults } from "./MultipleResults";

const Container = tw(motion.div)`sm:m-1 lg:m-2 p-4 flex flex-col`;

export const AnalyzeResults = ({ result, type }) => {
  return (
    <Container
      layout
      animate={{ opacity: [0, 1], y: [100, 0] }}
      transition={{ duration: 0.2 }}
    >
      <h1 tw="bg-clip-text text-transparent bg-gradient-to-r from-yellow-600 to-indigo-400 text-xl mx-auto my-2 uppercase font-extrabold">
        Results
      </h1>
      {type === "test" ? (
        <>
          <TaggedSentence tagged_sent={result.tagged} />
          <ParsedTree
            title="Parser Results"
            parsedTree={result.parsed}
            image={result.image}
          />
        </>
      ) : (
        <>
          <ParsedTree title="Grammar" parsedTree={result.grammar} />
          <MultipleResults
            title="TestSet Evaluation"
            results={result.test_results}
          />
        </>
      )}
    </Container>
  );
};
