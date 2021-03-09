import React, { useState } from "react";
import tw from "twin.macro";
import TextareaAutosize from "react-autosize-textarea";
import { motion } from "framer-motion";
import { AnalyzeResults } from "./Components/AnalyzeResults";

const Container = tw.div`flex min-h-screen p-4 bg-gradient-to-br from-blue-100 to-gray-200`;
const MainContent = tw.div`w-full flex flex-col`;
const TextInput = tw(
  TextareaAutosize
)`border py-2 px-4 rounded-3xl border-gray-200
focus:ring-2 ring-indigo-500 text-gray-500 resize-none text-center
shadow hover:shadow-lg h-10 mx-auto sm:w-full lg:w-2/4 outline-none`;
const Button = tw(
  motion.button
)`rounded-3xl w-40 h-10 m-3 mx-auto bg-gradient-to-br from-blue-400 to-indigo-700 text-blue-50 shadow focus:ring-2 focus:ring-blue-400`;

function App() {
  const [sent, setSent] = useState("");
  const [result, setResult] = useState(undefined);
  const [loading, setLoading] = useState(false);
  const handleAnalyzeText = () => {
    setLoading(true);
    fetch("http://127.0.0.1:8000/analyze?sent=" + sent)
      .then((response) => response.json())
      .then((data) => {
        setResult(data);
      })
      .catch((e) => alert("Error"));
    setLoading(false);
  };

  return (
    <Container>
      <MainContent>
        <div tw="flex flex-col my-auto w-full">
          <TextInput
            placeholder="Enter a sentence to scan here"
            value={sent}
            onChange={(e) => setSent(e.target.value)}
          />

          {!loading ? (
            <Button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              style={{ outline: "none" }}
              onClick={handleAnalyzeText}
            >
              Analyze texte
            </Button>
          ) : (
            <div tw="w-40 h-10 m-3 mx-auto  text-indigo-400 text-2xl uppercase">
              Loading ...
            </div>
          )}
        </div>
        {result && <AnalyzeResults result={result} />}
      </MainContent>
    </Container>
  );
}

export default App;
