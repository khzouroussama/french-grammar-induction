import React, { useState } from "react";
import tw from "twin.macro";
import TextareaAutosize from "react-autosize-textarea";
import { motion, AnimateSharedLayout } from "framer-motion";

import { AnalyzeResults } from "./Components/AnalyzeResults";

import { ImSpinner9 } from "react-icons/im";
import { IoBarcodeOutline } from "react-icons/io5";

let API =
  process.env.NODE_ENV === "production"
    ? process.env.REACT_APP_PROD_API
    : process.env.REACT_APP_DEV_API;

const Container = tw.div`flex min-h-screen p-2 lg:p-4 bg-blue-50 bg-opacity-30`;
const MainContent = tw(motion.div)`w-full flex flex-col`;
const TextInput = tw(TextareaAutosize)`border p-4 rounded-3xl border-gray-200
ring-2 ring-pink-700 text-gray-500 resize-none text-center
 hover:shadow-xl h-8 mx-auto w-full lg:w-2/4 outline-none`;
const Button = tw(
  motion.div
)`cursor-pointer flex align-middle rounded-3xl px-6 font-bold h-10 m-3 mx-auto bg-gradient-to-br from-indigo-600 via-pink-600 to-yellow-500 text-white shadow focus:ring-2 focus:ring-yellow-400`;

function App() {
  const [sent, setSent] = useState(
    "Elle a aussi plaidé pour une réforme de la procédure pénale pour qu'elle soit adaptée aux articles de la Déclaration Universelle des Droits de l'Homme, sur les droits des prisonniers à comparaître devant un tribunal indépendant et impartial et à disposer de garanties de procédures et de la présomption d'innocence."
  );
  const [result, setResult] = useState(undefined);
  const [loading, setLoading] = useState(false);

  const handleAnalyzeText = () => {
    setLoading(true);
    setResult(undefined);

    fetch(`${API}/analyze?sent=${sent}`)
      .then((response) => response.json())
      .then((data) => {
        setResult(data);
        setLoading(false);
      })
      .catch((e) => {
        alert("Error");
        setLoading(false);
      });
  };

  return (
    <AnimateSharedLayout>
      <Container>
        <MainContent>
          <motion.div layout tw="flex flex-col my-auto w-full">
            <IoBarcodeOutline tw="mx-auto text-7xl text-pink-600" />
            <h1 tw="mx-auto text-4xl font-bold mb-4 text-center text-transparent  bg-clip-text bg-gradient-to-br from-yellow-300 via-pink-500 to-indigo-600 ">
              Analyse sentence
            </h1>
            <TextInput
              placeholder="Enter a sentence to scan here"
              value={sent}
              onChange={(e) => setSent(e.target.value)}
            />

            {loading ? (
              <div tw="flex flex-col h-10 m-3 mx-auto text-pink-600 ">
                <div tw="my-2">
                  <ImSpinner9 tw="animate-spin text-7xl text-center mx-auto" />
                </div>
                <div tw="mx-auto font-bold">Analyzing</div>
              </div>
            ) : (
              <Button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                style={{ outline: "none" }}
                onClick={handleAnalyzeText}
              >
                <span tw="my-auto">Analyse {result && "new"} sentence</span>
              </Button>
            )}
          </motion.div>
          {result && <AnalyzeResults result={result} />}
        </MainContent>
      </Container>
    </AnimateSharedLayout>
  );
}

export default App;
